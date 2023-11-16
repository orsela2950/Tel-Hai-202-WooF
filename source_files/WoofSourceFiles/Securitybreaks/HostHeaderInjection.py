from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi


class HostHeaderInjection(SecurityBreak):
    def __init__(self, serverInfoModuleIn):
        self.name = "HTTP Host Header Injection"
        self.serverInfoModule = serverInfoModuleIn
        
    def checkThreats(self, request: fastapi.Request, clientIp : str):
        """gets a request and checks if it got the host header injection in it

        Args:
            request (fastapi.Request): the request to check (as recieved from client)
            clientIp (str): the ip of this request sender

        Returns:
            (Bool): true for threats found false for safe packet
        """        
        does_headers_equal = self.compare_hosts(self.serverInfoModule.MAIN_URL, request.headers["host"])

        #if headers equal we need to return false for not finding threats
        return not does_headers_equal

    
    def getName(self):
        return self.name
    
    def compare_hosts(self, saved_host : str, requested_host: str):
        """compairs 2 hosts after stripping

        Args:
            saved_host (str): saved in server info
            requested_host (str): requested by client

        Returns:
            (Bool): true for headers equal and false for not equal
        """
        # Normalize saved host by removing port number and scheme
        normalized_saved_host = self.serverInfoModule.remove_scheme(saved_host).split(':')[0]

        # Normalize requested host by removing port number and scheme
        normalized_requested_host = self.serverInfoModule.remove_scheme(requested_host).split(':')[0]

        # Compare normalized hosts
        if normalized_saved_host.lower() == normalized_requested_host.lower():
            return True
        return False