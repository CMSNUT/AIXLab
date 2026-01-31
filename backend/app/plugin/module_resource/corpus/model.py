# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import DateTime, Text, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ResourceCorpusModel(ModelMixin, UserMixin):
    """
    语料表
    """
    __tablename__: str = 'resource_corpus'
    __table_args__: dict[str, str] = {'comment': '语料'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    paper_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='文献ID')
    section: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='文章章节')
    content_en: Mapped[str | None] = mapped_column(Text, nullable=True, comment='英文内容')
    content_cn: Mapped[str | None] = mapped_column(Text, nullable=True, comment='中文内容')

