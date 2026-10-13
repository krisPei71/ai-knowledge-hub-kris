from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from app.config import settings

engine = create_engine(
    settings.database_url,
    connect_args = { "check_same_thread":False}
    if settings.database_url.startswith('sqlite')
    else {},#允许多线程访问 
    echo = False # 改成 True 会在控制台打印每条 SQL，调试很有用，平时关掉
)

# 会话工厂，每次调用，拿到数据库会话
SessionLocal = sessionmaker(
    autocommit =False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def getdb():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()