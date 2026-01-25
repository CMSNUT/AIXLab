# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Text, BigInteger, String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ResourceLiteratureModel(ModelMixin, UserMixin):
    """
    文献管理表
    """
    __tablename__: str = 'resource_literature'
    __table_args__: dict[str, str] = {'comment': '文献管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    title: Mapped[str | None] = mapped_column(String(200), nullable=True, comment='文献标题')
    abstract: Mapped[str | None] = mapped_column(Text, nullable=True, comment='摘要')
    keywords: Mapped[str | None] = mapped_column(String(200), nullable=True, comment='关键词')
    doi: Mapped[str | None] = mapped_column(String(200), nullable=True, comment='DOI标识')
    publish_year: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='发表年份')
    journal_name: Mapped[str | None] = mapped_column(String(200), nullable=True, comment='期刊/会议名称')
    volume: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='卷')
    issue: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='期')
    pages: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='页码')

