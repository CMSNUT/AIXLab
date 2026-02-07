# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchemaModify, UserBySchema

class PlotScriptCreateSchema(BaseModel):
    """
    绘图脚本管理新增模型
    """
    name: str  | None = Field(default=None, description='绘图脚本名称')
    alias: str  | None = Field(default=None, description='脚本英文名称')
    order: int  | None = Field(default=None, description='脚本序号')
    service: str  | None = Field(default=None, description='软件版本')
    field: str  | None = Field(default=None, description='应用领域')
    category: str  | None = Field(default=None, description='功能类别')
    image: str  | None = Field(default=None, description='脚本图标')
    description: str  | None = Field(default=None, description='功能描述')


class PlotScriptUpdateSchema(PlotScriptCreateSchema):
    """
    绘图脚本管理更新模型
    """
    ...


class PlotScriptOutSchema(PlotScriptCreateSchema, BaseSchemaModify, UserBySchema):
    """
    绘图脚本管理响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class PlotScriptQueryParam:
    """绘图脚本管理查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="绘图脚本名称"),
        alias: str | None = Query(None, description="脚本英文名称"),
        category: str | None = Query(None, description="功能类别"),
        description: str | None = Query(None, description="功能描述"),
        order: int | None = Query(None, description="脚本序号"),
        service: str | None = Query(None, description="软件版本"),
        field: str | None = Query(None, description="应用领域"),
        image: str | None = Query(None, description="脚本图标"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 模糊查询字段
        self.name = ("like", name)
        # 模糊查询字段
        self.alias = ("like", alias)
        # 精确查询字段
        self.order = order
        # 精确查询字段
        self.service = service
        # 精确查询字段
        self.field = field
        # 模糊查询字段
        self.category = ("like", category)
        # 精确查询字段
        self.image = image
        # 模糊查询字段
        self.description = ("like", description)
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
