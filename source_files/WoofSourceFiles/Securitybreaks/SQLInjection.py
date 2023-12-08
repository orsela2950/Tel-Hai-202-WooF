from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi
import re


class SQLInjection(SecurityBreak):
    def __init__(self):
     self.name = "SQL Injection"
    
    def checkThreats(self, request: fastapi.Request, clientIp : str):
        """Check if the request contains SQL Injection

        Args:
            request (fastapi.Request): the request to check (as recieved from client)
            clientIp (str): the ip of this request sender

        Returns:
            (Bool): true for threats found false for safe packet
        """

        regex = r"(?i)\b(?:SELECT|UPDATE|DELETE|INSERT\s+INTO|CREATE\s+(?:DATABASE|TABLE|INDEX|VIEW)|ALTER\s+(?:DATABASE|TABLE)|DROP\s+(?:TABLE|INDEX)|WHERE|FROM|JOIN|ON|AS|GROUP\s+BY|HAVING|ORDER\s+BY|LIMIT|OFFSET)\b"
        

        for param_name, param_value in request.query_params.items():
            matchBody = re.search(regex, param_value)
            if matchBody:
                full_query = matchBody.group()
                self.debugPrint(f"A sql statement was detected in the request:{full_query}")
                return (True, full_query)
            

        for header, value in request.headers.items():
            matchHeader = re.search(regex, value)
            if matchHeader:
                full_query = matchHeader.group()
                self.debugPrint(f"A sql statement was detected in the request:{full_query}")
                return True,full_query
        
        
        return (False, None)
    
    def getName(self):
        return self.name
    
    def debugPrint(self, text :str):
        if self.debugPrint:
            print('[SQL Injection debug] ' + text)