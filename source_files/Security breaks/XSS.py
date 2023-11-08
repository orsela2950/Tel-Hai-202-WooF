import SecurityBreak
import fastapi


class XSS(SecurityBreak):
    def __init__(self):
     self.name = "Cross Site Scripting (XSS)"
    
    def checkThreats(request: fastapi.Request):
        pass
    
    def getName(self):
        return self.name
