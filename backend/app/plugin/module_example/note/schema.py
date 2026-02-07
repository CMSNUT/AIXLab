# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchemaModify, UserBySchema

class ExampleNoteCreateSchema(BaseModel):
    """
    案例分析笔记管理新增模型
    """
    name: str  | None = Field(default=None, description='笔记名称')
    description: str  | None = Field(default=None, description='笔记内容')
    analysis_id: int  | None = Field(default=None, description='案例分析ID')


class ExampleNoteUpdateSchema(ExampleNoteCreateSchema):
    """
    案例分析笔记管理更新模型
    """
    ...


class ExampleNoteOutSchema(ExampleNoteCreateSchema, BaseSchemaModify, UserBySchema):
    """
    案例分析笔记管理响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class ExampleNoteQueryParam:
    """案例分析笔记管理查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="笔记名称"),
        description: str | None = Query(None, description="笔记内容"),
        analysis_id: int | None = Query(None, description="案例分析ID"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 模糊查询字段
        self.name = ("like", name)
        # 模糊查询字段
        self.description = ("like", description)
        # 精确查询字段
        self.analysis_id = analysis_id
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
