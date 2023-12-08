from abc import ABC, abstractmethod
import fastapi

class SecurityBreak(ABC):
 
    @abstractmethod
    def checkThreats(self, request: fastapi.Request, clientIp : str):
        pass
    @abstractmethod
    def getName(self):
        pass




    
