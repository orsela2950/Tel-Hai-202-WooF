import datetime
from fastapi import Request
import Securitybreaks.SecurityBreak as SecurityBreak
from Security.SecurityEvent import SecurityEvent
from logger import Logger


def get_attack_name(rule: SecurityBreak):
    # Get the name of the attack
    attack_name = rule.getName()
    return attack_name


class SecurityRuleEngine:
    def __init__(self, logger: Logger):
        self.rules = []  # this will be a list of the security break interface object
        self.logger = logger

    def add_rule(self, rule: SecurityBreak):
        self.rules.append(rule)

    async def is_request_malicious(self, request: Request, client_ip: str):
        request_url = request.url.path
        event = SecurityEvent(request)
        
        for rule in self.rules:
            print('checking:', rule.getName()+'...')
            check = await rule.checkThreats(request, client_ip)
            if check[0]:
                # The request is malicious, so log it and block it
                event.add_break(rule)
                print(rule.getName(), check[1])
        if event.is_there_risk():
            self.logger.log_security(event)
        return event
