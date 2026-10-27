from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from .models import Priority, TicketStatus


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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