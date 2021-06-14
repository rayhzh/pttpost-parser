from ptt.parser import (
    PttSpider,
    PostReader
)


def main():
    spider = PttSpider('NBA')
    posts = spider.parse(3, keyword='Kobe', recommend=60)
    for post in posts:
        print(f'[{post.like}] {post.title} -{post.author}')
    reader = PostReader()
    article = reader.read(posts[0])
    print(f'Title: {article.title}')
    print(f'{article.body}')


if __name__ == '__main__':
    main()
