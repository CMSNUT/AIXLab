# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ResourceCaseModel(ModelMixin, UserMixin):
    """
    案例表
    """
    __tablename__: str = 'resource_case'
    __table_args__: dict[str, str] = {'comment': '案例'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='案例名称')
    content: Mapped[str | None] = mapped_column(Text, nullable=True, comment='内容')
    paper_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='文献ID')

