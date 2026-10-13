from fastapi import APIRouter,Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.database import getdb
from app.security import get_hash_password,verify_hash_password,create_access_token
from app.deps import get_current_user
from app.models.user import User
from app.schemas.user import LoginRequest,Token,UserOut

router = APIRouter(prefix="/api/auth",tags=["认证"])

@router.post("/login",response_model=Token)
def login(data:LoginRequest,db:Session=Depends(getdb)):
    # 登录校验用户名密码
    user = db.query(User).filter(User.username==data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")

    if not verify_hash_password(data.password,user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    # 生成token
    token = create_access_token(user_id=user.id,role=user.role)
    return Token(access_token=token,token_type="bearer")
@router.get("/me",response_model=UserOut)
def get_me(current_user:User=Depends(get_current_user)):
    # 返回当前用户登录信息
    return current_user
