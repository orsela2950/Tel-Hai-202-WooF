from Securitybreaks.SecurityBreak import SecurityBreak
from urllib.parse import urlparse, urlunparse, parse_qs, urlunsplit
import fastapi
import os

allowed_urls_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'allowed_urls.txt')
with open(allowed_urls_path, 'r') as f:
    allowed_urls = f.readlines()
    allowed_urls_list = [url.replace('\n', '') for url in allowed_urls]


def remove_url_parameters(request_url):
    parsed_url = urlparse(str(request_url))

    # Extract scheme, netloc, path, params, query, fragment
    scheme, netloc, path, params, query, fragment = parsed_url

    # Reconstruct the URL without query parameters
    new_url = urlunparse((scheme, netloc, path, '', '', ''))

    return new_url


class OpenRedirect(SecurityBreak):
    def __init__(self):
        super().__init__()  # Call parent's constructor
        self.name = "Open Redirect Vulnerability"

    async def check_threats(self, request: fastapi.Request, clientIp: str) -> tuple[bool, str] | tuple[bool, None]:
        """

        @param request:
        @param clientIp:
        @return:
        """

        redirect_params = ["url", "uri", "path", "next", "go", "data", "view", "page", "location", "return", "redir",
                           "redirect", "redirect_uri", "redirect_url", "redirect_cookie", "redirect_param"]

        # Parse the URL:
        parsed_url = urlparse(str(request.url))

        # Get the parameters as a dictionary
        request_data = parse_qs(parsed_url.query)
        request_data.update(dict(request.headers))

        # Check if one of the requet's parameters is redirect parameter:
        for redirect_param in redirect_params:
            if redirect_param in request_data.keys():

                # Check if url to enter is from allowed urls:
                url_to_enter = remove_url_parameters(request_data[redirect_param])
                if url_to_enter not in allowed_urls:
                    return True, f"{redirect_param}={url_to_enter}"

        return False, None

    def get_name(self):
        return self.name

    def get_json_name(self):  # json type name, and not the name for displaying
        return 'OpenRedirect'
