from pathlib import Path
from functools import partial
from bs4 import BeautifulSoup
from ptt.parser import PttSpider
import pytest


@pytest.fixture
def data_dir():
    return Path(__file__).resolve().parent / 'data'


@pytest.fixture
def mock_spider(data_dir, monkeypatch):
    def mock_get_soup(content, *args, **kwargs):
        return BeautifulSoup(content, 'html.parser')
    rq_content = (data_dir/'nba_index.txt').read_text()
    mock_get_nba_soup = partial(mock_get_soup, rq_content)
    monkeypatch.setattr(PttSpider, '_get_soup', mock_get_nba_soup)


@pytest.fixture
def article_tag(data_dir):
    rq_content = (data_dir/'article.txt').read_text()
    return BeautifulSoup(rq_content, 'html.parser')
