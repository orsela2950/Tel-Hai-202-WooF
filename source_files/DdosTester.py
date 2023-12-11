import requests
import time


def send_request(payload):
    ans = requests.post("http://testwaf202.com", json=payload)
    print("Status Code:", ans.status_code, "| Content:", ans.content)

# Send 10 similar requests
for i in range(10):
    payload = {"key": "value"}
    send_request(payload)
    


# Send a different request
different_payload = {"key": "modified_value"}
send_request(different_payload)


# Now send a request to trigger the cleanup process
cleanup_payload = {"cleanup": True}
send_request(cleanup_payload)