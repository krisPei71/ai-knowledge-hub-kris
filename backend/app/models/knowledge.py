# app/models/knowledge.py
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Knowledge(Base):
    __tablename__ = "knowledge"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    
    # 来源工单 ID（如果这篇知识是由工单生成的，就记录在这里）
    source_ticket_id: Mapped[int | None] = mapped_column(ForeignKey("tickets.id"), nullable=True)
    
    # 状态：draft(草稿) / published(已发布)
    status: Mapped[str] = mapped_column(String(20), default="published", index=True)
    
    # ⭐ 核心：存储向量。MVP 阶段用 JSON 字符串存，D5 可换 pgvector
    embedding: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )