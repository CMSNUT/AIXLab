import pymysql
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 数据库连接
DATABASE_URL = "mysql+pymysql://aikemi:snut3426@mysql:3306/aixlab"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 分析任务模型
class AnalysisTask(Base):
    __tablename__ = "analysis_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    backend = Column(String(10))  # python 或 R
    task_type = Column(String(20))  # view, cluster, plot
    parameters = Column(JSON)
    status = Column(String(20), default="pending")
    result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

# 创建表
Base.metadata.create_all(bind=engine)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()