import datetime
import fastapi
import httpx
import serverIfnfo
from uvicorn import run
from SecurityRuleEngine import SecurityRuleEngine

#import the security breaks
import Securitybreaks.HostHeaderInjection
import Securitybreaks.HPP
import Securitybreaks.OpenRedirect
import Securitybreaks.SQLInjection
import Securitybreaks.XSS
import Securitybreaks.XST

# Create a FastAPI app instance
app = fastapi.FastAPI()

# Create a SecurityRuleEngine instance
rule_engine = SecurityRuleEngine()

# Add rules to the SecurityRuleEngine instance
rule_engine.add_rule(Securitybreaks.HostHeaderInjection.HostHeaderInjection())
rule_engine.add_rule(Securitybreaks.HPP)
rule_engine.add_rule(Securitybreaks.OpenRedirect)
rule_engine.add_rule(Securitybreaks.SQLInjection)
rule_engine.add_rule(Securitybreaks.XSS)
rule_engine.add_rule(Securitybreaks.XST)

# Define a route that can handle any HTTP method and any path
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def proxy(path: str, request: fastapi.Request):
    # Get the original destination from the request headers
    destination = request.headers.get("Host")
    # Construct the full URL of the original destination
    url = f"http://{destination}/{path}"
    ipead_url = f"http://{serverIfnfo.IP}:{serverIfnfo.PORT}/{path}"


    # Log the request
    print(f"[+] recieved: {request.method} | to: {url} | targeted to: {ipead_url}")
    with open("Logs\waf.log", "a") as log_file:
        # Log the request
        log_file.write("[{}] Request received: {}:{} -> {} ->{}\n".format(datetime.datetime.now(), request.client.host,request.client.port,url,ipead_url))
    #==============================


    malicious_rule = rule_engine.is_request_malicious(request, request.client.host)
    if malicious_rule:
        error_response = f"Malicious request detected: {malicious_rule}"
        return fastapi.Response(content=error_response, status_code=400)


    #transfer this to the header injection soon ==============================================
    modified_headers = {}
    for pair in request.headers.raw:
        modified_headers[pair[0].decode()] = pair[1].decode()
    # add the x forward header
    modified_headers["X-Forwarded-For"] = request.client.host
    modified_headers["host"] = serverIfnfo.URL

#ok VV
    # Forward the incoming request to the original destination and get the response
    client = httpx.Client()
    response = client.get(ipead_url, headers=modified_headers)

    # Check the size and complexity of the response object
    if len(response.content) > 1024 * 1024:
        # The response object is too large
        raise Exception("Response object is too large")

    return fastapi.Response(content=response.content, headers=response.headers, status_code=response.status_code)


# Run the FastAPI app using uvicorn and specify the host and port to listen on
run(app,host="0.0.0.0",port=8000)