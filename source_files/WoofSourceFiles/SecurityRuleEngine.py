import datetime
import re
import fastapi
import Securitybreaks.SecurityBreak as SecurityBreak

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
            results = rule.checkThreats(request, clientIp)
            if results:
                # The request is malicious, so log it and block it
                self.log_security_break(request,rule)
                return rule
        return None # if no rule apllied to the request

    def get_attack_name(self, rule):
        # Get the name of the attack
        attack_name = rule.split()[0] if rule else ""
        return attack_name

    def log_security_break(self, request,rule):
        # Log the security break
        with open("Security\Logs\securityEvents.log", "a") as log_file:
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