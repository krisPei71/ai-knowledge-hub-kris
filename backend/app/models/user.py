from datetime import datetime
from sqlalchemy import Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column

class User(Base):
    __tablename__ = 'users'

    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    username:Mapped[str] = mapped_column(String(50),nullable=False,index=True,unique=True)
    password_hash:Mapped[str] = mapped_column(String(255),nullable=False)
    role:Mapped[str] = mapped_column(String(50),default='admin')
    created_at:Mapped[datetime] = mapped_column(default=datetime.utcnow)