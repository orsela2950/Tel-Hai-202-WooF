import requests


#in order for this to work youll need this line in the hosts file:
#127.0.0.1 testwaf202.com
ans = requests.get("http://testwaf202.com")
print("should work: " + str(ans.status_code) + " | content: " +str(ans.content))
input()

payload = "faedsfaseff</progress>gkselgegh"
headers = {"Content-Type": "text/plain"}
ans = requests.post("http://testwaf202.com", data=payload, headers=headers)
print("should not work: " + str(ans.status_code) + " | content: " +str(ans.content))
input()

jsData = {
    "payload" : '</progress>',
    "another" : "</progress>"}
ans = requests.post("http://testwaf202.com:8000", data = jsData)
print("should not work: " + str(ans.status_code) + " | content: " +str(ans.content))
input()


