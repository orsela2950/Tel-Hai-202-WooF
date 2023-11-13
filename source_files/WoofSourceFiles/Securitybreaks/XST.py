from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi


class XST(SecurityBreak):
    def __init__(self):
     self.name = "Cross Site Tracing (XST)"
    
    def checkThreats(request: fastapi.Request):
        return None
    
    def getName(self):
        return self.name