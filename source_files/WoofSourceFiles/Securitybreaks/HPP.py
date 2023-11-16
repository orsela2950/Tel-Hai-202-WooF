from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi


class HPP(SecurityBreak):
    def __init__(self):
     self.name = "HTTP Parameter Pollution"
    
    def checkThreats(self, request: fastapi.Request, clientIp : str):
        return None
    
    def getName(self):
        return self.name