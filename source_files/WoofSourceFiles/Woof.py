import datetime
import fastapi
import aiohttp
import serverInfo
from uvicorn import run
from SecurityRuleEngine import SecurityRuleEngine
from punishment_manager import *

# Custom modules import
import punishment_manager
from logger import Logger
from Ddos import Ddos

# import the security breaks
from Securitybreaks.HostHeaderInjection import HostHeaderInjection as securityRule_HostHeaderInjection
from Securitybreaks.HPP import HPP as securityRule_HPP
from Securitybreaks.SSIInjection import SSIInjection as securityRule_SSIInjection
from Securitybreaks.OpenRedirect import OpenRedirect as securityRule_OpenRedirect
from Securitybreaks.SQLInjection import SQLInjection as securityRule_SQLInjection
from Securitybreaks.XSS import XSS as securityRule_XSS
from Securitybreaks.XST import XST as securityRule_XST
from Security.SecurityEvent import SecurityEvent
from Securitybreaks.Helper import Helper

# Declare debugging state
_DEBUGGING = True
# Create a FastAPI app instance
app = fastapi.FastAPI()
# Create a Logger instance
logger = Logger(_DEBUGGING)
# Create a SecurityRuleEngine instance
rule_engine = SecurityRuleEngine(logger)
ddos = Ddos()

# Add rules to the SecurityRuleEngine instance
rule_engine.add_rule(securityRule_HostHeaderInjection(serverInfoModuleIn=serverInfo))
rule_engine.add_rule(securityRule_HPP())
rule_engine.add_rule(securityRule_SSIInjection())
rule_engine.add_rule(securityRule_OpenRedirect())
rule_engine.add_rule(securityRule_SQLInjection())
rule_engine.add_rule(securityRule_XSS())
rule_engine.add_rule(securityRule_XST())


def load_ban_message(ip, reason, expiration, source):
    with Helper.findFile_Read("ban_msg.html", "source_files\\WoofSourceFiles\\WoofManagerPanel\\ban_message") as html_f:
        with Helper.findFile_Read("ban_style.css",
                                  "source_files\\WoofSourceFiles\\WoofManagerPanel\\ban_message") as css_f:
            return html_f.read().format(css_styles=css_f.read(), ip=ip, reason=reason, expiration=expiration,
                                        source=source)


def load_error_message(e: Exception):
    with Helper.findFile_Read(
            "error_msg.html", "source_files\\WoofSourceFiles\\WoofManagerPanel\\error_message") as html_f:
        with Helper.findFile_Read(
                "error_style.css", "source_files\\WoofSourceFiles\\WoofManagerPanel\\error_message") as css_f:
            # Read the contents of the CSS
            css_styles = css_f.read()

            # Insert the CSS styles and error message into the HTML template
            html_content = html_f.read().format(css_styles=css_styles, error=e)

            return html_content


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
        if _DEBUGGING: print(f"An unexpected error occurred: {e}")
        return fastapi.Response(content=load_error_message(e), status_code=500)


@app.api_route("/favicon.ico", methods=["GET"])
async def favicon(request: fastapi.Request):
    return await send_safe_packet("favicon.ico", request)


# Define a route that can handle any HTTP method and any path
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def proxy(path: str, request: fastapi.Request):
    """Handles a request, checking for IP bans and returning appropriate responses."""
    check_ban = check_ip_ban(request.client.host)
    if check_ban[0]:  # If IP is banned
        try:
            ip, reason, expiration, source = check_ban[1:]  # Unpack ban details

            error_response = load_ban_message(ip, reason, expiration, source)

        except ValueError:  # Handle potential errors in ban details
            error_response = """
            <h1>Access Denied</h1>
            <p>Your IP address has been banned, but detailed information is unavailable.</p>
            """
        if _DEBUGGING: print("Access Denied response sent to", check_ban[1])
        return fastapi.Response(content=error_response, status_code=403)  # Use 403 Forbidden for clarity

    # Get the original destination(host) from the request headers
    host = serverInfo.remove_scheme(request.headers.get("Host"))
    # Construct the full URL of the original destination(host)
    url = f"http://{host}/{path}"
    ipead_url = f"http://{serverInfo.get_server_ip()}:{serverInfo.get_server_port()}/{path}"

    # Log the request
    if _DEBUGGING: print(f"[+] recieved: {request.method} | to: {url} | targeted to: {ipead_url}")
    logger.log_main(request.method, request.client.host, request.client.port, url, ipead_url)

    diff_ddos = await ddos.packet_into_stuck(request)
    if diff_ddos[0]:
        error_response = f"Ddos attack deteced, {diff_ddos[1]}" + \
                         "Be careful! you just got a strike! 3 strikes and your be banned for life"
        if _DEBUGGING: print(error_response)
        ddos_event = SecurityEvent(request)
        ddos_event.add_break(ddos)
        logger.log_security(ddos_event)
        punishment_manager.strike_user(request.client.host, "You've been caught doing: Ddos attack")
        return fastapi.Response(content=error_response, status_code=400)

    malicious_event = await rule_engine.is_request_malicious(request, request.client.host)
    if malicious_event.is_there_risk():
        error_response = f"Malicious request detected: {malicious_event.return_risks()}" + \
                         "Be careful! you just got a strike! 3 strikes and your be banned for life"
        if _DEBUGGING: print(error_response)
        punishment_manager.strike_user(request.client.host, malicious_event.printEventDescription())  # not DOS event
        return fastapi.Response(content=error_response, status_code=400)

    return await send_safe_packet(path, request)


if __name__ == "__main__":
    # Run the FastAPI app using uvicorn and specify the host and port to listen on
    run(app, host="0.0.0.0", port=80)  # , ssl=ssl_context)
