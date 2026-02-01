# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import String, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class ResourceKitModel(ModelMixinModify, UserMixin):
    """
    模块表
    """
    __tablename__: str = 'resource_kit'
    __table_args__: dict[str, str] = {'comment': '模块'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='模块名称')
    type: Mapped[str | None] = mapped_column(String(10), nullable=True, comment='模块类型')
    language: Mapped[str | None] = mapped_column(String(10), nullable=True, comment='编程语言')
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment='备注/描述')
    local_path: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='本地文件')
    network_url: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='网络地址')
    cloud_url: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='网盘地址')

