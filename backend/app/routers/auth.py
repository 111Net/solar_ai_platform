from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.get("/test")
def auth_test():
    return {"message": "Auth router working"}


@router.post("/register")
def register(user: RegisterRequest):
    return {
        "message": "User registered successfully",
        "email": user.email,
        "full_name": user.full_name
    }


@router.post("/login")
def login(user: LoginRequest):
    return {
        "message": "Login successful",
        "email": user.email,
        "token": "demo-token"
    }