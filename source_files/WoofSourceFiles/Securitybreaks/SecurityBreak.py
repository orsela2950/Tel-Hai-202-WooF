from abc import ABC, abstractmethod
import fastapi

class SecurityBreak(ABC):
 
    @abstractmethod
    def checkThreats(request: fastapi.Request):
        pass
    @abstractmethod
    def getName(self):
        pass




    
