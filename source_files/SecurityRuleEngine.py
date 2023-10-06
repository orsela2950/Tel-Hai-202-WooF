from datetime import datetime

class SecurityRuleEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule: str):
        self.rules.append(rule)

    def is_request_malicious(self, request):
        return False #just for now
        for rule in self.rules:
            if rule in request.url:
                return True

        return False

class Logger:
    def __init__(self):
        self.file = open("waf.log", "w")

    def log(self, message: str):
        self.file.write(datetime.datetime.now() +' | '+ message + "\n")
