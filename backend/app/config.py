import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # 应用配置
    APP_NAME = "AIXLAB Backend"
    VERSION = "1.0.0"
    
    # 数据库配置
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://aikemi:snut3426@localhost:3306/aixlab")
    
    # JWT配置
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # 其他服务URL
    PYAPI_URL = os.getenv("PYAPI_URL", "http://localhost:8001")
    RAPI_URL = os.getenv("RAPI_URL", "http://localhost:8002")

settings = Settings()