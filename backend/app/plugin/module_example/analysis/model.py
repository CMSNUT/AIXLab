# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Text, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class ExampleAnalysisModel(ModelMixinModify, UserMixin):
    """
    案例分析管理表
    """
    __tablename__: str = 'example_analysis'
    __table_args__: dict[str, str] = {'comment': '案例分析管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='研究案例名称')
    field: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='研究领域')
    category: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='研究主题')
    image: Mapped[str | None] = mapped_column(Text, nullable=True, comment='研究案例图标')
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment='案例详情内容')

