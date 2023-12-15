from Securitybreaks.SecurityBreak import SecurityBreak
import re
import fastapi
from fastapi import Query

class SSIInjection(SecurityBreak):
    def __init__(self):
     self.name = "SSI Injection"
    
    async def checkThreats(self, request: fastapi.Request, clientIp : str):
        """Function to check if a request contains SSIi (Server-Side Includes Injection) characters.

        Args:
        request (fastapi.Request): the request to check (as recieved from client)
                clientIp (str): the ip of this request sender

        Returns:
            (Bool): true for threats found false for safe packet

        """
        request_data=request.query_params
        for param_name, param_value in request_data.items():
            if self.is_text_ssii(param_value):
                return True ,param_value
        
        return False ,None
    
    def getName(self):
        return self.name
    
    def is_text_ssii(self,text):
        """Function to check if a string contains SSI injection (Server-Side Includes Injection) characters.

        Args:
            text (str): The string to check if contains SSI characters.

        Returns:
            bool: True - SSIi detected, False - Safe string.
        """
        return re.compile("<!--#(.*?)-->").match(text)