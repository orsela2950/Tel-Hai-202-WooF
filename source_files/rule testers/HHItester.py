import requests

#in order for this to work youll need this line in the hosts file:
#127.0.0.1 testwaf202.com
ans = requests.get("http://testwaf202.com/")
print("ans: " + str(ans.status_code) + " | content: " +str(ans.content))
input()

ans = requests.get("http://127.0.0.1")
print("ans: " + str(ans.status_code) + " | content: " +str(ans.content))
input()

headers = {'Host': '\\n',}
ans = requests.get("http://testwaf202.com/", headers=headers)
print("ans: " + str(ans.status_code) + " | content: " +str(ans.content))
input()

headers = {'Host': 'http://testwaf202.com/',
           'X-Host': 'somthing'}
ans = requests.get("http://testwaf202.com/", headers=headers)
print("ans: " + str(ans.status_code) + " | content: " +str(ans.content))
input()

