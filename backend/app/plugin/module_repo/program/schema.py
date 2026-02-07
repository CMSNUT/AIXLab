# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchemaModify, UserBySchema

class RepoProgramCreateSchema(BaseModel):
    """
    代码仓库管理新增模型
    """
    name: str  | None = Field(default=None, description='代码仓库名称')
    alias: str  | None = Field(default=None, description='代码英文名称')
    language: str  | None = Field(default=None, description='代码语言')
    field: str  | None = Field(default=None, description='应用领域')
    category: str  | None = Field(default=None, description='功能类别')
    description: str  | None = Field(default=None, description='功能描述')
    local_file: str  | None = Field(default=None, description='本地文件')
    url_link: str  | None = Field(default=None, description='网络地址')
    cloud_link: str  | None = Field(default=None, description='网盘链接')


class RepoProgramUpdateSchema(RepoProgramCreateSchema):
    """
    代码仓库管理更新模型
    """
    ...


class RepoProgramOutSchema(RepoProgramCreateSchema, BaseSchemaModify, UserBySchema):
    """
    代码仓库管理响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class RepoProgramQueryParam:
    """代码仓库管理查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="代码仓库名称"),
        alias: str | None = Query(None, description="代码英文名称"),
        category: str | None = Query(None, description="功能类别"),
        description: str | None = Query(None, description="功能描述"),
        language: str | None = Query(None, description="代码语言"),
        field: str | None = Query(None, description="应用领域"),
        local_file: str | None = Query(None, description="本地文件"),
        url_link: str | None = Query(None, description="网络地址"),
        cloud_link: str | None = Query(None, description="网盘链接"),
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
        self.language = language
        # 精确查询字段
        self.field = field
        # 模糊查询字段
        self.category = ("like", category)
        # 模糊查询字段
        self.description = ("like", description)
        # 精确查询字段
        self.local_file = local_file
        # 精确查询字段
        self.url_link = url_link
        # 精确查询字段
        self.cloud_link = cloud_link
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
