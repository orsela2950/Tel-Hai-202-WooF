import sys
import datetime
import re
import fastapi
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Securitybreaks.SecurityBreak import SecurityBreak


class SecurityEvent:
    def __init__(self, request: fastapi.Request):
        self.ip = request.client.host
        self.request = request
        self.currentTime = datetime.datetime.now()
        self.SecurityRisks = []

    def printEventDescription(self):
        security_breaks = ", ".join([risk.get_name() for risk in self.SecurityRisks])
        return (
            "You've been caught doing: {}".format(
                security_breaks
            )
        )

    def add_break(self, risk: SecurityBreak):
        if not any(risk == breaker for breaker in self.SecurityRisks):
            self.SecurityRisks.append(risk)

    def is_there_risk(self):
        return len(self.SecurityRisks) > 0

    def return_risks(self):
        return [risk.get_name() for risk in self.SecurityRisks]

    def return_request_body(self):
        return str(re.sub(r"[<>&]", r"\&", str(self.request.body)))

    def return_request_headers(self):
        return str(re.sub(r"[<>&]", r"\&", str(self.request.headers)))
