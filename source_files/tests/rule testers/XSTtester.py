import requests

# in order for this to work, you'll need this line in the hosts file:
# 127.0.0.1 testwaf202.com
ans = requests.get("http://testwaf202.com")
print("should work: " + str(ans.status_code) + " | content: " + str(ans.content))
input()

# XST payload using TRACE method
ans = requests.request("TRACE", "http://testwaf202.com")
print("should not work: " + str(ans.status_code) + " | content: " + str(ans.content))
input()
