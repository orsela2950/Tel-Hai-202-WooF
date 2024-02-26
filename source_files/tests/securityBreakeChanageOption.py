from abc import ABC, abstractmethod
import fastapi

class SecurityBreak(ABC):
 
    @abstractmethod
    def checkThreats(request: fastapi.Request, clientIp : str):
        pass
    @abstractmethod
    def get_name(self):
        pass
    

class HostHeaderInjection(SecurityBreak):
    def __init__(self):
     self.name = "HTTP Host Header Injection"
    
    def checkThreats(request: fastapi.Request):
        return None
    
    def get_name(self):
        return self.name
    
class HPP(SecurityBreak):
    def __init__(self):
     self.name = "HTTP Parameter Pollution"
    
    def checkThreats(request: fastapi.Request):
        return None
    
    def get_name(self):
        return self.name

class OpenRedirect(SecurityBreak):
    def __init__(self):
     self.name = "Open Redirect Vulnerability"
    
    def checkThreats(request: fastapi.Request):
        return None
    
    def get_name(self):
        return self.name

class SQLInjection(SecurityBreak):
    def __init__(self):
     self.name = "SQL Injection"
    
    def checkThreats(request: fastapi.Request):
        return None
    
    def get_name(self):
        return self.name

class SSIInjection(SecurityBreak):
    def __init__(self):
     self.name = "SSI Injection"
    
    def checkThreats(request: fastapi.Request):
        return None
    
    def get_name(self):
        return self.name

class XSS(SecurityBreak):
    def __init__(self):
     self.name = "Cross Site Scripting (XSS)"
    
    def checkThreats(request: fastapi.Request):
        return None
    
    def get_name(self):
        return self.name

class XST(SecurityBreak):
    def __init__(self):
     self.name = "Cross Site Tracing (XST)"
    
    def checkThreats(request: fastapi.Request):
        return None
    
    def get_name(self):
        return self.name