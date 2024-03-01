from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi
import re
import threading


class SQLInjection(SecurityBreak):
    def __init__(self):
        super().__init__()  # Call parent's constructor
        self.name = "SQL Injection"
        self.debug_prints = False

    async def check_threats(self, request: fastapi.Request, clientIp: str):
        """Check if the request contains SQL Injection

        Args:
            request (fastapi.Request): the request to check (as recieved from client)
            clientIp (str): the ip of this request sender

        Returns:
            (Bool): true for threats found false for safe packet
        """

        regex = (r"(?i)\b(?:SELECT|UPDATE|DELETE|INSERT\s+INTO|CREATE\s+(?:DATABASE|TABLE|INDEX|VIEW)|ALTER\s+("
                 r"?:DATABASE|TABLE)|DROP\s+(?:TABLE|INDEX)|WHERE|FROM|JOIN|ON|AS|GROUP\s+BY|HAVING|ORDER\s+BY|LIMIT"
                 r"|OFFSET)\b")

        for param_name, param_value in request.query_params.items():
            matchBody = re.search(regex, param_value)
            if matchBody:
                full_query = matchBody.group()
                self.debug_print(f"A sql statement was detected in the request params:{full_query}")
                return True, full_query

        for header, value in request.headers.items():
            matchHeader = re.search(regex, value)
            if matchHeader:
                full_query = matchHeader.group()
                self.debug_print(f"A sql statement was detected in the request headers:{full_query}")
                return True, full_query

        body = await request.body()
        if body:
            matchHeader = re.search(regex, str(body))
            if matchHeader:
                full_query = matchHeader.group()
                self.debug_print(f"A sql statement was detected in the request body:{full_query}")
                return True, full_query

        return False, None

    def get_name(self):
        return self.name

    def get_json_name(self):  # json type name, and not the name for displaying
        return 'SQL_Injection'

    def debug_print(self, text: str):
        if self.debug_prints:
            print('[SQL Injection debug] ' + text)
