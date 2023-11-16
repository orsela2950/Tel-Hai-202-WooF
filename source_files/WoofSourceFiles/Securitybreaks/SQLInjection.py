from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi


class SQLInjection(SecurityBreak):
    def __init__(self):
     self.name = "SQL Injection"
    
    def checkThreats(self, request: fastapi.Request, clientIp : str):
        return None
    
    def getName(self):
        return self.name