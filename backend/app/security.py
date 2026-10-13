# from passlib.context import CryptContext
import jwt
import bcrypt
from datetime import datetime,timedelta,timezone

from app.config import settings

# crypt_context=CryptContext(schemes=['bcrypt'],deprecated="auto")

def get_hash_password(password):
    # return crypt_context.hash(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"),salt)
    return hashed.decode()

def verify_hash_password(plain_password,hashed_password):
    # return crypt_context.verify(plain_password,hashed_password)
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(user_id:int,role:str)->str:
     """
     生成 JWT。
     payload 只放 user_id 和 role，不放任何敏感信息。
     """
     # 过期时间 = 当前时间 + 配置的有效期（分钟）
     expire = datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
     payload = {
         "user_id":user_id,
         "role":role,
         "exp":expire
     }

     token = jwt.encode(
         payload,
         settings.secret_key,
         algorithm=settings.jwt_algorithm
     )
     return token

def decode_token(token:str) ->dict|None:
    try:
        payload=jwt.decode(
            token,
            settings.secret_key,
            algorithms=settings.jwt_algorithm
        )
        return payload
    except:
        return None
         
        





