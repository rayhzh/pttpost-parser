from ptt.article import PttArticle
from . import parser as pttparser
from tabulate import tabulate
from tqdm import tqdm
from pathlib import Path
from typing import Dict


class PostDownloader:
    """PttDownloader
    """

    def __init__(self, board: str) -> None:
        self.board = board
        self.spider = pttparser.PttSpider(board)

    def download(self, post_num: int, **kwargs) -> None:
        posts = self.spider.parse(post_num, **kwargs)
        reader = pttparser.PostReader()
        dir_name = self._get_dir_name(kwargs)
        dir_p = Path('download') / dir_name
        dir_p.mkdir(parents=True, exist_ok=True)
        self._show_tab(dir_p, **kwargs)
        with tqdm(total=len(posts), desc='Downloading') as pbar:
            for i in range(len(posts)//20+1):
                articles = reader.read_posts(posts[(i)*20:(i+1)*20])
                for article in articles:
                    try:
                        self._write_file(article, dir_p)
                    except Exception:
                        pass
                pbar.update(20)

                

    def _write_file(self, article: PttArticle, dir_p: Path) -> None:
        file_name = f"{article.title}_{article.author}.txt"
        file_name = file_name.replace('/', '.')
        post_p = dir_p / file_name
        try:
            post_p.write_text(article.contents)
        except OSError:
            post_p = dir_p / f"{article.title.replace('/', '.')}_?????"
            post_p.write_text(article.contents)

    def _show_tab(self, dir_p: Path, **kwargs) -> None:
        arg_dict = {
            'keyword': kwargs.get('keyword', 'None'),
            'author': kwargs.get('author', 'None'),
            'recommend': kwargs.get('recommend', 'None')
        }
        print(tabulate(list(arg_dict.items()), headers=['argument key', 'value']))
        print('-'*50)
        print('download path:', './'+str(dir_p))


    def _get_dir_name(self, arg_dict: Dict[str, str]) -> str:
        name = self.board
        if arg_dict.get('keyword'):
            name += f"_key_{arg_dict['keyword']}"
        if arg_dict.get('author'):
            name += f"_author_{arg_dict['author']}"
        if arg_dict.get('recommend'):
            name += f"_recommend_{arg_dict['recommend']}"
        return name