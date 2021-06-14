import re
from typing import List
from bs4.element import Tag  # type: ignore


class PttPush:
    ''' ptt 推文 in ptt Article


    Attributes:

        push_tag (str): 推, 噓 or →

        user (str): User name of this push

        content (str): The content of this push

        time (str): Time string (ex: 06/12 21:22)

        tag (Tag): Beauitifulsoup tag of this push

    '''

    def __init__(self, tag: Tag) -> None:
        self._tag = tag
        self._push_tag = self.tag.span.text
        self._user = self.tag.find(attrs={'class': 'f3 hl push-userid'}).text
        self._content = self.tag.find(attrs={'class': 'f3 push-content'}).text
        self._time = self.tag.find(attrs={'class': 'push-ipdatetime'}).text

    @property
    def push_tag(self) -> str:
        return self._push_tag.strip(' ')

    @property
    def user(self) -> str:
        return self._user.strip(' ')

    @property
    def content(self) -> str:
        return re.sub(r'^\s*:\s*', '', self._content)

    @property
    def time(self) -> str:
        return self._time.strip(' \n')

    @property
    def tag(self) -> Tag:
        return self._tag

    def __repr__(self) -> str:
        return self.content


class PttArticle:
    ''' Ptt Article


    Attributes:

        tag (Tag): Beauitifulsoup tag of this page
        author (str): Article author
        title (str): Article title
        date (str): Time string (ex: Sat Jun 12 19:24:25 2021)
        contents (str): All text in this page
        body (str): the content of the article
        ip (str): IP of this post
        country (str): Country of this post
    '''

    REGEX = re.compile(u'※ 發信站: 批踢踢實業坊|※ 文章網址:', re.UNICODE)
    IP_REGEX = re.compile(
        (r'※ 發信站: 批踢踢實業坊\(ptt.cc\), 來自: '
         r'(?P<ip>\d+\.\d+\.\d+\.\d+) \((?P<country>[^)]+)\)'),
        re.UNICODE
    )

    def __init__(self, tag: Tag) -> None:
        self._tag = tag

    @property
    def tag(self) -> Tag:
        return self._tag

    @property
    def author(self) -> str:
        return self.article_meta[0].text

    @property
    def title(self) -> str:
        return self.article_meta[2].text

    @property
    def date(self) -> str:
        return self.article_meta[3].text

    @property
    def contents(self) -> str:
        return self.tag.find(attrs={'id': 'main-content'}).text

    @property
    def body(self) -> str:
        if not hasattr(self, '_body'):
            start_m = re.search(self.date, self.contents)
            end_m = self.REGEX.search(self.contents)
            if start_m is None or end_m is None:
                raise ValueError('Not match')
            start, end = start_m.end(), end_m.start()
            self._body = self.contents[start:end-3]
        return self._body

    @property
    def ip(self) -> str:
        m = self.IP_REGEX.search(self.contents)
        if m is None:
            raise ValueError('Not match')
        return m.group('ip')

    @property
    def country(self) -> str:
        m = self.IP_REGEX.search(self.contents)
        if m is None:
            raise ValueError('Not match')
        return m.group('country')

    @property
    def article_meta(self) -> List[Tag]:
        return list(self.tag.find_all(attrs={'class': 'article-meta-value'}))

    @property
    def pushes(self) -> List[PttPush]:
        if not hasattr(self, '_pushes'):
            pushes = self.tag.find_all(attrs={'class': 'push'})
            self._pushes = [PttPush(p) for p in pushes]
        return self._pushes

    def __repr__(self) -> str:
        return self.title
