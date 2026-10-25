# app/routers/stats.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import getdb
from app.deps import get_current_user
from app.models import Ticket, User

router = APIRouter(prefix="/api/stats", tags=["数据统计"])

@router.get("/overview")
def get_overview(
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user),
):
    # 1. 基础工单数量
    total = db.query(Ticket).count()
    pending = db.query(Ticket).filter(Ticket.status == "pending").count()
    resolved = db.query(Ticket).filter(Ticket.status.in_(["resolved", "closed"])).count()

    # 2. 分类分布 (饼图数据)
    category_stats = db.query(Ticket.category, func.count(Ticket.id))\
        .filter(Ticket.category.isnot(None))\
        .group_by(Ticket.category).all()
    category_data = [{"name": c[0], "value": c[1]} for c in category_stats]

    # 3. AI 准确率计算逻辑
    # 只有当用户没有修改过 AI 的分类时（即 ai_category_raw == category），才算 AI 判对
    ai_total = db.query(Ticket).filter(Ticket.ai_category_raw.isnot(None)).count()
    ai_correct = db.query(Ticket).filter(
        Ticket.ai_category_raw.isnot(None),
        Ticket.ai_category_raw == Ticket.category
    ).count()
    
    ai_accuracy = round((ai_correct / ai_total * 100), 1) if ai_total > 0 else 0

    return {
        "total": total,
        "pending": pending,
        "resolved": resolved,
        "ai_accuracy": ai_accuracy,
        "category_data": category_data,
    }