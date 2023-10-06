from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


#usage:
#python -m uvicorn source_files.proxyWebserverTest:app