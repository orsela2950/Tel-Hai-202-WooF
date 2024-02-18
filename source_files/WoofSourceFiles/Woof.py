import fastapi
import aiohttp
import serverInfo
from uvicorn import run
# Custom modules import
from SecurityRuleEngine import SecurityRuleEngine
import message_loader
import punishment_manager
from logger import Logger

# import the security breaks
from Securitybreaks.Ddos import Ddos as securityRule_Ddos
from Securitybreaks.HostHeaderInjection import HostHeaderInjection as securityRule_HostHeaderInjection
from Securitybreaks.SSIInjection import SSIInjection as securityRule_SSIInjection
from Securitybreaks.OpenRedirect import OpenRedirect as securityRule_OpenRedirect
from Securitybreaks.SQLInjection import SQLInjection as securityRule_SQLInjection
from Securitybreaks.HPP import HPP as securityRule_HPP
from Securitybreaks.XSS import XSS as securityRule_XSS
from Securitybreaks.XST import XST as securityRule_XST

# Declare debugging state
_DEBUGGING = True
# Create a FastAPI app instance
app = fastapi.FastAPI()
# Create a Logger instance
logger = Logger(_DEBUGGING)
# Create a SecurityRuleEngine instance
rule_engine = SecurityRuleEngine(logger)


rule_engine.add_rule(securityRule_Ddos())
rule_engine.add_rule(securityRule_HostHeaderInjection(serverInfoModuleIn=serverInfo))
rule_engine.add_rule(securityRule_HPP())
rule_engine.add_rule(securityRule_SSIInjection())
rule_engine.add_rule(securityRule_OpenRedirect())
rule_engine.add_rule(securityRule_SQLInjection())
rule_engine.add_rule(securityRule_XSS())
rule_engine.add_rule(securityRule_XST())


async def send_safe_packet(path: str, request: fastapi.Request):
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
        if _DEBUGGING:
            print(f"An unexpected error occurred: {e}")
        return fastapi.Response(content=message_loader.load_error_message(e), status_code=500)


@app.api_route("/favicon.ico", methods=["GET"])
async def favicon(request: fastapi.Request):
    return await send_safe_packet("favicon.ico", request)


# Define a route that can handle any HTTP method and any path
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def proxy(path: str, request: fastapi.Request):
    """Handles a request, checking for IP bans and returning appropriate responses."""
    check_ban = punishment_manager.check_ip_ban(request.client.host)
    if check_ban[0]:  # If IP is banned
        try:
            ip, reason, expiration, source = check_ban[1:]  # Unpack ban details

            error_response = message_loader.load_ban_message(ip, reason, expiration, source)

        except ValueError:  # Handle potential errors in ban details
            error_response = message_loader.load_denied_message()
        if _DEBUGGING:
            print("Access Denied response sent to", check_ban[1])
        return fastapi.Response(content=error_response, status_code=403)  # Use 403 Forbidden for clarity

    # Get the original destination(host) from the request headers
    host = serverInfo.remove_scheme(request.headers.get("Host"))
    # Construct the full URL of the original destination(host)
    url = f"http://{host}/{path}"
    ip_read_url = f"http://{serverInfo.get_server_ip()}:{serverInfo.get_server_port()}/{path}"

    # Log the request
    if _DEBUGGING:
        print(f"[+] received: {request.method} | to: {url} | targeted to: {ip_read_url}")
    logger.log_main_toml(request.method, request.client.host, request.client.port, url, ip_read_url)

    malicious_event = await rule_engine.is_request_malicious(request, request.client.host)
    if malicious_event.is_there_risk():
        strike_count = punishment_manager.strike_user(request.client.host, malicious_event.printEventDescription())

        error_response = f"Malicious request detected: {malicious_event.return_risks()}"
        if strike_count == 1:
            error_response += \
                " Be careful! you just got your first strike! 2 more strikes and your be banned for life!"
        elif strike_count == 2:
            error_response += \
                " Be careful! you just got your second strike! 1 more strikes and your be banned for life!"
        elif strike_count == 3:
            error_response += \
                " That's it! you just got third strike! YOU ARE BANNED FOR LIFE!"

        if _DEBUGGING:
            print(error_response)
        return fastapi.Response(content=error_response, status_code=400)

    return await send_safe_packet(path, request)


if __name__ == "__main__":
    # Run the FastAPI app using uvicorn and specify the host and port to listen on
    run(app, port=80)  # , ssl=ssl_context)
    logger.close_debug_log()
    print('Ba bye')
