from fastapi import APIRouter,Depends,Query,HTTPException,status as http_status
from sqlalchemy.orm  import Session

from app.database import getdb
from app.deps import get_current_user
from app.models.ticket import Ticket
from app.models.user import User
from app.models.ticket_log import TicketLog
from app.schemas.tickets import TicketCreate,TicketList,TicketOut,TicketLogOut,TicketStatusUpdate
from app.services.ticket_service import translation_status
from app.schemas.ai import KnowledgeFromTicketRequest,KnowledgeOut
from app.services.ai.knowledge_service import create_knowledge_from_ticket

router = APIRouter(prefix='/api/tickets',tags=['工单'])


# 工单列表
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
    # 数据隔离，普通员工只能看到自己的，其他可以看到全部的
    if(current_user.role =='reporter'):
        query = query.filter(Ticket.creator_id == current_user.id)
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

# 创建工单
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
        priority=data.priority or "medium",
        category=data.category,
        ai_category_raw=data.ai_category_raw,
        ai_confidence=data.ai_confidence,
        ai_summary=data.ai_summary,
        creator_id=current_user.id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    out = TicketOut(
        **{k: v for k, v in ticket.__dict__.items() if not k.startswith("_")},
        creator_username=current_user.username,
        assignee_username=None,
    )
    # 日志
    db.add(TicketLog(
        ticket_id=ticket.id,
        from_status="",
        to_status="pending",
        operator_id=current_user.id,
        remark="创建工单",
    ))
    db.commit()

    return out

# 工单详情
@router.get("/{ticket_id}",response_model=TicketOut)
def get_ticket_detail(
    ticket_id:int,
    db:Session=Depends(getdb),
    current_user:User=Depends(get_current_user)
):
    ticket = db.get(Ticket,ticket_id)
    if ticket is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND,detail="工单不存在")
    if current_user.role =='reporter' and ticket.creator_id!=current_user.id:
        raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN,detail="只能查看自己创建的工单")
    creator = db.get(User, ticket.creator_id)
    assignee = db.get(User, ticket.assignee_id) if ticket.assignee_id else None
    out=TicketOut(
        **{k:v for k,v in ticket.__dict__.items() if not k.startswith("_")},
        creator_username=creator.username if creator else '未知',
        assignee_username=assignee.username if assignee else None
    )

    return out

# 更新工单状态
@router.patch("/{ticket_id}/status",response_model=TicketOut)
def update_ticket_status(
    ticket_id:int,
    data: TicketStatusUpdate,
    db:Session=Depends(getdb),
    current_user:User=Depends(get_current_user)
):
    ticket = translation_status(db,ticket_id,data,current_user)
    creator = db.get(User,ticket.creator_id)
    assignee  = db.get(User,ticket.assignee_id) if ticket.assignee_id else None

    out=TicketOut(
        **{k:v for k,v in ticket.__dict__.items() if not k.startswith("_")},
        creator_username=creator.username if creator else '未知',
        assignee_username=assignee.username if assignee else None
    )

    return out

# 工单日志
@router.get("/{ticket_id}/logs",response_model=list[TicketLogOut])
def get_ticket_log(
    ticket_id:int,
    db:Session=Depends(getdb),
    current_user:User=Depends(get_current_user)
):
    ticket = db.get(Ticket,ticket_id)
    if ticket is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND,detail="工单不存在")
    
    logs=(
        db.query(TicketLog).filter(TicketLog.ticket_id == ticket_id).order_by(TicketLog.created_at.asc()).all()
    )
    result = []
    for log in logs:
        operator = db.get(User,log.operator_id)
        result.append(
            TicketLogOut(
                **{k:v for k,v in log.__dict__.items() if not k.startswith("_")},
                operator_username=operator.username if operator else '未知'
            )
        )
    return result

@router.post("/{ticket_id}/to-knowledge",response_model=KnowledgeOut)
async def ticket_to_knowledge(ticket_id:int,data:KnowledgeFromTicketRequest,db:Session=Depends(getdb),user:User=Depends(get_current_user)):
    try:
        knowledge=await create_knowledge_from_ticket(ticket_id,data.solution,db,user)
        return knowledge
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
