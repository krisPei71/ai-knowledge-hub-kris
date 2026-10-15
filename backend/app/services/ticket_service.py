from fastapi import HTTPException,status as http_status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.ticket import Ticket
from app.models.ticket_log import TicketLog

from app.schemas.tickets import TicketStatusUpdate,TicketLogOut

# =========================================================
# 状态机定义
# =========================================================
# key: (from_status, to_status) 元组
# value: 规则字典

STATE_MACHINE:dict[tuple[str,str],dict]={
    ('pending','processing'):{
        "roles":["handler","admin"],
        "require_creator":False,
        "require_assignee":False,
        "auto_assign":True,
        "remark_required":False
    },
    ('processing','resolved'):{
        "roles":["handler","admin"],
        "require_creator":False,
        "require_assignee":True,
        "auto_assign":False,
        "remark_required":False
    },
    ('resolved','closed'):{
        "roles":["reporter","admin"],
        "require_creator":True,
        "require_assignee":False,
        "auto_assign":False,
        "remark_required":False
    },
    ('resolved','processing'):{
        "roles":["reporter","admin"],
        "require_creator":True,
        "require_assignee":False,
        "auto_assign":False,
        "remark_required":True
    },
}

def translation_status(
        db:Session,
        ticket_id:int,
        data:TicketStatusUpdate,
        current_user:User
)->Ticket:
    # 1.先验证工单是否存在
    ticket = db.get(Ticket,ticket_id)
    if ticket is None:
       raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND,detail="工单不存在")
    
    from_status= ticket.status
    to_status = data.to_status

    # 检查当前状态，如果已经是目标状态，直接返回工单信息
    # 防重复认领
    if(from_status == to_status):
       return ticket

    # 2.验证要修改的状态是否在允许的范围内
    rule= STATE_MACHINE.get((from_status,to_status))
    if rule is None:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST,detail=f"非法状态流转：{from_status}->{to_status}")
    
    # 3.验证所属角色是否有权利处理
    if current_user.role!='admin' and current_user.role not in rule['roles']:
        raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN,detail="所属角色无权限处理")
    
    # 4.验证登录人是否是创建者
    if rule['require_creator'] and current_user.id != ticket.creator_id:
       if current_user.role != "admin":
        raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN,detail="只有提单人可处理")
    
    # 5.验证登录人是否是处理者
    if rule['require_assignee'] and current_user.id != ticket.assignee_id:
       if current_user.role != "admin":
        raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN,detail="只有处理人可处理")
    
    # 6.验证备注是否空
    if rule['remark_required'] and not(data.remark and data.remark.strip()):
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST,detail="备注必填")
    
    # 7.执行变更
    updated_value={"status":to_status}
    # ticket.status=to_status
    if(rule["auto_assign"]) and not ticket.assignee_id:
       updated_value["assignee_id"]=current_user.id
    rows = db.query(Ticket).filter(Ticket.id == ticket_id,Ticket.status==from_status).update(updated_value,synchronize_session=False)
    if rows == 0:
       db.rollback()
       raise HTTPException(
        status_code=http_status.HTTP_409_CONFLICT,
        detail="工单状态已被其他人修改，请刷新后重试",
    )
    # 8.写日志
    db.add(TicketLog(
       ticket_id=ticket.id,
       from_status=from_status,
       to_status=to_status,
       operator_id=current_user.id,
       remark=data.remark,
    ))
    db.commit()
    db.refresh(ticket)
    return ticket
