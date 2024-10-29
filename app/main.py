from fastapi import FastAPI
from app.api.v1 import statistic


app = FastAPI()

app.include_router(statistic.router, prefix="/api/v1", tags=["Statistic"])


@app.get("/api/v1/ping", tags=["System"])
def ping():
    return {"result": "pong"}


