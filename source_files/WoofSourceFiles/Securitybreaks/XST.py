import SecurityBreak
import fastapi


class XST(SecurityBreak):
    def __init__(self):
     self.name = "Cross Site Tracing (XST)"
    
    def checkThreats(request: fastapi.Request):
        pass
    
    def getName(self):
        return self.name