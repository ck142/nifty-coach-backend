# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.trades import router as trades_router
from db_setup import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

# Init app
app = FastAPI()

# CORS config for frontend-backend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(trades_router)

# Health check
@app.get("/ping")
def ping():
    return {"message": "pong"}
