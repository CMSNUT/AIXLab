# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchemaModify, UserBySchema

class ExampleAnalysisCreateSchema(BaseModel):
    """
    案例分析管理新增模型
    """
    name: str  | None = Field(default=None, description='研究案例名称')
    field: str  | None = Field(default=None, description='研究领域')
    category: str  | None = Field(default=None, description='研究主题')
    image: str  | None = Field(default=None, description='研究案例图标')
    description: str  | None = Field(default=None, description='案例详情内容')


class ExampleAnalysisUpdateSchema(ExampleAnalysisCreateSchema):
    """
    案例分析管理更新模型
    """
    ...


class ExampleAnalysisOutSchema(ExampleAnalysisCreateSchema, BaseSchemaModify, UserBySchema):
    """
    案例分析管理响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class ExampleAnalysisQueryParam:
    """案例分析管理查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="研究案例名称"),
        category: str | None = Query(None, description="研究主题"),
        description: str | None = Query(None, description="案例详情内容"),
        field: str | None = Query(None, description="研究领域"),
        image: str | None = Query(None, description="研究案例图标"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 模糊查询字段
        self.name = ("like", name)
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
