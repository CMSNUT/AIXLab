# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import DateTime, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class ExampleNoteModel(ModelMixinModify, UserMixin):
    """
    案例分析笔记管理表
    """
    __tablename__: str = 'example_note'
    __table_args__: dict[str, str] = {'comment': '案例分析笔记管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='笔记名称')
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment='笔记内容')
    analysis_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='案例分析ID')

