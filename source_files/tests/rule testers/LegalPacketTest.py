import requests
import time


def send_request(url, method="GET", headers=None, params=None, data=None, json=None):
    time.sleep(2)  # Wait for 2 seconds

    # Define the request parameters
    request_params = {
        "url": url,
        "method": method,
        "headers": headers,
        "params": params,
        "data": data,
        "json": json
    }

    # Send the request
    ans = requests.request(**request_params)

    # Print the response details
    print(f"Request sent to {url} | Method: {method} | Status Code: {ans.status_code} | Content: {ans.content}")


# Example legal packet payloads
get_payload = {"key": "value"}
post_payload = {"key": "value", "another_key": "another_value"}

# Example headers
headers = {
    "User-Agent": "MyApp/1.0",
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}

# Example URL parameters
params = {
    "param1": "value1",
    "param2": "value2"
}

# Send different legal requests with different configurations
send_request("http://testwaf202.com", method="GET", params=params, headers=headers, json=get_payload)
send_request("http://testwaf202.com", method="POST", data=post_payload, headers=headers, params=params)
