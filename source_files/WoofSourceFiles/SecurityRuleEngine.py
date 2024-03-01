from fastapi import Request
import Securitybreaks.SecurityBreak as SecurityBreak
from Security.SecurityEvent import SecurityEvent
from logger import Logger


import serverInfo

class SecurityRuleEngine:
    def __init__(self, logger: Logger):
        self.rules: list[SecurityBreak] = []  # this will be a list of the security break interface object
        self.logger = logger

    def add_rule(self, rule: SecurityBreak):
        self.rules.append(rule)

    def update_rules_state(self):
        rules_state = serverInfo.get_rules_state()
        for rule in self.rules:
            rule.state = rules_state[rule.get_json_name()]

    async def is_request_malicious(self, request: Request, client_ip: str):
        self.update_rules_state()  # Refresh the rules state
        event = SecurityEvent(request)
        
        for rule in self.rules:
            if rule.state:  # If the rule turned on
                check = await rule.check_threats(request, client_ip)
                if check[0]:
                    # The request is malicious, so log it and block it
                    event.add_break(rule)
                    print(rule.get_name(), check[1])
        if event.is_there_risk():
            self.logger.log_security_toml(event)
        return event
