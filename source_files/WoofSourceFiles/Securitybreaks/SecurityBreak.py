from abc import ABC, abstractmethod
import fastapi


class SecurityBreak(ABC):
    def __init__(self):
        super().__init__()  # Call parent's constructor
        self.state = True

    @abstractmethod
    async def check_threats(self, request: fastapi.Request, clientIp: str):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_json_name(self):  # json type name, and not the name for displaying
        pass
