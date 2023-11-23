import datetime
import re
import fastapi
import Securitybreaks.SecurityBreak as SecurityBreak
from Security.SecurityEvent import SecurityEvent
import os
from pathlib import Path

class SecurityRuleEngine:
    def __init__(self):
        self.rules = [] # this will be a list of the security break interface object

    def add_rule(self, rule: SecurityBreak):
        self.rules.append(rule)

    def is_request_malicious(self, request : fastapi.Request, clientIp : str):
        request_url = request.url.path
        event = SecurityEvent(request)
        
        for rule in self.rules:
            check= rule.checkThreats(request, clientIp)
            if check[0] :
                # The request is malicious, so log it and block it
                event.addBreak(rule)
                print(rule.getName(),check[1])
        if event.thereIsRisk(): self.log_security_break(event)        
        return event
    def get_attack_name(self, rule):
        # Get the name of the attack
        attack_name = rule.getName()
        return attack_name

    def log_security_break(self,event): 
        # Log the security break
        with self.findFile("securityEvents.log","source_files\WoofSourceFiles\Logs") as log_file:
            log_file.write(event.printEventDescription())
    
    def findFile(self,name, path):
        filePath=""
        for root, dirs, files in os.walk(os.getcwd()):
            if name in files:
                return open(os.path.join(root, name),"a")
        return open(path+"\\"+name,"w")
        
        
            
