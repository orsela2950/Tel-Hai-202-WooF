from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi
from typing import Tuple
import os

blocked_content_types = ['text/html', 'application/javascript', 'application/x-shockwave-flash', 'application/xml',
                         'application/x-www-form-urlencoded']

# load the word list:
# File usage:
xss_malicious_list_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'XSS_Malicious.txt')
with open(xss_malicious_list_path, 'r') as f:
    file_list = f.readlines()
    blocked_keyword_list = [(word.replace('\n', '')) for word in file_list]
    f.close()


class XSS(SecurityBreak):
    def __init__(self):
        super().__init__()  # Call parent's constructor
        self.name = "Cross Site Scripting (XSS)"
        self.debug_prints = False

    async def check_threats(self, request: fastapi.Request, clientIp: str) -> Tuple[bool, str]:
        """Check if the request contains XSS Attack

        Args:
            request (fastapi.Request): the request to check (as received from the client)
            clientIp (str): the IP of this request sender

        Returns:
            (Bool, str): true for threats found false for safe packet, a summary of the found attack if found or none
        """
        print(blocked_keyword_list)

        # Check the content type for not allowed content types
        if ('Content-Type' in request.headers.keys()) and (
                request.headers['content-type'].lower() in blocked_content_types):
            self.debug_print('Content type is not allowed: ' + str(request.headers['content-type']))
            return True, 'Content type : ' + str(request.headers['content-type'])

        # Check query parameters for blocked keywords
        for param_name, param_value in request.query_params.items():
            if True in (word in param_value for word in blocked_keyword_list):
                self.debug_print('Blocked a packet because it cannot contain "' + param_value + '"')
                return True, 'The packet can\'t contain "' + param_value + '"'

        # Check request body for XSS
        body = await request.body()
        print(str(body))
        word_in_body_list = [word for word in blocked_keyword_list if word in str(body)]
        if word_in_body_list:
            self.debug_print('Blocked a packet because it contains XSS in the body')
            return True, f'The packet contains XSS param "{word_in_body_list}" in the body'

        return False, ""

    def InPacket(self, request: fastapi.Request, word: str):
        """checks if a word/phrase is in the packet

        Args:
            request (fastapi.Request): the packet
            word (str): the string

        Returns:
            (Bool): weather the word is in the packet or not
        """
        for header in request.headers:
            if word in request.headers[header]:
                return True

        if word in request.body:
            return True

        return False

    def get_name(self):
        return self.name

    def get_json_name(self):  # json type name, and not the name for displaying
        return 'XSS'

    def debug_print(self, text: str):
        if self.debug_prints:
            print('[XSS debug] ' + text)
