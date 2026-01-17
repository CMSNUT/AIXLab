from pydantic import BaseSettings

class Settings(BaseSettings):
    # 主后端的API地址，用于通信
    BACKEND_API_URL: str = "http://localhost:8000"
    
    # 数据库配置（如果需要直接访问）
    DATABASE_URL: str = "mysql+pymysql://aikemi:snut3426@localhost:3306/aixlab"

    class Config:
        env_file = ".env"

settings = Settings()