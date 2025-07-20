
from fastapi import FastAPI
from routers import trades
from db_setup import Base, engine
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(trades.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
