# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchemaModify, UserBySchema

class ExampleSectionProgramsCreateSchema(BaseModel):
    """
    案例节点代码关联管理新增模型
    """
    node_id: int  | None = Field(default=None, description='案例节点ID')
    program_id: int  | None = Field(default=None, description='代码仓库ID')


class ExampleSectionProgramsUpdateSchema(ExampleSectionProgramsCreateSchema):
    """
    案例节点代码关联管理更新模型
    """
    ...


class ExampleSectionProgramsOutSchema(ExampleSectionProgramsCreateSchema, BaseSchemaModify, UserBySchema):
    """
    案例节点代码关联管理响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class ExampleSectionProgramsQueryParam:
    """案例节点代码关联管理查询参数"""

    def __init__(
        self,
        node_id: int | None = Query(None, description="案例节点ID"),
        program_id: int | None = Query(None, description="代码仓库ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.node_id = node_id
        # 精确查询字段
        self.program_id = program_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
