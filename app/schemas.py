from uuid import UUID
from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class UserOut(BaseModel):
    id: UUID
    email: str


class SystemUser(UserOut):
    password: str


class Alert(BaseModel):
    crypto_code: str
    trigger_price: float


class AlertAllOut(BaseModel):
    alert_id: int
    crypto_code: str
    trigger_price: float
    status: str