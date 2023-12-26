from Securitybreaks.SecurityBreak import SecurityBreak
import urllib.parse
from typing import Tuple
import fastapi

class OpenRedirect(SecurityBreak):
    def __init__(self):
     self.name = "Open Redirect Vulnerability"
    
    async def checkThreats(self, request: fastapi.Request, clientIp: str) -> Tuple[bool, str]:
        with open('Securitybreaks/allowed_urls.txt', 'r') as f:
            allowed_urls = f.readlines()
            f.close()

        redirect_params = ["url", "uri", "path", "next", "go", "data", "view", "page", "location", "return", "redir", "redirect", "redirect_uri", "redirect_url","redirect_cookie","redirect_param"] 

        # Parse the URL:
        parsed_url = urllib.parse.urlparse(str(request.url))

        # Get the parameters as a dictionary
        request_data = urllib.parse.parse_qs(parsed_url.query)
        request_data.update(dict(request.headers))

        for redirect_param in redirect_params:
            if (redirect_param in request_data):
                # Check if url to enter is from allowed urls:
                url_enter = request_data[redirect_param]
                if url_enter not in allowed_urls:
                    return (True, f"{redirect_param}={url_enter}")
            for value in request_data.values():
                if (redirect_param in value):
                    return (True, f"{redirect_param}={value}")
                

        return (False, None)
    
    def getName(self):
        return self.name