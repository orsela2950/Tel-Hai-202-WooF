import requests
from SecurityRuleEngine import SecurityRuleEngine
from fastapi import FastAPI, Request
from pydantic import BaseModel
import serverIfnfo
import ssl #for later - for htttps support

#python -m uvicorn WooF_Main:app

app = FastAPI()
#app.add_security_rule_engine()
#app.add_logger(Logger())


@app.get("/")
async def inspect_request(request: Request, test: int = 999):
    #check if the requests host matches the servers url
    if "host" in request.headers and request.headers["host"].startswith(serverIfnfo.URL):  
        return "good!"
    return "not good!"



"""commented out
    @app.post("/security_rules")
    async def add_security_rule(rule: str):
        security_rule_engine.add_rule(rule)
        return {"message": "Hello World"}
    if security_rule_engine.is_request_malicious(request):
            # Block the request
            pass
        # Forward the request to the backend server
        pass
"""
