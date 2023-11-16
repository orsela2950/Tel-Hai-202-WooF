from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi


class OpenRedirect(SecurityBreak):
    def __init__(self):
     self.name = "Open Redirect Vulnerability"
    
    def checkThreats(self, request: fastapi.Request, clientIp : str):
        return None
    
    def getName(self):
        return self.name