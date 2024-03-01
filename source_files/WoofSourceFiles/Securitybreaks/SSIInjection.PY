from Securitybreaks.SecurityBreak import SecurityBreak
import re
import fastapi
from urllib.parse import unquote


class SSIInjection(SecurityBreak):
    def __init__(self):
        super().__init__()  # Call parent's constructor
        self.name = "SSI Injection"

    async def check_threats(self, request: fastapi.Request, clientIp: str):
        """Function to check if a request contains SSIi (Server-Side Includes Injection) characters.

        Args:
        request (fastapi.Request): the request to check (as recieved from client)
                clientIp (str): the ip of this request sender

        Returns:
            (Bool): true for threats found false for safe packet

        """
        request_data = request.query_params
        body = await request.body()
        decoded_text = unquote(body.decode())
        print(decoded_text)
        for param_name, param_value in request_data.items():
            if self.is_text_ssii(param_value):
                return True, param_value

        if self.is_text_ssii(body.decode()) or self.is_text_ssii(decoded_text):
            return True, "SII injection in body"

        return False, None

    def get_name(self):
        return self.name

    def get_json_name(self):  # json type name, and not the name for displaying
        return 'SSI_Injection'

    def is_text_ssii(self, text: object) -> bool:
        """Function to check if a string contains SSI injection (Server-Side Includes Injection) characters.

        Args:
            text (str): The string to check if contains SSI characters.

        Returns:
            bool: True - SSIi detected, False - Safe string.
        """
        return bool(re.search("<!--#(.*?)-->", text))
