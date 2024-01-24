from ..Securitybreaks.SecurityBreak import SecurityBreak
from ..Ddos import Ddos
import datetime
import re
import fastapi


class SecurityEvent:
    def __init__(self, request: fastapi.Request):
        self.ip = request.client.host
        self.request = request
        self.currentTime = datetime.datetime.now()
        self.SecurityRisks = []

    # def printEventDescription(self):
    #     security_breaks = ", ".join([risk.getName() for risk in self.SecurityRisks])
    #     return (
    #         "[{}] Malicious request detected from {} to {} | detected: {} | headers:({})\n".format(
    #             datetime.datetime.now(),
    #             self.request.client.host,
    #             self.request.url,
    #             security_breaks,
    #             self.returnRequestHeaders(),
    #             # self.returnRequestBody(),
    #         )
    #     )

    def add_break(self, risk: SecurityBreak or Ddos):
        if not any(risk == breaker for breaker in self.SecurityRisks):
            self.SecurityRisks.append(risk)

    def is_there_risk(self):
        return len(self.SecurityRisks) > 0

    def return_risks(self):
        return [risk.getName() for risk in self.SecurityRisks]

    def return_request_body(self):
        return str(re.sub(r"[<>&]", r"\&", str(self.request.body)))

    def return_request_headers(self):
        return str(re.sub(r"[<>&]", r"\&", str(self.request.headers)))
