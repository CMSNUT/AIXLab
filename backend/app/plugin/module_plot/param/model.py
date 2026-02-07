# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class PlotParamModel(ModelMixinModify, UserMixin):
    """
    绘图参数管理表
    """
    __tablename__: str = 'plot_param'
    __table_args__: dict[str, str] = {'comment': '绘图参数管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    group: Mapped[str | None] = mapped_column(String(10), nullable=True, comment='参数组别')
    name: Mapped[str | None] = mapped_column(String(30), nullable=True, comment='参数名称')
    order: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='参数序号')
    script_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='脚本主键ID')

