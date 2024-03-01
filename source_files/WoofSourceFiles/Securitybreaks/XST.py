from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi


class XST(SecurityBreak):
    def __init__(self):
        super().__init__()  # Call parent's constructor
        self.name = "Cross Site Tracing (XST)"

    async def check_threats(self, request: fastapi.Request, clientIp : str):
        """Function check if HTTP request contains Cross Site Tracing (XST) attack,
        by checking if the request method is TRACE.

        Args:
        request (fastapi.Request): the request to check (as recieved from client)
                clientIp (str): the ip of this request sender

        Returns:
            (Bool): true for threats found false for safe packet

        """
        return request.method == "TRACE" , f"{request.method} : {request.url}"
    
    def get_name(self):
        return self.name

    def get_json_name(self):  # json type name, and not the name for displaying
        return 'XST'
