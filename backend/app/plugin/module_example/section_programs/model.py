# -*- coding: utf-8 -*-

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class ExampleSectionProgramsModel(ModelMixinModify, UserMixin):
    """
    案例节点代码关联管理表
    """
    __tablename__: str = 'example_section_programs'
    __table_args__: dict[str, str] = {'comment': '案例节点代码关联管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    node_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='案例节点ID')
    program_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='代码仓库ID')

