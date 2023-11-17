import datetime
import re
import fastapi
import Securitybreaks.SecurityBreak as SecurityBreak
import os
from pathlib import Path

class SecurityRuleEngine:
    def __init__(self):
        self.rules = [] # this will be a list of the security break interface object

    def add_rule(self, rule: SecurityBreak):
        self.rules.append(rule)

    def is_request_malicious(self, request : fastapi.Request, clientIp : str):
        request_url = request.url.path
        if not request_url:
            return None
        
        for rule in self.rules:
            if rule.checkThreats(request, clientIp):
                # The request is malicious, so log it and block it
                self.log_security_break(request,rule)
                return rule
        return None # if no rule apllied to the request

    def get_attack_name(self, rule):
        # Get the name of the attack
        attack_name = rule.getName()
        return attack_name

    def log_security_break(self, request,rule): # fix this function for if the directory doesnt exist
        # Log the security break
        with self.findFile("securityEvents.log","source_files\WoofSourceFiles\Logs") as log_file:
            log_file.write(
                "[{}] Malicious request detected from {} to {}: {} ({})\n".format(
                    datetime.datetime.now(),
                    request.client.host,
                    request.url,
                    self.get_attack_name(rule),
                    re.sub(r"[<>&]", r"\&", str(request.headers)),
                    re.sub(r"[<>&]", r"\&", str(request.body)),
                )
            )
    
    def findFile(self,name, path):
        filePath=""
        for root, dirs, files in os.walk(os.getcwd()):
            if name in files:
                return open(os.path.join(root, name),"a")
        return open(path+"\\"+name,"w")
        
        
            
