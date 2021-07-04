from ptt import parser as pttparser
import argparse
import timeit
from tabulate import tabulate
from pathlib import Path

def _get_dir_name(args) -> str:
    name = args.board
    if args.keyword:
        name += f"_key_{args.keyword}"
    if args.author:
        name += f"_author_{args.author}"
    if args.recommend:
        name += f"_like_{args.recommend}"
    return name


def main(args):
    spider = pttparser.PttSpider(args.board)
    args_dict = vars(args)
    print(tabulate(list(args_dict.items()), headers=['argument key', 'value']))
    post_num = args_dict.pop('post_num')
    kwargs = {k:v for k, v in args_dict.items() if v is not None}
    posts = spider.parse(post_num, **kwargs)
    print('parsing ....')
    reader = pttparser.PostReader()
    print('dumping ...')
    dir_name = _get_dir_name(args)
    dir_p = Path('download') / dir_name
    dir_p.mkdir(parents=True, exist_ok=True)
    articles = reader.read_posts(posts)
    for article in articles:
        file_name = f"{article.title}_{article.author}.txt"
        file_name = file_name.replace('/', '.')
        post_p = dir_p / file_name
        try:
            post_p.write_text(article.contents)
        except OSError:
            post_p = dir_p / f"{article.title.replace('/', '.')}_?????"
            post_p.write_text(article.contents)
    print('Please refer to', dir_p.name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-board", dest="board", help="你想搜尋的看板", default="gossiping")
    parser.add_argument("-num", dest="post_num", help="文章數", type=int, default=50)
    parser.add_argument("-keyword", dest="keyword", help="標題關鍵字", default=None)
    parser.add_argument("-author", dest="author", help="搜尋作者", default=None)
    parser.add_argument("-like", dest="recommend", help="推數 (ex: 10, 99, -99)", default=None)
    args = parser.parse_args()
    start = timeit.default_timer()
    main(args)
    print('Runtime:', timeit.default_timer() - start)