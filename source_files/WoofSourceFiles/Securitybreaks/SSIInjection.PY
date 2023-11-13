from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi


class SSIInjection(SecurityBreak):
    def __init__(self):
     self.name = "SSI Injection"
    
    def checkThreats(request: fastapi.Request):
        return None
    
    def getName(self):
        return self.name