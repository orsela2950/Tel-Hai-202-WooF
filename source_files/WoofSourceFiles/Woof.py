import datetime
import fastapi
import aiohttp
import os
import asyncio
import serverInfo
import re
from uvicorn import run
from SecurityRuleEngine import SecurityRuleEngine
from punishment_manager import *
from Ddos import Ddos
from elasticsearch import Elasticsearch

# import the security breaks
from Securitybreaks.HostHeaderInjection import HostHeaderInjection as securityRule_HostHeaderInjection
from Securitybreaks.HPP import HPP as securityRule_HPP
from Securitybreaks.SSIInjection import SSIInjection as securityRule_SSIInjection
from Securitybreaks.OpenRedirect import OpenRedirect as securityRule_OpenRedirect
from Securitybreaks.SQLInjection import SQLInjection as securityRule_SQLInjection
from Securitybreaks.XSS import XSS as securityRule_XSS
from Securitybreaks.XST import XST as securityRule_XST
from Security.SecurityEvent import SecurityEvent

# Create a FastAPI app instance
app = fastapi.FastAPI()

es = Elasticsearch("http://localhost:9200")

# Create a SecurityRuleEngine instance
rule_engine = SecurityRuleEngine(es)

ddos = Ddos()

    


# Add rules to the SecurityRuleEngine instance
rule_engine.add_rule(securityRule_HostHeaderInjection(serverInfoModuleIn=serverInfo))
rule_engine.add_rule(securityRule_HPP())
rule_engine.add_rule(securityRule_SSIInjection())
rule_engine.add_rule(securityRule_OpenRedirect())
rule_engine.add_rule(securityRule_SQLInjection())
rule_engine.add_rule(securityRule_XSS())
rule_engine.add_rule(securityRule_XST())


# Define a route that can handle any HTTP method and any path
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def proxy(path: str, request: fastapi.Request):
    refresh_blacklist()
    check_ban=check_ip_ban()
    if check_ban[0]:
        error_response = f"You are banned for this reason: {check_ban[2]}\n"

        # Check if the ban is not permanent (ban column is False)
        if not check_ban[5]:
            expiration_date = check_ban[4]
            error_response += f"The ban will expire on: {expiration_date}\n"

        print(error_response)
        return fastapi.Response(content=error_response, status_code=400)
    
    
    
    # Get the original destination(host) from the request headers
    host = serverInfo.remove_scheme(request.headers.get("Host"))
    # Construct the full URL of the original destination(host)
    url = f"http://{host}/{path}"
    ipead_url = f"http://{serverInfo.get_server_ip()}:{serverInfo.get_server_port()}/{path}"
    # Log the request
    print(f"[+] recieved: {request.method} | to: {url} | targeted to: {ipead_url}")

    with rule_engine.findFile_Write("waf.log", "source_files/WoofSourceFiles/Logs") as log_file:
        # Log the request
        log_file.write("[{}] Request received: {}:{} -> {} ->{}\n".format(datetime.datetime.now(), request.client.host,
                                                                          request.client.port, url, ipead_url))
        log_file.close()
        
        
     # Log the request to Elasticsearch
    log_data = {
        "@timestamp": datetime.datetime.now().isoformat(),
        "request_method": request.method,
        "client_host": request.client.host,
        "port":request.client.port,
        "url": url,
        "target_url": ipead_url
    }
    # Index the log data to Elasticsearch
    es.index(index="requests", body=log_data)
        
        
        
    
    diff_ddos = await ddos.packet_into_stuck(request)
    if diff_ddos[0]:
        error_response = f"Ddos attack deteced, {diff_ddos[1]}"
        print(error_response)
        DdosEvent = SecurityEvent(request)
        DdosEvent.addBreak(ddos)
        rule_engine.log_security_break(DdosEvent)
        return fastapi.Response(content=error_response, status_code=400)

    malicious_event = await rule_engine.is_request_malicious(request, request.client.host)
    if malicious_event.thereIsRisk():
        error_response = f"Malicious request detected: {malicious_event.returnRisks()}"
        print(error_response)
        return fastapi.Response(content=error_response, status_code=400)

    try:
        # Extract the target URL from the path
        target_url = serverInfo.get_server_ipead_url() + ':' + str(serverInfo.get_server_port()) + '/' + path
        
        
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
        return fastapi.Response(content=f"An unexpected error occurred: {e.args}", status_code=500)

if __name__ == "__main__":
    # Run the FastAPI app using uvicorn and specify the host and port to listen on
    run(app, host="0.0.0.0", port=80)  # , ssl=ssl_context)
