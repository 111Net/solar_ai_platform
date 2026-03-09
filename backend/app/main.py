from fastapi import FastAPI
from app.routers import auth

app = FastAPI(
    title="Solar AI Platform",
    description="Solar-as-a-Service API for cooperatives",
    version="1.0.0"
)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Solar AI Platform API running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}