from datetime import datetime
from sqlalchemy import Float, ForeignKey, Integer, String, Text
from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column


class Ticket(Base):
    __tablename__ = 'tickets'

    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    title:Mapped[str]=mapped_column(String(255))
    description:Mapped[str]=mapped_column(Text)

    status:Mapped[str]=mapped_column(String(20),default="pending",index=True)
    priority:Mapped[str]=mapped_column(String(10),default="medium",index=True)
    category:Mapped[str | None]=mapped_column(String(50),index=True)

    ai_summary:Mapped[str | None]=mapped_column(Text)
    ai_confidence:Mapped[float |None]=mapped_column(Float)
    ai_category_raw:Mapped[str | None]=mapped_column(String(50))

    creator_id:Mapped[int] = mapped_column(Integer,ForeignKey("users.id"),index=True)
    assignee_id:Mapped[int | None] = mapped_column(Integer,ForeignKey("users.id"),index=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )



