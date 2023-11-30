import requests

def test_sql_injection_detection(url):
    # Good request
    response = requests.get(url)
    print("Should work:", response.status_code, "| Content:", response.content)

    input("Press Enter to continue...")

    # SQL injection attempt in request body
    payload = "SELECT * FROM users; DROP TABLE users;"
    response = requests.post(url, data=payload)
    print("Should not work (SQL injection in request body):", response.status_code, "| Content:", response.content)

    input("Press Enter to continue...")

    # SQL injection attempt in URL parameters
    params = {'param': "'; DROP TABLE users; --"}
    response = requests.get(url, params=params)
    print("Should not work (SQL injection in URL parameters):", response.status_code, "| Content:", response.content)

    input("Press Enter to continue...")

    # SQL injection attempt in cookie
    headers = {'Cookie': "user_id=1'; DROP TABLE users; --"}
    response = requests.get(url, headers=headers)
    print("Should not work (SQL injection in cookie):", response.status_code, "| Content:", response.content)

    input("Press Enter to continue...")

    # SQL injection attempt with encoded payload
    payload = "SELECT%20*%20FROM%20users%3B%20DROP%20TABLE%20users%3B--"
    response = requests.post(url, data=payload)
    print("Should not work (Encoded SQL injection in request body):", response.status_code, "| Content:", response.content)

if __name__ == "__main__":
    
    test_sql_injection_detection("http://testwaf202.com")