from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi

blocked_keyword_list = []
blocked_content_types = ['text/html', 'application/javascript', 'application/x-shockwave-flash', 'application/xml','application/x-www-form-urlencoded']

class XSS(SecurityBreak):
    def __init__(self):
        self.name = "Cross Site Scripting (XSS)"
        self.debugPrints = False
    
    def checkThreats(self, request: fastapi.Request, clientIp : str):
        return None
    
    def getName(self):
    
    def debugPrint(self, text : str):
        if self.debugPrint:
            print('[XSS debug] ' + text)
    