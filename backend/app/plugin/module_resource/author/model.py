# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import String, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ResourceAuthorModel(ModelMixin, UserMixin):
    """
    作者表
    """
    __tablename__: str = 'resource_author'
    __table_args__: dict[str, str] = {'comment': '作者'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='作者姓名')
    institution: Mapped[str | None] = mapped_column(String(500), nullable=True, comment='机构/单位')
    email: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='邮箱')
    orcid: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='ORCID标识')

