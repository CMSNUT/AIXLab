# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class ResourceCorpusCreateSchema(BaseModel):
    """
    语料新增模型
    """
    status: str = Field(default="0", description='是否启用')
    paper_id: int = Field(default=..., description='文献ID')
    section: str = Field(default=..., description='文章章节')
    content_en: str = Field(default=..., description='英文内容')
    content_cn: str = Field(default=..., description='中文内容')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')


class ResourceCorpusUpdateSchema(ResourceCorpusCreateSchema):
    """
    语料更新模型
    """
    ...


class ResourceCorpusOutSchema(ResourceCorpusCreateSchema, BaseSchema, UserBySchema):
    """
    语料响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class ResourceCorpusQueryParam:
    """语料查询参数"""

    def __init__(
        self,
        content_en: str | None = Query(None, description="英文内容"),
        content_cn: str | None = Query(None, description="中文内容"),
        description: str | None = Query(None, description="备注/描述"),
        status: str | None = Query(None, description="是否启用"),
        paper_id: int | None = Query(None, description="文献ID"),
        section: str | None = Query(None, description="文章章节"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.status = status
        # 精确查询字段
        self.paper_id = paper_id
        # 精确查询字段
        self.section = section
        # 模糊查询字段
        self.content_en = ("like", content_en)
        # 模糊查询字段
        self.content_cn = ("like", content_cn)
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
