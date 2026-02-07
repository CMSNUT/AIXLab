# -*- coding: utf-8 -*-

import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class LabPlotModel(ModelMixinModify, UserMixin):
    """
    绘图工具管理表
    """
    __tablename__: str = 'lab_plot'
    __table_args__: dict[str, str] = {'comment': '绘图工具管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='绘图模块名称')
    code: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='模块英文名称')
    field: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='领域')
    category: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='类别')
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment='备注/描述')
    image: Mapped[str | None] = mapped_column(Text, nullable=True, comment='图片')

class CalculationRequest(BaseModel):
    """计算请求模型"""
    a: float = Field(..., description="第一个数字", ge=-999999, le=999999)
    b: float = Field(..., description="第二个数字", ge=-999999, le=999999)
    
    @field_validator('a', 'b')
    def validate_numbers(cls, v):
        if abs(v) > 999999:
            raise ValueError('数字不能超过999999')
        return v

class BatchOperation(BaseModel):
    """批量操作"""
    type: str = Field(..., description="操作类型: add, multiply")
    a: float
    b: float

class BatchRequest(BaseModel):
    """批量请求"""
    operations: List[BatchOperation]    





