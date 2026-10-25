from pathlib import Path
from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    # # 读根目录的env文件
    # model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")

    # 数据库连接串：字段名 database_url 会自动匹配环境变量 DATABASE_URL
    # 给了默认值，即使 .env 里没写也能用
    database_url:str="sqlite:///./ticket_hub.db"

    # JWT 密钥：不给默认值 = 必填，.env 里没有就启动报错（这是好事，fail fast）
    secret_key:str

     # 算法和有效期给默认值
    jwt_algorithm:str = "HS256"
    access_token_expire_minutes:int = 1440

    ai_provider:str="openai"
    ai_api_key:str="sk-1538ffb903644152981757939c72e5c6"
    ai_base_url:str="https://api.deepseek.com"
    ai_model:str="deepseek-flash"

    embedding_provider: str = "mock"  # mock / openai
    embedding_dimension: int = 128    # 向量维度

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"


settings = Settings()