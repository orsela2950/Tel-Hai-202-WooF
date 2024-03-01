from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi
import urllib.parse


class HPP(SecurityBreak):
    def __init__(self):
        self.name = "HTTP Parameter Pollution"

    async def checkThreats(self, request: fastapi.Request, clientIp: str):
        """
    Function that checks if a request contains HTTP Parameter Pollution (HPP).
        First, it checks for HPP in the parameters when entered in the URL directly
        Then, it checks for HPP in the parameters when entered in a input field
    
    Args:
            request (fastapi.Request): the request to check (as recieved from client)
            clientIp (str): the ip of this request sender

        Returns:
            (Bool): true for threats found false for safe packet

        """

        # Parse the URL:
        parsed_url = urllib.parse.urlparse(str(request.url))

        # Get the parameters as a dictionary
        params_dict = urllib.parse.parse_qs(parsed_url.query)

        # Check if any parameter has more than one value:
        for param_name, param_values in params_dict.items():
            if len(param_values) > 1:
                return True, f"{param_name}={param_values}"

        return False, None

    def getName(self):
        return self.name
