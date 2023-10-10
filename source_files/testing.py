import fastapi
import requests
import uvicorn
import serverIfnfo

# Create a FastAPI app instance
app = fastapi.FastAPI()

# Define a route that can handle any HTTP method and any path
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def proxy(path: str, request: fastapi.Request):
    # Get the original destination from the request headers
    destination = request.headers.get("Host")
    
    # Construct the full URL of the original destination
    url = f"http://{destination}/{path}"
    ipead_url = f"http://{serverIfnfo.IP}:{serverIfnfo.PORT}/{path}"
    
    print(f"[+] recieved: {request.method} | to: {url} | targeted to: {ipead_url}")
    
    
    #----------------
    #make the check here and send back the response from the web server
    #----------------

    #create copy of headers for adding the "x-forwarded-for" header
    modified_headers = {}
    for pair in request.headers.raw:
        modified_headers[pair[0].decode()] = pair[1].decode()
    #add the x forward header
    if "X-Forwarded-For" not in modified_headers.keys():
        modified_headers["X-Forwarded-For"] = request.client.host
    modified_headers["host"] = serverIfnfo.URL
    # Forward the incoming request to the original destination and get the response
    
    try:
        print("method: "+ request.method)
        print("headers: "+ str(modified_headers))
        print("ipead_url: "+ ipead_url)
        #the program crashes here
        response = requests.request(
        method='GET',
        url='http://127.0.0.1:80',)
        return response

    except Exception as e:
        print("exception in respons===============================================================")
        print(e)
    return "error in requestin to web server"

# Run the FastAPI app using uvicorn and specify the host and port to listen on
uvicorn.run(app, port=8000)



#response = requests.get(serverIfnfo.URL_IP, headers={"Host": serverIfnfo.URL}) # Sets the host header to "www.bing.com"
#print(response.request.headers["Host"]) # Prints "www.bing.com"
