from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi


class HostHeaderInjection(SecurityBreak):
    def __init__(self):
     self.name = "HTTP Host Header Injection"
    
    def checkThreats(request: fastapi.Request):
        return None
    
    def getName(self):
        return self.name