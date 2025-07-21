import requests
from bs4 import BeautifulSoup

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',  
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',  
    'cache-control': 'no-cache',  
    'dnt': '1',  
    'pragma': 'no-cache',  
    'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',  
    'sec-ch-ua-mobile': '?0',  
    'sec-ch-ua-platform': '"macOS"',  
    'sec-fetch-dest': 'document',  
    'sec-fetch-mode': 'navigate',  
    'sec-fetch-site': 'same-origin',  
    'sec-fetch-user': '?1',  
    'upgrade-insecure-requests': '1',  
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46',
}

page = requests.get("https://www.goodreads.com/list/show/2681",headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

titles = soup.select(".tablelist tbody tr[itemtype='http://schema.org/Book'] td a.bookTitle span[itemprop=\"name\"]")

top10 = titles[:10]

print(top10)
print(page)