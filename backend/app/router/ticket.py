from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm  import Session

from app.database import getdb
from app.deps import get_current_user
from app.models.ticket import Ticket
from app.models.user import User
from app.models.ticket_log import TicketLog
from app.schemas.tickets import TicketCreate,TicketList,TicketOut

router = APIRouter(prefix='/api/tickets',tags=['工单'])

@router.get('',response_model=TicketList)
def list_tickets(
    status: str | None = None,
    priority: str | None = None,
    keyword: str | None = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Ticket)
    if(status):
        query=query.filter(Ticket.status==status)
    if(priority):
        query=query.filter(Ticket.priority==priority)
    if(keyword):
        query=query.filter(
            Ticket.title.like(f"%{keyword}%") | Ticket.description.like(f"%{keyword}%")
        )

    total = query.count()
    tickets=(
        query.order_by(Ticket.created_at.desc()).offset((page-1)*page_size).limit(page_size).all()
    )
    items=[]
    for t in tickets:
        creator = db.query(User).get(t.creator_id)
        assignee = db.query(User).get(t.assignee_id) if t.assignee_id else None
        items.append(
            TicketOut(
                **{k:v for k,v in t.__dict__.items() if not k.startswith('-')},
                creator_username=creator.username if creator else '未知',
                assignee_username=assignee.username if assignee else '未知'
            )
        )
    return TicketList(total=total,items=items)

@router.post("", response_model=TicketOut)
def create_ticket(
    data: TicketCreate,
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user),
):
    ticket = Ticket(
        title=data.title,
        description=data.description,
        status="pending",
        priority="medium",
        creator_id=current_user.id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # 日志
    db.add(TicketLog(
        ticket_id=ticket.id,
        from_status="",
        to_status="pending",
        operator_id=current_user.id,
        remark="创建工单",
    ))
    db.commit()

    return TicketOut(
        **{k: v for k, v in ticket.__dict__.items() if not k.startswith("_")},
        creator_username=current_user.username,
        assignee_username=None,
    )