
from fastapi import FastAPI
from routers import trades

app = FastAPI()
app.include_router(trades.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
