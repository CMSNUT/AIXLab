# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class ResourceScriptCreateSchema(BaseModel):
    """
    脚本新增模型
    """
    status: str = Field(default="0", description='是否启用')
    name: str = Field(default=..., description='脚本名称')
    type: str = Field(default=..., description='脚本类型')
    language: str = Field(default=..., description='编程语言')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')
    local_path: str = Field(default=..., description='本地存储路径')
    network_url: str = Field(default=..., description='网络地址')
    cloud_url: str = Field(default=..., description='网盘地址')


class ResourceScriptUpdateSchema(ResourceScriptCreateSchema):
    """
    脚本更新模型
    """
    ...


class ResourceScriptOutSchema(ResourceScriptCreateSchema, BaseSchema, UserBySchema):
    """
    脚本响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class ResourceScriptQueryParam:
    """脚本查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="脚本名称"),
        description: str | None = Query(None, description="备注/描述"),
        status: str | None = Query(None, description="是否启用"),
        type: str | None = Query(None, description="脚本类型"),
        language: str | None = Query(None, description="编程语言"),
        local_path: str | None = Query(None, description="本地存储路径"),
        network_url: str | None = Query(None, description="网络地址"),
        cloud_url: str | None = Query(None, description="网盘地址"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.status = status
        # 模糊查询字段
        self.name = ("like", name)
        # 精确查询字段
        self.type = type
        # 精确查询字段
        self.language = language
        # 模糊查询字段
        self.description = ("like", description)
        # 精确查询字段
        self.local_path = local_path
        # 精确查询字段
        self.network_url = network_url
        # 精确查询字段
        self.cloud_url = cloud_url
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
