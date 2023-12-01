import datetime
import fastapi
import httpx
import os
import serverInfo
from uvicorn import run
from SecurityRuleEngine import SecurityRuleEngine

#import the security breaks
from Securitybreaks.HostHeaderInjection import HostHeaderInjection as securityRule_HostHeaderInjection
from Securitybreaks.HPP import HPP as securityRule_HPP
from Securitybreaks.SSIInjection import SSIinjection as securityRule_SSIinjection
from Securitybreaks.OpenRedirect import OpenRedirect as securityRule_OpenRedirect
from Securitybreaks.SQLInjection import SQLInjection as securityRule_SQLInjection
from Securitybreaks.XSS import XSS as securityRule_XSS
from Securitybreaks.XST import XST as securityRule_XST
import Security.SecurityEvent as SecurityEvent

# Create a FastAPI app instance
app = fastapi.FastAPI()

# Create a SecurityRuleEngine instance
rule_engine = SecurityRuleEngine()

# Add rules to the SecurityRuleEngine instance
rule_engine.add_rule(securityRule_HostHeaderInjection(serverInfoModuleIn=serverInfo))
rule_engine.add_rule(securityRule_HPP())
rule_engine.add_rule(securityRule_SSIinjection())
rule_engine.add_rule(securityRule_OpenRedirect())
rule_engine.add_rule(securityRule_SQLInjection())
rule_engine.add_rule(securityRule_XSS())
rule_engine.add_rule(securityRule_XST())

# Define a route that can handle any HTTP method and any path
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def proxy(path: str, request: fastapi.Request):
    # Get the original destination from the request headers
    destination = serverInfo.remove_scheme(request.headers.get("Host"))
    # Construct the full URL of the original destination
    url = f"http://{destination}/{path}"
    ipead_url = f"http://{serverInfo.IP}:{serverInfo.PORT}/{path}"


    # Log the request
    print(f"[+] recieved: {request.method} | to: {url} | targeted to: {ipead_url}")
    
    with rule_engine.findFile("waf.log", "source_files/WoofSourceFiles/Logs") as log_file:
        # Log the request
        log_file.write("[{}] Request received: {}:{} -> {} ->{}\n".format(datetime.datetime.now(), request.client.host,request.client.port,url,ipead_url))
    #==============================


    malicious_event = rule_engine.is_request_malicious(request, request.client.host)
    if malicious_event.thereIsRisk():
        error_response = f"Malicious request detected: {malicious_event.returnRisks()}"
        print(error_response)
        return fastapi.Response(content=error_response, status_code=400)

#ok VV
    modified_headers = {}
    for pair in request.headers.raw:
        modified_headers[pair[0].decode()] = pair[1].decode()
    # add the x forward header
    modified_headers["X-Forwarded-For"] = request.client.host
    modified_headers["host"] = destination

    try:
        # Forward the incoming request to the original destination and get the response
        client = httpx.Client()
        if request.method == 'GET':
            response = client.get(ipead_url, headers=modified_headers, params=request.query_params)
        elif request.method == 'POST':
            response = client.post(ipead_url, headers=modified_headers, data= await request.body())
        else:
            return fastapi.Response(content="NEW HTTP METHOD, We Support only post and get at the time", status_code=500)
        
    except httpx.HTTPError as http_err:
        # Handle HTTP errors (e.g., 4xx or 5xx responses)
        print(f"HTTP error occurred: {http_err}")
        return fastapi.Response(content=f"HTTP error occurred: {http_err}", status_code=500)

    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")
        return fastapi.Response(content=f"An unexpected error occurred: {e}", status_code=500)


    # Check the size and complexity of the response object
    if len(response.content) > 1024 * 1024:
        # The response object is too large
        raise Exception("Response object is too large")

    return fastapi.Response(content=response.content, headers=response.headers, status_code=response.status_code)

# Run the FastAPI app using uvicorn and specify the host and port to listen on
if __name__ == "__main__":
    run(app, host="0.0.0.0", port=80)#, ssl=ssl_context)