
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import trades

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trades.router)

@app.get("/ping")
def ping():
    return {"message": "Backend is alive!"}
