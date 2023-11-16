from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi


class HostHeaderInjection(SecurityBreak):
    def __init__(self):
     self.name = "HTTP Host Header Injection"
    
    def checkThreats(self, request: fastapi.Request, clientIp : str):
        print("===============================================================================")
        print("===============================================================================")
        print(request)
        print(clientIp)
        print("===============================================================================")
        print("===============================================================================")
        return None
    
    def getName(self):
        return self.name