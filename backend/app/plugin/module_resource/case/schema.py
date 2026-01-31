# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class ResourceCaseCreateSchema(BaseModel):
    """
    案例新增模型
    """
    status: str = Field(default="0", description='是否启用')
    name: str = Field(default=..., description='案例名称')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')
    content: str = Field(default=..., description='内容')
    paper_id: int = Field(default=..., description='文献ID')


class ResourceCaseUpdateSchema(ResourceCaseCreateSchema):
    """
    案例更新模型
    """
    ...


class ResourceCaseOutSchema(ResourceCaseCreateSchema, BaseSchema, UserBySchema):
    """
    案例响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class ResourceCaseQueryParam:
    """案例查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="案例名称"),
        description: str | None = Query(None, description="备注/描述"),
        content: str | None = Query(None, description="内容"),
        status: str | None = Query(None, description="是否启用"),
        paper_id: int | None = Query(None, description="文献ID"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.status = status
        # 模糊查询字段
        self.name = ("like", name)
        # 模糊查询字段
        self.description = ("like", description)
        # 模糊查询字段
        self.content = ("like", content)
        # 精确查询字段
        self.paper_id = paper_id
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
