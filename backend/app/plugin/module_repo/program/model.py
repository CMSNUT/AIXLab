# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class RepoProgramModel(ModelMixinModify, UserMixin):
    """
    代码仓库管理表
    """
    __tablename__: str = 'repo_program'
    __table_args__: dict[str, str] = {'comment': '代码仓库管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='代码仓库名称')
    alias: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='代码英文名称')
    language: Mapped[str | None] = mapped_column(String(10), nullable=True, comment='代码语言')
    field: Mapped[str | None] = mapped_column(String(10), nullable=True, comment='应用领域')
    category: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='功能类别')
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment='功能描述')
    local_file: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='本地文件')
    url_link: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='网络地址')
    cloud_link: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='网盘链接')

