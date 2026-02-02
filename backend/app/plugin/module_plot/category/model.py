# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Integer, Text, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class PlotCategoryModel(ModelMixinModify, UserMixin):
    """
    绘图模块管理表
    """
    __tablename__: str = 'plot_category'
    __table_args__: dict[str, str] = {'comment': '绘图模块管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='模块名称')
    code: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='模块编码')
    category: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='模块大类')
    subcategory: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='模块子类')
    image: Mapped[str | None] = mapped_column(Text, nullable=True, comment='模块图片')

