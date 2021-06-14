# pttpost-parser

Pttpost-parser is a Python library for collecting articles from [ptt website](https://www.ptt.cc/bbs/index.html).


## Features
- Asynchronus request
- Detailed information
- Author, recommend, keyword search


## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install this pacakage.
```bash
pip install -r requirement.txt
```


## Usage
Collect posts from the specific board with keyword search.
```python
from ptt.parser import PttSpider, PostReader

spider = PttSpider('NBA')
posts = spider.parse(3, keyword='Kobe', recommend=60)
for post in posts:
    print(f'[{post.like}] {post.title} -{post.author}')
```

Get detail information from a post.
```python
reader = PostReader()

article = reader.read(posts[0])
print(f'Title: {article.title}')
print(f'{article.body}')

```

Read mutiple posts
```python
articles = reader.read_posts(posts)
for article in articles:
    print('-'*100)
    print(f'Title: {article.title}')
    print(f'{article.body}')
```

Get pushes contents from the article.
```python
pushes = article.pushes
for push in pushes[:10]:
    print(f"{push.push_tag} {push.content}-{push.user}")
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License
[MIT](https://choosealicense.com/licenses/mit/)