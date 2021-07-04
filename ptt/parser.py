import re
from bs4 import BeautifulSoup  # type: ignore
from bs4.element import Tag  # type: ignore
from functools import lru_cache
import requests  # type: ignore
import asyncio
import concurrent.futures
from typing import Optional, List, cast

from .page import DefaultPage, SearchPage, PageManager
from .article import PttArticle
from .type import Like, Url


class UnknownBoardError(Exception):
    pass


class PttPost:

    def __init__(self, tag: Tag) -> None:
        self._tag = tag

    @property
    def title(self) -> str:
        title = self.tag.find(attrs={'class': 'title'}).text
        return re.sub('\n', '', title)

    @property
    def link(self) -> Optional[Url]:
        try:
            href = self.tag.find(attrs={'class': 'title'}).a['href']
            link: Optional[Url] = Url('https://www.ptt.cc' + href)
        except Exception:
            link = None
        finally:
            return link

    @property
    def author(self) -> str:
        return self.meta.find(attrs={'class', 'author'}).text

    @property
    def date(self) -> str:
        return self.meta.find(attrs={'class': 'date'}).text.lstrip()

    @property
    def like(self) -> Like:
        like = self.tag.find(attrs={'class': 'nrec'}).text
        return Like(like)

    @property
    def meta(self) -> Tag:
        return self.tag.find('div', {'class': 'meta'})

    @property
    def tag(self) -> Tag:
        return self._tag

    def __str__(self) -> str:
        return f"{self.like} {self.title}"

    def __repr__(self) -> str:
        return f"{self.author}: {self.title}"


class PttSession:

    _isintance = None
    _over18_url = 'https://www.ptt.cc/ask/over18'

    def get_session(self) -> requests.Session:
        if self._isintance is None:
            session = requests.Session()
            res = session.post(self._over18_url, data={'yes': 'yes'})
            assert res.status_code == 200, f"{res.status_code}, {res.text}"
            self._isintance = session
        return self._isintance


class PttSpider:

    URL_REGEX = re.compile(r'/bbs/(?P<board>\w+)/index(?P<indx>\d+).html')

    def __init__(self, board: str) -> None:
        self.board = board
        self._set_page_manager()

    def _set_page_manager(self) -> None:
        page_indx = self.get_page_indx()
        self._defaultpage = DefaultPage(self.start_url)
        self._defaultpage.set_page_indx(page_indx)
        self._searchpage = SearchPage(self.start_url)

    @property
    def start_url(self) -> Url:
        return Url(f"https://www.ptt.cc/bbs/{self.board}/index.html")

    def get_page_indx(self) -> int:
        soup = self._get_soup(self.start_url)
        tag: Optional[Tag] = next(
            (tag for tag in soup.find_all('a', {'class': 'btn wide'})
             if "上頁" in tag.text),
            None
        )
        if tag is None:
            raise UnknownBoardError(f'Inaccessiable board({self.board})')
        m = self.URL_REGEX.fullmatch(tag['href'])
        assert m, 'Not match url regex'
        return int(m.group('indx')) + 1

    def _get_request_method(self):
        session = PttSession()
        return session.get_session()

    @lru_cache()
    def _get_soup(self, url: Url) -> BeautifulSoup:
        rq = self._get_request_method()
        response = rq.get(url)
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, 'html.parser')

    def refresh(self) -> None:
        self._get_soup.cache_clear()

    def parse(self, post_num, **kwargs) -> List[PttPost]:
        page_manger: PageManager
        if kwargs.get('keyword') or kwargs.get('author') \
                or kwargs.get('recommend'):
            page_manger = self._searchpage
        else:
            page_manger = self._defaultpage
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            self._parse(post_num, page_manger, **kwargs)
        )

    async def _parse(
        self,
        post_num: int,
        page_manager: PageManager,
        **kwargs,
    ) -> List[PttPost]:
        posts: List[PttPost] = []
        search_page_num = post_num // 20 + 2
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            res = [
                executor.submit(self._get_soup, cur_url)
                for cur_url in page_manager.get_urls(search_page_num, **kwargs)
            ]
            concurrent.futures.wait(res)
        for r in res:
            soup = r.result()
            posts.extend(
                [PttPost(tag)
                 for tag in soup.find_all('div', {'class': 'r-ent'})]
            )
        return posts[:post_num]


class PostReader:
    """ read PttPost
    """

    def read(self, post: PttPost) -> Optional[PttArticle]:
        if post.link is None:
            return None
        rq = self._get_request_method()
        response = rq.get(post.link)
        response.encoding = 'utf-8'
        tag = BeautifulSoup(response.text, 'html.parser')
        return PttArticle(tag)

    def _get_request_method(self):
        session = PttSession()
        return session.get_session()

    def read_posts(self, posts: List[PttPost]) -> List[PttArticle]:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._read_posts(posts))

    async def _read_posts(self, posts: List[PttPost]) -> List[PttArticle]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            res = [
                executor.submit(self.read, post)
                for post in posts
            ]
            concurrent.futures.wait(res)
        return cast(
            List[PttArticle],
            [r.result() for r in res
             if r.result() and r.result().tag.title.string != '404']
        )
