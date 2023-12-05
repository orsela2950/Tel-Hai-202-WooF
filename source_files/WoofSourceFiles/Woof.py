import datetime
import fastapi
import aiohttp
import os
import serverInfo
from uvicorn import run
from SecurityRuleEngine import SecurityRuleEngine

#import the security breaks
from Securitybreaks.HostHeaderInjection import HostHeaderInjection as securityRule_HostHeaderInjection
from Securitybreaks.HPP import HPP as securityRule_HPP
from Securitybreaks.SSIinjection import SSIinjection as securityRule_SSIinjection
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

    malicious_event = rule_engine.is_request_malicious(request, request.client.host)
    if malicious_event.thereIsRisk():
        error_response = f"Malicious request detected: {malicious_event.returnRisks()}"
        print(error_response)
        return fastapi.Response(content=error_response, status_code=400)

    try:
        # Extract the target URL from the path
        target_url = serverInfo.URL_IP + ':' + str(serverInfo.PORT) + path

        # Create an async HTTP client session
        async with aiohttp.ClientSession() as session:
            # Construct the request object using the FastAPI `Request` object
            request_kwargs = {
                "method": request.method,
                "url": target_url,
                "headers": dict(request.headers),  # Convert `Headers` object to dictionary
            }
            # add the X-Forwarded-For header
            request_kwargs["headers"]["X-Forwarded-For"] = request.client.host

            # If there is a body, pass it as a positional argument after the URL
            if request.body:
                request_kwargs = request_kwargs | {"data": await request.body()}

            # Send the request to the target server
            async with session.request(**request_kwargs) as target_response:
                # Copy the response status code
                status_code = target_response.status

                # Copy the response headers
                headers = {}
                for name, value in target_response.headers.items():
                    headers[name] = value

                # Copy the response body
                body = await target_response.read()

                # Construct the FastAPI response
                return fastapi.Response(
                    status_code=status_code,
                    headers=headers,
                    content=body,
                )
                
    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")
        return fastapi.Response(content=f"An unexpected error occurred: {e}", status_code=500)

# Run the FastAPI app using uvicorn and specify the host and port to listen on
if __name__ == "__main__":
    run(app, host="0.0.0.0", port=80)#, ssl=ssl_context)