# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Integer, Text, BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class RscLiteratureModel(ModelMixin, UserMixin):
    """
    文献管理表
    """
    __tablename__: str = 'rsc_literature'
    __table_args__: dict[str, str] = {'comment': '文献管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    type: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='文章类型，如期刊论文、会议论文等')
    title: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='标题')
    source: Mapped[str | None] = mapped_column(String(500), nullable=True, comment='期刊/会议名称')
    year: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='年份')
    volume: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='卷')
    issue: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='期')
    pages: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='页码')
    doi: Mapped[str | None] = mapped_column(String(500), nullable=True, comment='DOI标识')
    pmid: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='PubMed ID')

