# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchemaModify, UserBySchema

class ResourcePaperCreateSchema(BaseModel):
    """
    文献新增模型
    """
    type: str  | None = Field(default=None, description='文章类型')
    field: str  | None = Field(default=None, description='文章领域')
    title: str  | None = Field(default=None, description='标题')
    source: str  | None = Field(default=None, description='期刊/会议名称')
    year: int  | None = Field(default=None, description='年份')
    volume: str  | None = Field(default=None, description='卷')
    issue: str  | None = Field(default=None, description='期')
    pages: str  | None = Field(default=None, description='页码')
    doi: str  | None = Field(default=None, description='DOI')
    pmid: str  | None = Field(default=None, description='PubMed ID')
    description: str  | None = Field(default=None, description='备注/描述')


class ResourcePaperUpdateSchema(ResourcePaperCreateSchema):
    """
    文献更新模型
    """
    ...


class ResourcePaperOutSchema(ResourcePaperCreateSchema, BaseSchemaModify, UserBySchema):
    """
    文献响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class ResourcePaperQueryParam:
    """文献查询参数"""

    def __init__(
        self,
        title: str | None = Query(None, description="标题"),
        source: str | None = Query(None, description="期刊/会议名称"),
        description: str | None = Query(None, description="备注/描述"),
        type: str | None = Query(None, description="文章类型"),
        field: str | None = Query(None, description="文章领域"),
        year: int | None = Query(None, description="年份"),
        volume: str | None = Query(None, description="卷"),
        issue: str | None = Query(None, description="期"),
        pages: str | None = Query(None, description="页码"),
        doi: str | None = Query(None, description="DOI"),
        pmid: str | None = Query(None, description="PubMed ID"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.type = type
        # 精确查询字段
        self.field = field
        # 模糊查询字段
        self.title = ("like", title)
        # 模糊查询字段
        self.source = ("like", source)
        # 精确查询字段
        self.year = year
        # 精确查询字段
        self.volume = volume
        # 精确查询字段
        self.issue = issue
        # 精确查询字段
        self.pages = pages
        # 精确查询字段
        self.doi = doi
        # 精确查询字段
        self.pmid = pmid
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
