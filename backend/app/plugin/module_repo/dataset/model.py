# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class RepoDatasetModel(ModelMixinModify, UserMixin):
    """
    数据仓库管理表
    """
    __tablename__: str = 'repo_dataset'
    __table_args__: dict[str, str] = {'comment': '数据仓库管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='数据仓库名称')
    alias: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='数据英文名称')
    format: Mapped[str | None] = mapped_column(String(10), nullable=True, comment='数据格式')
    field: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='应用领域')
    category: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='数据类别')
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment='数据描述')
    local_file: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='本地文件')
    url_link: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='网络地址')
    cloud_link: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='网盘链接')

