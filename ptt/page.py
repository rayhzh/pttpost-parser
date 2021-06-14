import re
from .type import Url
from typing import Iterator, List
import urllib.parse as urlpasre
from abc import ABC, abstractmethod


class PageManager(ABC):

    def __init__(self, start_url: Url) -> None:
        self.start_url = start_url

    @abstractmethod
    def get_urls(self, search_page_num: int, **kwargs) -> Iterator[Url]:
        pass


class DefaultPage(PageManager):

    def set_page_indx(self, indx: int) -> None:
        self._page_indx = indx

    def get_page_indx(self) -> int:
        return self._page_indx

    def get_url(self, indx: int) -> Url:
        url = re.sub(r'index.html', f'index{indx}.html', self.start_url)
        return Url(url)

    def get_urls(
        self,
        search_page_num: int,
        **kwargs
    ) -> Iterator[Url]:
        first_indx = self.get_page_indx()
        for indx in range(first_indx, first_indx-search_page_num, -1):
            yield self.get_url(indx)


class SearchPage(PageManager):

    def get_url(self, indx: int, **kwargs) -> Url:
        body_list: List[str] = []
        for key in kwargs:
            if key == 'author':
                body_list.append(f"author:{kwargs[key]}")
            elif key == 'keyword':
                body_list.append(kwargs[key])
            elif key == 'recommend':
                # Search string effects the search results
                body_list.insert(0, f"recommend:{kwargs[key]}")
        search_url = urlpasre.urljoin(self.start_url, 'search')
        url_parse = urlpasre.urlparse(search_url)
        url_query = urlpasre.urlencode({
            'page': str(indx),
            'q': "\\+".join(body_list)
        })
        url = url_parse._replace(query=url_query).geturl()
        return Url(url.replace('%5C%2B', '+'))

    def get_urls(
        self,
        search_page_num: int,
        **kwargs
    ) -> Iterator[Url]:
        for indx in range(1, search_page_num+1):
            yield self.get_url(indx, **kwargs)
