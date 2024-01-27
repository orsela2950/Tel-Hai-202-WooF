import requests
import urllib.parse


def is_request_hpp(request_url):
    parsed_url = urllib.parse.urlparse(request_url)
    params_dict = urllib.parse.parse_qs(parsed_url.query)

    for param_name, param_values in params_dict.items():
        if len(param_values) > 1:
            return True, f"{param_name}={param_values}"

    return False, None


# Example URL with HPP: multiple values for the 'name' parameter
url_with_hpp_direct = "http://testwaf202.com/path?name=a&name=b"
response = requests.get(url_with_hpp_direct)
hpp_detected, hpp_details = is_request_hpp(url_with_hpp_direct)
print(f"URL: {url_with_hpp_direct}")
print(f"Response Status Code: {response.status_code}")
print(f"HPP Detected: {hpp_detected}")
if hpp_detected:
    print(f"HPP Details: {hpp_details}")
print("Response Content:")
print(response.content.decode('utf-8'))
input("Press Enter to continue...")

# Example URL with HPP encoded in the 'name' parameter
url_with_hpp_encoded = "http://testwaf202.com/path?name=a%26name%3Db"
response = requests.get(url_with_hpp_encoded)
hpp_detected, hpp_details = is_request_hpp(url_with_hpp_encoded)
print(f"URL: {url_with_hpp_encoded}")
print(f"Response Status Code: {response.status_code}")
print(f"HPP Detected: {hpp_detected}")
if hpp_detected:
    print(f"HPP Details: {hpp_details}")
print("Response Content:")
print(response.content.decode('utf-8'))
input("Press Enter to continue...")

# Example URL without HPP
url_without_hpp = "http://testwaf202.com/path?name=single_value"
response = requests.get(url_without_hpp)
hpp_detected, hpp_details = is_request_hpp(url_without_hpp)
print(f"URL: {url_without_hpp}")
print(f"Response Status Code: {response.status_code}")
print(f"HPP Detected: {hpp_detected}")
if hpp_detected:
    print(f"HPP Details: {hpp_details}")
print("Response Content:")
print(response.content.decode('utf-8'))
input("Press Enter to exit...")
