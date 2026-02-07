# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchemaModify, UserBySchema

class PlotMethodCreateSchema(BaseModel):
    """
    绘图方法管理新增模型
    """
    description: str  | None = Field(default=None, description='方法描述')
    order: int  | None = Field(default=None, description='方法步骤')
    script_id: int  | None = Field(default=None, description='脚本主键ID')


class PlotMethodUpdateSchema(PlotMethodCreateSchema):
    """
    绘图方法管理更新模型
    """
    ...


class PlotMethodOutSchema(PlotMethodCreateSchema, BaseSchemaModify, UserBySchema):
    """
    绘图方法管理响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class PlotMethodQueryParam:
    """绘图方法管理查询参数"""

    def __init__(
        self,
        description: str | None = Query(None, description="方法描述"),
        order: int | None = Query(None, description="方法步骤"),
        script_id: int | None = Query(None, description="脚本主键ID"),
        created_id: int | None = Query(None, description="创建人ID（关联sys_user表）"),
        updated_id: int | None = Query(None, description="更新人ID（关联sys_user表）"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 模糊查询字段
        self.description = ("like", description)
        # 精确查询字段
        self.order = order
        # 精确查询字段
        self.script_id = script_id
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
