# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ResourceChartModel(ModelMixin, UserMixin):
    """
    图表表
    """
    __tablename__: str = 'resource_chart'
    __table_args__: dict[str, str] = {'comment': '图表'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    paper_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='文献ID')
    name: Mapped[str | None] = mapped_column(String(200), nullable=True, comment='图表名称')
    code: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='图表编号')
    local_path: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='本地存储路径')
    network_url: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment='网络地址')

