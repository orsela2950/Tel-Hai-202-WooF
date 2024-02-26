from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi
import os

blocked_content_types = ['text/html', 'application/javascript', 'application/x-shockwave-flash', 'application/xml',
                         'application/x-www-form-urlencoded']

# load the word list:
# File usage:
xss_malicious_list_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'XSS_Malicious.txt')
with open(xss_malicious_list_path, 'r') as f:
    blocked_keyword_list = f.readlines()
    f.close()


class XSS(SecurityBreak):
    def __init__(self):
        super().__init__()  # Call parent's constructor
        self.name = "Cross Site Scripting (XSS)"
        self.debug_prints = False

    async def check_threats(self, request: fastapi.Request, clientIp: str):
        """Check if the request contains XSS Attack

        Args:
            request (fastapi.Request): the request to check (as recieved from client)
            clientIp (str): the ip of this request sender

        Returns:
            (Bool, str): true for threats found false for safe packet, a summary of the found attack if found or none
        """

        # check the content type for not allowed content types
        if ('Content-Type' in request.headers.keys()) and (
                request.headers['Content-Type'].lower() in blocked_content_types):
            self.debug_print('Content type is not allowed: ' + str(request.headers['Content-Type']))
            return True, 'Content type : ' + str(request.headers['Content-Type'])

        for param_name, param_value in request.query_params.items():
            if True in (word in param_value for word in blocked_keyword_list):
                self.debug_print('blocked a packet because it cannot contain "' + param_value + '"')
                return True, 'The packet cant contain "' + param_value + '"'

        return False, None

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
