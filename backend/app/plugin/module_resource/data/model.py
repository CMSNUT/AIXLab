# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ResourceDataModel(ModelMixin, UserMixin):
    """
    数据表
    """
    __tablename__: str = 'resource_data'
    __table_args__: dict[str, str] = {'comment': '数据'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(500), nullable=True, comment='数据名称')
    type: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='数据类型')
    format: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='数据格式')
    local_path: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='本地存储路径')
    network_url: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='网络地址')
    cloud_url: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='网盘地址')

