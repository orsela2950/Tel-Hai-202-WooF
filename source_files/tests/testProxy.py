import requests

# Replace with the URL of your proxy server
proxy_server_url = "http://127.0.0.1:80"

# Test payloads with different attack patterns
test_payloads = [
    "favicon.ico",
    "<script>alert('XSS attack')</script>",
    "SELECT * FROM users",
    "UNION ALL SELECT null, null, null, null, null, null, null, null, null, null",
]

def test_proxy_server():
    for payload in test_payloads:
        response = send_test_request(payload)
        if "Malicious request detected" in response.text:
            print(f"Test for payload '{payload}' - Blocked: Proxy server detected the attack")
        else:
            print(f"Test for payload '{payload}' - Passed: Proxy server allowed the request")

def send_test_request(payload):
    headers = {"Host": "127.0.0.1"}  # Replace with a valid host
    url = f"{proxy_server_url}/{payload}"
    response = requests.get(url, headers=headers)
    return response

if __name__ == "__main__":
    test_proxy_server()