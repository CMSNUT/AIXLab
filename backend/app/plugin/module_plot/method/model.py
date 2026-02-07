# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class PlotMethodModel(ModelMixinModify, UserMixin):
    """
    绘图方法管理表
    """
    __tablename__: str = 'plot_method'
    __table_args__: dict[str, str] = {'comment': '绘图方法管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    description: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='方法描述')
    order: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='方法步骤')
    script_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='脚本主键ID')

