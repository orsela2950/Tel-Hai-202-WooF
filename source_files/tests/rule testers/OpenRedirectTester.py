import requests


def test_open_redirect_detection(url):
    # Good request
    response = requests.get(url)
    print("Should work:", response.status_code, "| Content:", response.content)

    input("Press Enter to continue...")

    # Open redirect attempt in URL parameters
    params = {'redirect_param': "http://malicious-website.com"}
    response = requests.get(url, params=params)
    print("Should not work (Open redirect in URL parameters):", response.status_code, "| Content:", response.content)

    input("Press Enter to continue...")

    # Open redirect attempt in cookie
    headers = {'Cookie': f"redirect_cookie=http://malicious-website.com; other_cookie=value"}
    response = requests.get(url, headers=headers)
    print("Should not work (Open redirect in cookie):", response.status_code, "| Content:", response.content)


if __name__ == "__main__":
    test_open_redirect_detection("http://testwaf202.com")
