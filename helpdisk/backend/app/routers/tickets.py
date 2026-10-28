from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Ticket, Role
from ..schemas import TicketIn, TicketOut, TicketUpdate
from ..deps import CurrentUser, require_roles

router = APIRouter(prefix="/tickets", tags=["tickets"])
DB = Annotated[Session, Depends(get_db)]

TEMP_AUTOR_ID = 1

@router.get("", response_model=list[TicketOut])
def list_tickets(db: DB, user: CurrentUser):
    query = select(Ticket).order_by(Ticket.created_at.desc())
    if user.role == Role.user:
        query = query.where(Ticket.author_id == user.id)
    return db.scalars(query).all()

@router.post("", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(data: TicketIn, db: DB, user: CurrentUser):
    ticket = Ticket(**data.model_dump(), author_id=user.id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@router.patch(
    "/{ticket_id}",
    response_model=TicketOut,
    dependencies=[Depends(require_roles(Role.agent, Role.admin))],
)
def update_ticket(ticket_id: int, data: TicketUpdate, db: DB):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Ticket no encontrado")
    ticket.status = data.status
    db.commit()
    db.refresh(ticket)
    return ticket

@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(Role.admin))],
)
def delete_ticket(ticket_id: int, db: DB):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Ticket no encontrado")
    db.delete(ticket)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)