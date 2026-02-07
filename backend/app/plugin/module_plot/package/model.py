# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class PlotPackageModel(ModelMixinModify, UserMixin):
    """
    绘图库包管理表
    """
    __tablename__: str = 'plot_package'
    __table_args__: dict[str, str] = {'comment': '绘图库包管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    version: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='库包版本')
    script_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='绘图脚本表的主键ID')
    url: Mapped[str | None] = mapped_column(String(200), nullable=True, comment='教程网址')

