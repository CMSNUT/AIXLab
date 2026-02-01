# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import DateTime, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class ResourcePaperModel(ModelMixinModify, UserMixin):
    """
    文献表
    """
    __tablename__: str = 'resource_paper'
    __table_args__: dict[str, str] = {'comment': '文献'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    type: Mapped[str | None] = mapped_column(String(10), nullable=True, comment='文章类型')
    field: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='文章领域')
    title: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='标题')
    source: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='期刊/会议名称')
    year: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='年份')
    volume: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='卷')
    issue: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='期')
    pages: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='页码')
    doi: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='DOI')
    pmid: Mapped[str | None] = mapped_column(String(10), nullable=True, comment='PubMed ID')
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment='备注/描述')

