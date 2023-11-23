from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi

blocked_keyword_list = []
blocked_content_types = ['text/html', 'application/javascript', 'application/x-shockwave-flash', 'application/xml','application/x-www-form-urlencoded']

class XSS(SecurityBreak):
    def __init__(self):
        self.name = "Cross Site Scripting (XSS)"
        self.debugPrints = False
    
    def checkThreats(self, request: fastapi.Request, clientIp : str):
        """Check if the request contains XSS

        Args:
            request (fastapi.Request): the request to check (as recieved from client)
            clientIp (str): the ip of this request sender

        Returns:
            (Bool): true for threats found false for safe packet
        """
        
        #check the content type for not allowed content types
        if request.headers['Content-Type'].lower() in blocked_content_types:
            self.debugPrint('Content type is not allowed: ' + str(request.headers['Content-Type']))
            return True
        
        #check the data for xss
         
        
        return None
    
    def getName(self):
        return self.name
    
    def debugPrint(self, text : str):
        if self.debugPrint:
            print('[XSS debug] ' + text)
    