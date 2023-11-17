from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi
import urllib.parse


class HPP(SecurityBreak):
    def __init__(self):
     self.name = "HTTP Parameter Pollution"
    
    def checkThreats(self, request: fastapi.Request, clientIp : str):
        return None
    
    def getName(self):
        return self.name