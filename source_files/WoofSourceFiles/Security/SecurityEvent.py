from Securitybreaks.SecurityBreak import SecurityBreak
import datetime
import re

class SecurityEvent:
    def __init__(self, request):
        self.ip = request.client.host
        self.request = request
        self.currentTime = datetime.datetime.now()
        self.SecurityRisks = []

    def printEventDescription(self):
            security_breaks = ", ".join([risk.getName() for risk in self.SecurityRisks])
            return (
                "[{}] Malicious request detected from {} to {}: {} ({})\n".format(
                    datetime.datetime.now(),
                    self.request.client.host,
                    self.request.url,
                    security_breaks,
                    re.sub(r"[<>&]", r"\&", str(self.request.headers)),
                    re.sub(r"[<>&]", r"\&", str(self.request.body)),
                )
            )

    def addBreak(self,risk: SecurityBreak):
         if not any(risk == breaker for breaker in self.SecurityRisks):
              self.SecurityRisks.append(risk)
    
    def thereIsRisk(self):
         return len(self.SecurityRisks)>0