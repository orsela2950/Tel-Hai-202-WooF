import requests
from SecurityRuleEngine import SecurityRuleEngine
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import serverIfnfo
import ssl #for later - for htttps support

app = FastAPI()
#app.add_security_rule_engine()
#app.add_logger(Logger())


@app.get("/{path}")
async def inspect_request(request: Request, path: str):
    print("path: {}".format(path))
    #check if the requests host matches the servers url
    if "host" in request.headers and request.headers["host"].startswith(serverIfnfo.URL):  
        return "good!"
    return "not good!"


# Run the FastAPI app using uvicorn and specify the host and port to listen on
uvicorn.run(app, port=8000)

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
