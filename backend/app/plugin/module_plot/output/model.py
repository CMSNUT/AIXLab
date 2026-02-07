# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class PlotOutputModel(ModelMixinModify, UserMixin):
    """
    绘图结果管理表
    """
    __tablename__: str = 'plot_output'
    __table_args__: dict[str, str] = {'comment': '绘图结果管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    order: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='结果序号')
    name: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='结果标题')
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment='结果内容')
    script_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='脚本主键ID')

