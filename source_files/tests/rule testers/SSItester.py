import requests

# in order for this to work you'll need this line in the hosts file:
# 127.0.0.1 testwaf202.com
ans = requests.get("http://testwaf202.com")
print("should work: " + str(ans.status_code) + " | content: " + str(ans.content))
input()

# SSI Injection payload
ssi_payload = "<!--#exec cmd='ls' -->"
ans = requests.post("http://testwaf202.com", data={"param_name": ssi_payload})
print("should not work: " + str(ans.status_code) + " | content: " + str(ans.content))
input()

# Another SSI Injection payload
ssi_payload2 = "<!--#include file='/etc/passwd' -->"
ans = requests.post("http://testwaf202.com", data={"param_name": ssi_payload2})
print("should not work: " + str(ans.status_code) + " | content: " + str(ans.content))
input()
