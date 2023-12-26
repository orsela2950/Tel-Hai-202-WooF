from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi
from urllib.parse import parse_qs

blocked_keyword_list = []
blocked_content_types = ['text/html', 'application/javascript', 'application/x-shockwave-flash', 'application/xml','application/x-www-form-urlencoded']

#load the word list:
with open('Securitybreaks\XSS_Malicious.txt', 'r') as f:
    blocked_keyword_list = f.readlines()
    f.close()
class XSS(SecurityBreak):
    def __init__(self):
        self.name = "Cross Site Scripting (XSS)"
        self.debugPrints = False
    
    async def checkThreats(self, request: fastapi.Request, clientIp : str):
        """Check if the request contains XSS Attack

        Args:
            request (fastapi.Request): the request to check (as recieved from client)
            clientIp (str): the ip of this request sender

        Returns:
            (Bool, str): true for threats found false for safe packet, a summary of the found attack if found or none
        """
        
        #check the content type for not allowed content types
        if ('Content-Type' in request.headers.keys()) and (request.headers['Content-Type'].lower() in blocked_content_types):
            self.debugPrint('Content type is not allowed: ' + str(request.headers['Content-Type']))
            return True, 'Content type : ' + str(request.headers['Content-Type'])
        
        for param_name, param_value in request.query_params.items():
            if True in (word in param_value for word in blocked_keyword_list):
                self.debugPrint('blocked a packet because it cannot contain "' +param_value+ '"')
                return True, 'The packet cant contain "'+param_value+'"'
             
        return False, None
    
    def InPacket(self, request :fastapi.Request, word :str):
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
    
    def getName(self):
        return self.name
    
    def debugPrint(self, text :str):
        if self.debugPrint:
            print('[XSS debug] ' + text)
    