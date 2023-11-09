import SecurityBreak
import fastapi


class OpenRedirect(SecurityBreak):
    def __init__(self):
     self.name = "Open Redirect Vulnerability"
    
    def checkThreats(request: fastapi.Request):
        pass
    
    def getName(self):
        return self.name