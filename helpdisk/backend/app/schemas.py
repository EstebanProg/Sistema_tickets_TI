from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from .models import Priority, TicketStatus, Role


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class RegisterIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72) 


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(ORM):
    id: int
    name: str
    email: str
    role: Role
    is_active: bool


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class AuthorOut(ORM):
    id: int
    name: str

class TicketIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str
    priority: Priority = Priority.medium

class TicketUpdate(BaseModel):
    status: TicketStatus

class TicketOut(ORM):
    id: int
    title: str
    description: str
    priority: Priority
    status: TicketStatus
    created_at: datetime
    author: AuthorOut

class UserUpdate(BaseModel):
    role: Role | None = None
    is_active: bool | None = None

