import SecurityBreak
import fastapi


class HPP(SecurityBreak):
    def __init__(self):
     self.name = "HTTP Parameter Pollution"
    
    def checkThreats(request: fastapi.Request):
        pass
    
    def getName(self):
        return self.name