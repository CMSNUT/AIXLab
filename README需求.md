要构建1个数据库，需要设计1些数据表，这些数据表需要能实现下述功能：
文献信息：id、uuid、status、类型、标题、作者、来源(期刊)、年、卷、期、页码、DOI、PubMedID、描述、创建时间、创建人、更新时间、更新人
数据信息：id、uuid、status、名称、类型、格式、描述、本地位置、网络地址、网盘地址、创建时间、创建人、更新时间、更新人
代码信息：id、uuid、status、名称、类型、语言、描述、本地位置、网络地址、网盘地址、创建时间、创建人、更新时间、更新人
内置功能模块：id、uuid、status、名称、类型、语言、描述、本地位置、网络地址、网盘地址、创建时间、创建人、更新时间、更新人
文献-作者 多对多、文献-数据多对多、文献-代码多对多、数据-程序 多对多、功能-程序 多对多 数据-功能多对多

设计每个表的结构。

文献表 (literature)
字段：id, uuid, status, 类型, 标题, 来源(期刊), 年, 卷, 期, 页码, DOI, PubMedID, 描述, 创建时间, 创建人, 更新时间, 更新人

作者表 (author)
字段：id, uuid, status, 姓名, 机构, 描述, 创建时间, 创建人, 更新时间, 更新人

文献-作者关联表 (literature_author)
字段：id, literature_id, author_id, 排序（用于表示作者顺序）

数据表 (data)
字段：id, uuid, status, 名称, 类型, 格式, 描述, 本地位置, 网络地址, 网盘地址, 创建时间, 创建人, 更新时间, 更新人

代码表 (code)
字段：id, uuid, status, 名称, 类型, 语言, 描述, 本地位置, 网络地址, 网盘地址, 创建时间, 创建人, 更新时间, 更新人

功能模块表 (module)
字段：id, uuid, status, 名称, 类型, 语言, 描述, 本地位置, 网络地址, 网盘地址, 创建时间, 创建人, 更新时间, 更新人

文献-数据关联表 (literature_data)
字段：id, literature_id, data_id

文献-代码关联表 (literature_code)
字段：id, literature_id, code_id

数据-代码关联表 (data_code)
字段：id, data_id, code_id

功能-代码关联表 (module_code)
字段：id, module_id, code_id

数据-功能关联表 (data_module)
字段：id, data_id, module_id

注意：关联表一般不需要uuid和status，但如果有需要也可以加上。这里根据需求，我们只保留关联关系的主键和两个外键，以及一个自增id。
另外，文献-作者关联表需要一个排序字段，用于表示作者在文献中的顺序。

