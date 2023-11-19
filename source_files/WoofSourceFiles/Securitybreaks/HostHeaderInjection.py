from Securitybreaks.SecurityBreak import SecurityBreak
import fastapi
import re


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
        # Define the headers to check for HHI attacks (there are several headers that can be used to set the Host header):
        host_header_names = ['Host', 'X-Forwarded-Host', 'X-Host', 'X-Forwarded-Server', 'X-HTTP-Host-Override', 'Forwarded']
        # Check if there are more than one host header (all kinds) in the request (HHI attack):
        host_headers_in_request = list(set([i.lower() for i in host_header_names]).intersection(set([i.lower() for i in request.headers.keys()])))
        if len(host_headers_in_request) > 1:
            return True #(f"{', '.join(host_headers_in_request)}: {request.headers.getlist(host_headers_in_request[0])}")
        

        # For each header name, get all the values of the header and check them for HHI attacks
        for curr_host_header in host_header_names:
            
            # Get the host header values as a list:
            host_headers_values = request.headers.getlist(curr_host_header)
            
            # If there are more than one header value, it means that the header was set more than once (HHI attack):
            if len(host_headers_values) > 1:
                return True #f"{curr_host_header}: {host_headers_values}"
            
            # If no header in the "curr_host_header" was found, continue to the next header name:
            if len(host_headers_values) != 0:
                host_header_to_check = host_headers_values[0]  # Get the header value to check for HHI attacks
                
                # Check if the header value contains any illegal characters or patterns that might indicate an HHI attack (like '\n'):
                if not re.match(r'^[a-zA-Z0-9.\-:%]+\Z', host_header_to_check):
                    return True #f"{curr_host_header}: {host_header_to_check}"
            
        # If passed all the checks, return False (not HHI):
        return False #None

    
    def getName(self):
        return self.name
    
    

    