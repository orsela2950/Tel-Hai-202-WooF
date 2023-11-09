import SecurityBreak
import fastapi


class SQLInjection(SecurityBreak):
    def __init__(self):
     self.name = "SQL Injection"
    
    def checkThreats(request: fastapi.Request):
        pass
    
    def getName(self):
        return self.name