import datetime
import re


class SecurityRuleEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule: str):
        self.rules.append(rule)

    def is_request_malicious(self, request):
        request_url = request.url.path
        if not request_url:
            return False

        for rule in self.rules:
            if re.search(rule, request_url):
                return True

        return False

    def get_attack_name(self, rule):
        # Get the name of the attack
        attack_name = rule.split()[0] if rule else ""
        return attack_name

    def log_security_break(self, request):
        # Log the security break
        with open("security.log", "a") as log_file:
            log_file.write(
                "[{}] Malicious request detected from {} to {}: {} ({})\n".format(
                    datetime.datetime.now(),
                    request.client.host,
                    request.url,
                    self.get_attack_name(request),
                    re.sub(r"[<>&]", r"\&", str(request.headers)),
                    re.sub(r"[<>&]", r"\&", str(request.body)),
                )
            )