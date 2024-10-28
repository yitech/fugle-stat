from fastapi import FastAPI


app = FastAPI()


@app.get("/api/v1/ping", tags=["System"])
def ping():
    return {"result": "pong"}


