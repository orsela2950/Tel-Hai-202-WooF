import requests
import re
from time import time

def test_proxy_xss(proxy_url):
    """Tests a proxy server for cross-site scripting (XSS) vulnerabilities.

    Args:
        proxy_url: The URL of the proxy server.

    Returns:
        True if the proxy server is vulnerable to XSS, False otherwise.
    """

    xss_payload = "<script>alert('XSS')</script>"
    response = requests.get("https://www.google.com", proxies={"http": proxy_url}, params={"q": xss_payload}, headers={"Host": "www.google.com"})

    # Decode the response content from bytes to a string before searching for the payload.
    response_content = response.content.decode()

    if re.search(xss_payload, response_content):
        return True
    else:
        return False
    

def test_proxy_sql_injection(proxy_url):
    """Tests a proxy server for SQL injection vulnerabilities.

    Args:
        proxy_url: The URL of the proxy server.

    Returns:
        True if the proxy server is vulnerable to SQL injection, False otherwise.
    """

    sql_injection_payload = "' OR 1=1 --"
    response = requests.get("https://www.google.com", proxies={"http": proxy_url}, params={"q": sql_injection_payload}, headers={"Host": "www.google.com"})

    # Decode the response content from bytes to a string before searching for the payload.
    response_content = response.content.decode()

    if re.search(sql_injection_payload, response_content):
        return True
    else:
        return False
    
def test_proxy_slowloris(proxy_url):
    """Tests a proxy server for Slowloris attacks.

    Args:
        proxy_url: The URL of the proxy server.

    Returns:
        True if the proxy server is vulnerable to Slowloris attacks, False otherwise.
    """

    start_time = time()
    response = requests.get("https://www.google.com", proxies={"http": proxy_url}, headers={"Host": "www.google.com"})
    end_time = time()

    # If the response time is greater than 10 seconds, then the proxy server is likely vulnerable to Slowloris attacks.
    if end_time - start_time > 10:
        return True
    else:
        return False
    
def test_proxy(proxy_url):
    """Tests a proxy server for XSS, SQL injection, and Slowloris attacks.

    Args:
        proxy_url: The URL of the proxy server.

    Returns:
        A list of vulnerabilities found, or an empty list if no vulnerabilities were found.
    """

    vulnerabilities = []

    if test_proxy_xss(proxy_url):
        vulnerabilities.append("XSS")

    if test_proxy_sql_injection(proxy_url):
        vulnerabilities.append("SQL Injection")

    if test_proxy_slowloris(proxy_url):
        vulnerabilities.append("Slowloris")

    return vulnerabilities

if __name__ == "__main__":
    proxy_url = "https:://127.0.0.1:8000"

    vulnerabilities = test_proxy(proxy_url)

    if vulnerabilities:
        print("The proxy server is vulnerable to the following attacks:")
        for vulnerability in vulnerabilities:
            print(vulnerability)
    else:
        print("The proxy server does not appear to be vulnerable to the attacks tested.")