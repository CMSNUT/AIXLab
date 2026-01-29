# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class RscLiteratureCreateSchema(BaseModel):
    """
    文献管理新增模型
    """
    status: str = Field(default="0", description='是否启用(0:启用 1:禁用)')
    type: str = Field(default=..., description='文章类型，如期刊论文、会议论文等')
    title: str = Field(default=..., description='标题')
    source: str = Field(default=..., description='期刊/会议名称')
    year: int = Field(default=..., description='年份')
    volume: str = Field(default=..., description='卷')
    issue: str = Field(default=..., description='期')
    pages: str = Field(default=..., description='页码')
    doi: str = Field(default=..., description='DOI标识')
    pmid: str = Field(default=..., description='PubMed ID')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')


class RscLiteratureUpdateSchema(RscLiteratureCreateSchema):
    """
    文献管理更新模型
    """
    ...


class RscLiteratureOutSchema(RscLiteratureCreateSchema, BaseSchema, UserBySchema):
    """
    文献管理响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class RscLiteratureQueryParam:
    """文献管理查询参数"""

    def __init__(
        self,
        description: str | None = Query(None, description="备注/描述"),
        status: str | None = Query(None, description="是否启用(0:启用 1:禁用)"),
        type: str | None = Query(None, description="文章类型，如期刊论文、会议论文等"),
        title: str | None = Query(None, description="标题"),
        source: str | None = Query(None, description="期刊/会议名称"),
        year: int | None = Query(None, description="年份"),
        volume: str | None = Query(None, description="卷"),
        issue: str | None = Query(None, description="期"),
        pages: str | None = Query(None, description="页码"),
        doi: str | None = Query(None, description="DOI标识"),
        pmid: str | None = Query(None, description="PubMed ID"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.status = status
        # 精确查询字段
        self.type = type
        # 精确查询字段
        self.title = title
        # 精确查询字段
        self.source = source
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
