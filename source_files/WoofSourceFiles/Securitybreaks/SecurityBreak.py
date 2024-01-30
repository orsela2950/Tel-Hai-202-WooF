from abc import ABC, abstractmethod
import fastapi


class SecurityBreak(ABC):

    @abstractmethod
    async def checkThreats(self, request: fastapi.Request, clientIp: str):
        pass

    @abstractmethod
    def getName(self):
        pass
