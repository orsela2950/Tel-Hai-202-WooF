import requests

import requests


def test_sql_injection(url, payload, description):
    try:
        response = requests.post(url, data=payload)
        print(f"{description} - Status Code: {response.status_code} | Content: {response.content}")
    except requests.RequestException as e:
        print(f"Error during {description} request: {e}")


if __name__ == "__main__":
    target_url = "http://testwaf202.com"  # Replace with your target URL

    # Good request
    response = requests.get(target_url)
    print("Good Request - Status Code:", response.status_code, "| Content:", response.content)

    input("Press Enter to continue...")

    # SQL injection attempt in request body
    payload = "SELECT * FROM users; DROP TABLE users;"
    test_sql_injection(target_url, payload, "SQL injection in request body")

    input("Press Enter to continue...")

    # SQL injection attempt in URL parameters
    params = {'param': "'; DROP TABLE users; --"}
    payload = f"{target_url}?{requests.compat.urlencode(params)}"
    test_sql_injection(payload, "", "SQL injection in URL parameters")

    input("Press Enter to continue...")

    # SQL injection attempt in cookie
    headers = {'Cookie': "user_id=1'; DROP TABLE users; --"}
    test_sql_injection(target_url, "", "SQL injection in cookie")

    input("Press Enter to continue...")

    # SQL injection attempt with encoded payload
    payload = "SELECT%20*%20FROM%20users%3B%20DROP%20TABLE%20users%3B--"
    test_sql_injection(target_url, payload, "Encoded SQL injection in request body")

    input("Press Enter to exit...")
