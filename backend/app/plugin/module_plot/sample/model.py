# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class PlotSampleModel(ModelMixinModify, UserMixin):
    """
    绘图实例管理表
    """
    __tablename__: str = 'plot_sample'
    __table_args__: dict[str, str] = {'comment': '绘图实例管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    order: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='实例序号')
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment='实例内容')
    script_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='脚本主键ID')

