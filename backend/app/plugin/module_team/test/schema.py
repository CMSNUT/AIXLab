# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class TeamTestCreateSchema(BaseModel):
    """
    测试新增模型
    """
    name: str = Field(default=..., description='课题名称')
    content: str = Field(default=..., description='课题简介')
    file_path: str = Field(default=..., description='本地文件')
    image_path: str = Field(default=..., description='本地图片')


class TeamTestUpdateSchema(TeamTestCreateSchema):
    """
    测试更新模型
    """
    ...


class TeamTestOutSchema(TeamTestCreateSchema, BaseSchema, UserBySchema):
    """
    测试响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class TeamTestQueryParam:
    """测试查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="课题名称"),
        content: str | None = Query(None, description="课题简介"),
        file_path: str | None = Query(None, description="本地文件"),
        image_path: str | None = Query(None, description="本地图片"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 模糊查询字段
        self.name = ("like", name)
        # 模糊查询字段
        self.content = ("like", content)
        # 精确查询字段
        self.file_path = file_path
        # 精确查询字段
        self.image_path = image_path
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
