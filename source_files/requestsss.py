import requests

headers = {'host': 'http://testwaf202.com', 'connection': 'keep-alive', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36', 'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8', 'referer': 'http://testwaf202.com:8000/', 'accept-encoding': 'gzip, deflate', 'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7,uz;q=0.6', 'X-Forwarded-For': '127.0.0.1'}
response = requests.request(
    method='GET',
    url='http://127.0.0.1:80',
)

print(response.content.decode())