from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import getdb
from app.models.user import User
from app.security import decode_token

bearer_schema = HTTPBearer()

def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(bearer_schema),db:Session=Depends(getdb))->User:
    token=credentials.credentials #提取token字符串
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效或过期"
        )
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token格式错误"
        )
    
    user = db.query(User).filter(User.id==user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    
    return user

def require_role(*allow_roles:str):
    def checker(curren_user:User=Depends(get_current_user)):
        if curren_user.role not in allow_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        return curren_user
    return checker
    