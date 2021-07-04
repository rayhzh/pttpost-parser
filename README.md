# pttpost-parser
Python爬蟲練習，用asyncio + requests + BeautifulSoup快速擷取Ptt文章資訊 (ex: 作者、內容、詳細推文內容、IP)。支援關鍵字、推文數、作者搜尋

## Features
- Asynchronus request
- Detailed information
- Author, recommend, keyword search


## Installation
Git clone下來後，用pip安裝需要的libaray
```bash
pip install .
```

## Example
在安裝完後可以用 `python ./example/post_downloader.py` 來下載ptt文章,預設搜尋條件為八卦版的50篇文章,以下為範例:
![image](https://user-images.githubusercontent.com/28876380/124393835-001c7b00-dd2f-11eb-89d6-8f5b71ad5bfa.png)
執行後在./download可以看到下載的檔案

如果想要要搜尋特定的看板(ex: -board nba), 設定作者(ex: -author RoseC), 標題關鍵字, 推文數等等：
可以下 `python ./example/post_downloader.py -h`看用法
![image](https://user-images.githubusercontent.com/28876380/124393995-e2034a80-dd2f-11eb-8eb6-27c7d2432ea3.png)

以下為範例：`python ./examples/post_downloader.py -board nba -author RoseC -like 50`
![image](https://user-images.githubusercontent.com/28876380/124394023-03643680-dd30-11eb-9103-ff658776f7c1.png)
執行完後可以去 ./download/nba_author_RoseC_like_50 看所有的文章了

## Usage
在`PttSpider`裡面要給一個"PTT board" argument，之後就能call `parse`搜尋貼文了，`parse` 有三個option可以用，分別是
1. keyword: 標題關鍵字
2. recommend: 推文數 ex: 10, 90, -10
3. author: 作者名稱

三種搜尋方式可以混用。
`parse`搜尋完後，會回傳`PttPost`的List。
```python
from ptt.parser import PttSpider, PostReader

spider = PttSpider('NBA')
posts = spider.parse(3, keyword='Kobe', recommend=60)
for post in posts:
    print(f'[{post.like}] {post.title} -{post.author}')
```

如果想要`PttPost`的詳細資訊，可以用`PostReader`，拿到文章的詳細資訊，以及推文資訊。
```python
reader = PostReader()

article = reader.read(posts[0])
print(f'Title: {article.title}')
print(f'{article.body}')

```

文章推文的詳細資訊。
```python
pushes = article.pushes
for push in pushes[:10]:
    print(f"{push.push_tag} {push.content}-{push.user}")
```


如果想要一次拿到多個`PttPost`的詳細資訊，可以用`read_posts`，應用asynchronous http request可以加速資料擷取。
```python
articles = reader.read_posts(posts)
for article in articles:
    print('-'*100)
    print(f'Title: {article.title}')
    print(f'{article.body}')
```



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License
[MIT](https://choosealicense.com/licenses/mit/)
