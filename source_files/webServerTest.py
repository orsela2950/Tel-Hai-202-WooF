from fastapi import FastAPI, Request
import uvicorn
app = FastAPI()

@app.get("/")
async def root(request: Request):
    return "requested host "+ request.headers.get("Host")

print("-= ==WEBSERVER TESTER== =-")
# Run the FastAPI app using uvicorn and specify the host and port to listen on
uvicorn.run(app, port=80)