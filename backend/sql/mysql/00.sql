-- 文献表
DROP TABLE IF EXISTS `resource_literature`;
CREATE TABLE `resource_literature` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '文献ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT "0" COMMENT '是否启用(0:启用 1:禁用)',
  `title` varchar(200) NOT NULL COMMENT '文献标题',
  `abstract` text COMMENT '摘要',
  `keywords` varchar(200) DEFAULT NULL COMMENT '关键词',
  `doi` varchar(200) DEFAULT NULL COMMENT 'DOI标识',
  `publish_year` year DEFAULT NULL COMMENT '发表年份',
  `journal_name` varchar(200) DEFAULT NULL COMMENT '期刊/会议名称',
  `volume` varchar(20) DEFAULT NULL COMMENT '卷',
  `issue` varchar(20) DEFAULT NULL COMMENT '期',
  `pages` varchar(20) DEFAULT NULL COMMENT '页码',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  KEY `idx_doi` (`doi`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `idx_resource_literature_publish_year` (`publish_year`),
  KEY `idx_resource_literature_journal_name` (`journal_name`(100)),
  KEY `idx_resource_literature_title` (`title`(100)),
  KEY `idx_resource_literature_keywords` (`keywords`(100)),
  KEY `ix_resource_literature_created_id` (`created_id`),
  KEY `ix_resource_literature_updated_id` (`updated_id`),
  CONSTRAINT `resource_literature_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `resource_literature_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献表';


-- 2. 作者表
DROP TABLE IF EXISTS `resource_author`;
CREATE TABLE `resource_author` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '作者ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  `name` varchar(100) NOT NULL COMMENT '作者姓名',
  `english_name` varchar(200) DEFAULT NULL COMMENT '英文名/拼音',
  `orcid` varchar(50) DEFAULT NULL COMMENT 'ORCID标识',
  `email` varchar(150) DEFAULT NULL COMMENT '邮箱',
  `research_field` varchar(300) DEFAULT NULL COMMENT '研究领域',
  `affiliation_id` bigint DEFAULT NULL COMMENT '关联单位ID',
  `h_index` int DEFAULT '0' COMMENT 'H指数',
  `publication_count` int DEFAULT '0' COMMENT '发表文献数量',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_resource_author_created_id` (`created_id`),
  KEY `ix_resource_author_updated_id` (`updated_id`),
  KEY `idx_name` (`name`),
  KEY `idx_orcid` (`orcid`),
  KEY `idx_affiliation_id` (`affiliation_id`),
  KEY `idx_h_index` (`h_index`),
  KEY `idx_email` (`email`),
  KEY `idx_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='作者表';

-- 3. 作者单位表
DROP TABLE IF EXISTS `resource_affiliation`;
CREATE TABLE `resource_affiliation` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '单位ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  `name` varchar(300) NOT NULL COMMENT '单位名称',
  `english_name` varchar(500) DEFAULT NULL COMMENT '英文名称',
  `country` varchar(100) DEFAULT NULL COMMENT '国家',
  `province` varchar(100) DEFAULT NULL COMMENT '省份/州',
  `city` varchar(100) DEFAULT NULL COMMENT '城市',
  `institution_type` tinyint DEFAULT NULL COMMENT '机构类型：1-大学，2-研究所，3-企业，4-医院，5-政府机构，6-其他',
  `ranking` int DEFAULT NULL COMMENT '排名',
  `author_count` int DEFAULT '0' COMMENT '作者数量',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_resource_affiliation_created_id` (`created_id`),
  KEY `ix_resource_affiliation_updated_id` (`updated_id`),
  KEY `idx_name` (`name`(100)),
  KEY `idx_country` (`country`),
  KEY `idx_city` (`city`),
  KEY `idx_institution_type` (`institution_type`),
  KEY `idx_ranking` (`ranking`),
  KEY `idx_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='作者单位表';

-- 4. 文献语料表
DROP TABLE IF EXISTS `resource_literature_corpus`;
CREATE TABLE `resource_literature_corpus` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '语料ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  `literature_id` bigint NOT NULL COMMENT '文献ID',
  `section_type` tinyint NOT NULL COMMENT '章节类型：1-引言，2-方法，3-结果，4-讨论，5-结论',
  `section_title` varchar(200) DEFAULT NULL COMMENT '章节标题',
  `content` text NOT NULL COMMENT '语料内容',
  `sequence` int DEFAULT '0' COMMENT '章节顺序',
  `word_count` int DEFAULT '0' COMMENT '字数统计',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_resource_literature_corpus_created_id` (`created_id`),
  KEY `ix_resource_literature_corpus_updated_id` (`updated_id`),
  KEY `idx_literature_id` (`literature_id`),
  KEY `idx_section_type` (`section_type`),
  KEY `idx_sequence` (`sequence`),
  KEY `idx_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献语料表';

-- 5. 文献图表表
DROP TABLE IF EXISTS `resource_literature_figure`;
CREATE TABLE `resource_literature_figure` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '图表ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  `literature_id` bigint NOT NULL COMMENT '文献ID',
  `figure_type` tinyint NOT NULL COMMENT '图表类型：1-图，2-表',
  `figure_number` varchar(50) DEFAULT NULL COMMENT '图表编号（如Fig.1，Table.1）',
  `caption` text COMMENT '图表标题/说明',
  `image_url` varchar(500) DEFAULT NULL COMMENT '图片地址',
  `data_url` varchar(500) DEFAULT NULL COMMENT '原始数据地址',
  `sequence` int DEFAULT '0' COMMENT '顺序',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_resource_literature_figure_created_id` (`created_id`),
  KEY `ix_resource_literature_figure_updated_id` (`updated_id`),
  KEY `idx_literature_id` (`literature_id`),
  KEY `idx_figure_type` (`figure_type`),
  KEY `idx_figure_number` (`figure_number`),
  KEY `idx_sequence` (`sequence`),
  KEY `idx_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献图表表';

-- 6. 文献数据表
DROP TABLE IF EXISTS `resource_literature_data`;
CREATE TABLE `resource_literature_data` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '数据ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  `literature_id` bigint NOT NULL COMMENT '文献ID',
  `data_type` tinyint NOT NULL COMMENT '数据类型：1-数值，2-文本，3-图像，4-表格',
  `data_key` varchar(200) DEFAULT NULL COMMENT '数据键名',
  `data_value` text COMMENT '数据值',
  `data_unit` varchar(50) DEFAULT NULL COMMENT '数据单位',
  `source_figure_id` bigint DEFAULT NULL COMMENT '来源图表ID',
  `category` varchar(100) DEFAULT NULL COMMENT '数据分类',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_resource_literature_data_created_id` (`created_id`),
  KEY `ix_resource_literature_data_updated_id` (`updated_id`),
  KEY `idx_literature_id` (`literature_id`),
  KEY `idx_data_type` (`data_type`),
  KEY `idx_data_key` (`data_key`),
  KEY `idx_category` (`category`),
  KEY `idx_source_figure_id` (`source_figure_id`),
  KEY `idx_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献数据表';

-- 7. 文献解读表
DROP TABLE IF EXISTS `resource_literature_analysis`;
CREATE TABLE `resource_literature_analysis` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '解读ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  `literature_id` bigint NOT NULL COMMENT '文献ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `title` varchar(200) DEFAULT NULL COMMENT '解读标题',
  `content` text NOT NULL COMMENT '解读内容',
  `summary` varchar(500) DEFAULT NULL COMMENT '解读摘要',
  `view_count` int DEFAULT '0' COMMENT '查看次数',
  `like_count` int DEFAULT '0' COMMENT '点赞数',
  `collect_count` int DEFAULT '0' COMMENT '收藏数',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_resource_literature_analysis_created_id` (`created_id`),
  KEY `ix_resource_literature_analysis_updated_id` (`updated_id`),
  KEY `idx_literature_id` (`literature_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_created_time` (`created_time`),
  KEY `idx_view_count` (`view_count`),
  KEY `idx_like_count` (`like_count`),
  FULLTEXT KEY `ft_content` (`content`) WITH PARSER ngram
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献解读表';

-- 8. 解读评论表
DROP TABLE IF EXISTS `resource_analysis_comment`;
CREATE TABLE `resource_analysis_comment` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '评论ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  `analysis_id` bigint NOT NULL COMMENT '解读ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `parent_id` bigint DEFAULT '0' COMMENT '父评论ID（0表示顶级评论）',
  `content` text NOT NULL COMMENT '评论内容',
  `like_count` int DEFAULT '0' COMMENT '点赞数',
  `reply_count` int DEFAULT '0' COMMENT '回复数',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_resource_analysis_comment_created_id` (`created_id`),
  KEY `ix_resource_analysis_comment_updated_id` (`updated_id`),
  KEY `idx_analysis_id` (`analysis_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_created_time` (`created_time`),
  KEY `idx_like_count` (`like_count`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='解读评论表';

-- 9. 文献-作者关联表
DROP TABLE IF EXISTS `resource_literature_author`;
CREATE TABLE `resource_literature_author` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '关联ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  `literature_id` bigint NOT NULL COMMENT '文献ID',
  `author_id` bigint NOT NULL COMMENT '作者ID',
  `author_order` int DEFAULT '0' COMMENT '作者顺序（1表示第一作者）',
  `corresponding_author` tinyint DEFAULT '0' COMMENT '是否为通讯作者：0-否，1-是',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  UNIQUE KEY `uk_resource_literature_author` (`literature_id`,`author_id`),
  KEY `ix_resource_literature_author_created_id` (`created_id`),
  KEY `ix_resource_literature_author_updated_id` (`updated_id`),
  KEY `idx_author_id` (`author_id`),
  KEY `idx_author_order` (`author_order`),
  KEY `idx_corresponding_author` (`corresponding_author`),
  KEY `idx_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献-作者关联表';