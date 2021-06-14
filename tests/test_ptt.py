import pytest
from ptt.parser import PttSpider, UnknownBoardError
from ptt.article import PttArticle


@pytest.mark.webreq
def test_connect():
    spider = PttSpider('Gossiping')
    assert spider.parse(1)


@pytest.mark.webreq
def test_raise_error():
    not_exist_board = 'QQ'
    with pytest.raises(UnknownBoardError) as e:
        PttSpider(not_exist_board)
    assert "Inaccessiable board" in str(e.value)


def test_spider(mock_spider):
    spider = PttSpider('QQ')
    posts = spider.parse(2)
    assert len(posts) == 2
    assert posts[0].author == 'oiyuz'
    assert posts[0].title == "[討論] 只有我覺得公鹿會過籃網嗎"
    assert posts[0].like == 'X1'
    assert posts[0].date == '6/12'


def test_article(article_tag):
    article = PttArticle(article_tag)
    assert 'oiyuz' in article.author
    assert '哈登的傷 對傷勢保密' in article.body
    assert article.country == "臺灣"
    assert len(article.pushes) == 159
    assert article.pushes[100].user == 'Mei5566'
    assert article.pushes[99].content == '鹿過網 這篇被挖出來當先知'
    assert article.pushes[98].push_tag == '→'
    assert article.pushes[97].time == '06/12 21:22'
