# -*- coding: utf-8 -*-

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchemaModify, UserBySchema

class LabPlotCreateSchema(BaseModel):
    """
    绘图工具管理新增模型
    """
    name: str  | None = Field(default=None, description='绘图模块名称')
    code: str  | None = Field(default=None, description='模块英文名称')
    field: str  | None = Field(default=None, description='领域')
    category: str  | None = Field(default=None, description='类别')
    description: str  | None = Field(default=None, description='备注/描述')
    image: str  | None = Field(default=None, description='图片')


class LabPlotUpdateSchema(LabPlotCreateSchema):
    """
    绘图工具管理更新模型
    """
    ...


class LabPlotOutSchema(LabPlotCreateSchema, BaseSchemaModify, UserBySchema):
    """
    绘图工具管理响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class LabPlotQueryParam:
    """绘图工具管理查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="绘图模块名称"),
        code: str | None = Query(None, description="模块英文名称"),
        description: str | None = Query(None, description="备注/描述"),
        field: str | None = Query(None, description="领域"),
        category: str | None = Query(None, description="类别"),
        image: str | None = Query(None, description="图片"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 模糊查询字段
        self.name = ("like", name)
        # 模糊查询字段
        self.code = ("like", code)
        # 精确查询字段
        self.field = field
        # 精确查询字段
        self.category = category
        # 模糊查询字段
        self.description = ("like", description)
        # 精确查询字段
        self.image = image
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))

class LabPlotAddSchema(BaseModel):
    """
    加法运算请求参数（和model层CalculationRequest对齐）
    """
    a: Optional[float] = Field(default=None, description='第1个数（数字类型）')
    b: Optional[float] = Field(default=None, description='第2个数（数字类型）')

class BaseResponse(BaseModel):
    """基础响应模型（匹配前端ApiResponse）"""
    code: int
    data: Any
    msg: str
    status_code: int
    success: bool

class SuccessResponseXXX(BaseResponse):
    """成功响应模型"""
    success: bool = True
    code: int = 200
    status_code: int = 200

class ErrorResponseXXX(BaseResponse):
    """错误响应模型"""
    success: bool = False
    data: Optional[Any] = None
    