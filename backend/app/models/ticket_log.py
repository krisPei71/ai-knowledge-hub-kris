from datetime import datetime

from sqlalchemy import ForeignKey, String
from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column

class TicketLog(Base):
    __tablename__="ticket_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), index=True)
    from_status: Mapped[str] = mapped_column(String(20))
    to_status: Mapped[str] = mapped_column(String(20))
    operator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    remark: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
