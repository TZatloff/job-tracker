import secrets
from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from config import API_TOKEN, ADMIN_USER, ADMIN_PASSWORD

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


class LoginIn(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(creds: LoginIn):
    if creds.username != ADMIN_USER or creds.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    return {"token": API_TOKEN}


def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )

    token = authorization.split(" ")[1]
    if not secrets.compare_digest(token, API_TOKEN):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
