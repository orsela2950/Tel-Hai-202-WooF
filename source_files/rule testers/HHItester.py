import requests

#in order for this to work youll need this line in the hosts file:
#127.0.0.1 testwaf202.com
ans = requests.get("http://testwaf202.com")
print("should work: " + str(ans.status_code) + " | content: " +str(ans.content))
input()

#normal request but with manual host header that contains the http scheme
headers = {'Host': 'http://testwaf202.com',}
ans = requests.get("http://127.0.0.1", headers=headers)
print("should work: " + str(ans.status_code) + " | content: " +str(ans.content))
input()

#bad request that dont have the correct host header
ans = requests.get("http://127.0.0.1")
print("should not work: " + str(ans.status_code) + " | content: " +str(ans.content))
input()

headers = {'Host': '\\n',}
ans = requests.get("http://testwaf202.com", headers=headers)
print("should not work: " + str(ans.status_code) + " | content: " +str(ans.content))
input()

headers = {'Host': '',}
ans = requests.get("http://testwaf202.com", headers=headers)
print("should not work: " + str(ans.status_code) + " | content: " +str(ans.content))
input()

headers = {'Host': 'http://testwaf202.com', 'X-Host': 'somthing'}
ans = requests.get("http://testwaf202.com", headers=headers)
print("should not work: " + str(ans.status_code) + " | content: " +str(ans.content))
