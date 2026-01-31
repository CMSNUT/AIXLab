# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class ResourceChartCreateSchema(BaseModel):
    """
    图表新增模型
    """
    status: str = Field(default="0", description='是否启用')
    paper_id: int = Field(default=..., description='文献ID')
    name: str = Field(default=..., description='图表名称')
    code: str = Field(default=..., description='图表编号')
    local_path: str = Field(default=..., description='本地存储路径')
    network_url: str = Field(default=..., description='网络地址')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')


class ResourceChartUpdateSchema(ResourceChartCreateSchema):
    """
    图表更新模型
    """
    ...


class ResourceChartOutSchema(ResourceChartCreateSchema, BaseSchema, UserBySchema):
    """
    图表响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class ResourceChartQueryParam:
    """图表查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="图表名称"),
        code: str | None = Query(None, description="图表编号"),
        description: str | None = Query(None, description="备注/描述"),
        status: str | None = Query(None, description="是否启用"),
        paper_id: int | None = Query(None, description="文献ID"),
        local_path: str | None = Query(None, description="本地存储路径"),
        network_url: str | None = Query(None, description="网络地址"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.status = status
        # 精确查询字段
        self.paper_id = paper_id
        # 模糊查询字段
        self.name = ("like", name)
        # 模糊查询字段
        self.code = ("like", code)
        # 精确查询字段
        self.local_path = local_path
        # 精确查询字段
        self.network_url = network_url
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
