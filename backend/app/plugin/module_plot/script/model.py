# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Text, Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class PlotScriptModel(ModelMixinModify, UserMixin):
    """
    绘图脚本管理表
    """
    __tablename__: str = 'plot_script'
    __table_args__: dict[str, str] = {'comment': '绘图脚本管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='绘图脚本名称')
    alias: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='脚本英文名称')
    order: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='脚本序号')
    service: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='软件版本')
    field: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='应用领域')
    category: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='功能类别')
    image: Mapped[str | None] = mapped_column(Text, nullable=True, comment='脚本图标')
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment='功能描述')

