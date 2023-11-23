from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi


class XST(SecurityBreak):
    def __init__(self):
     self.name = "Cross Site Tracing (XST)"
    
    def checkThreats(self, request: fastapi.Request, clientIp : str):
        return False,None
    
    def getName(self):
        return self.name