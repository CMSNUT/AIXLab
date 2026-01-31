-- 1. 文献表
DROP TABLE IF EXISTS `resource_paper`;

CREATE TABLE `resource_paper` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT '0' COMMENT '是否启用',
  `type` varchar(10) DEFAULT NULL COMMENT '文章类型',
  `field` varchar(10) DEFAULT NULL COMMENT '文章领域',
  `title` varchar(300) NOT NULL COMMENT '标题',
  `source` varchar(300) DEFAULT NULL COMMENT '期刊/会议名称',
  `year` int DEFAULT NULL COMMENT '年份',
  `volume` varchar(20) DEFAULT NULL COMMENT '卷',
  `issue` varchar(20) DEFAULT NULL COMMENT '期',
  `pages` varchar(20) DEFAULT NULL COMMENT '页码',
  `doi` varchar(300) DEFAULT NULL COMMENT 'DOI',
  `pmid` varchar(10) DEFAULT NULL COMMENT 'PubMed ID',
  `description` text DEFAULT NULL COMMENT '备注/描述',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  UNIQUE KEY `ix_resource_paper_uuid` (`uuid`),
  KEY `ix_resource_paper_title` (`title`(255)),
  KEY `ix_resource_paper_created_id` (`created_id`),
  KEY `ix_resource_paper_updated_id` (`updated_id`),
  CONSTRAINT `resource_paper_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `resource_paper_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献表';

-- 2. 作者表
DROP TABLE IF EXISTS `resource_author`;

CREATE TABLE `resource_author` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT  '0'  COMMENT '是否启用',
  `name` varchar(255) NOT NULL COMMENT '作者姓名',
  `institution` varchar(500) COMMENT '机构/单位',
  `email` varchar(100) COMMENT '邮箱',
  `orcid` varchar(50) COMMENT 'ORCID标识',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  UNIQUE KEY `ix_resource_author_uuid` (`uuid`),
  UNIQUE KEY `ix_resource_author_orcid` (`orcid`),
  KEY `ix_resource_author_name` (`name`),
  KEY `ix_resource_author_institution` (`institution`(255)),
  KEY `ix_resource_author_created_id` (`created_id`),
  KEY `ix_resource_author_updated_id` (`updated_id`),
  KEY `ix_resource_author_created_time` (`created_time`),
  KEY `ix_resource_author_updated_time` (`updated_time`),
  CONSTRAINT `resource_author_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `resource_author_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='作者表';


-- 3. 数据表
DROP TABLE IF EXISTS `resource_data`;

CREATE TABLE `resource_data` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT  '0'  COMMENT '是否启用',
  `name` varchar(500) NOT NULL COMMENT '数据名称',
  `type` varchar(100) DEFAULT NULL COMMENT '数据类型',
  `format` varchar(100) DEFAULT 'CSV' COMMENT '数据格式',
  `description` text DEFAULT NULL COMMENT '备注/描述',
  `local_path` varchar(1000) DEFAULT NULL COMMENT '本地存储路径',
  `network_url` varchar(1000) DEFAULT NULL COMMENT '网络地址',
  `cloud_url` varchar(1000) DEFAULT NULL COMMENT '网盘地址',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  UNIQUE KEY `ix_resource_data_uuid` (`uuid`),
  KEY `ix_resource_data_name` (`name`(255)),
  KEY `ix_resource_data_status` (`status`),
  KEY `ix_resource_data_type` (`type`),
  KEY `ix_resource_data_format` (`format`),
  KEY `ix_resource_data_created_id` (`created_id`),
  KEY `ix_resource_data_updated_id` (`updated_id`),
  KEY `ix_resource_data_created_time` (`created_time`),
  KEY `ix_resource_data_updated_time` (`updated_time`),
  CONSTRAINT `resource_data_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `resource_data_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据表';

-- 4. 脚本表
DROP TABLE IF EXISTS `resource_script`;

CREATE TABLE `resource_script` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT  '0'  COMMENT '是否启用',
  `name` varchar(500) NOT NULL COMMENT '脚本名称',
  `type` varchar(100) COMMENT '脚本类型',
  `language` varchar(100) COMMENT '编程语言',
  `description` text COMMENT '备注/描述',
  `local_path` varchar(1000) DEFAULT NULL COMMENT '本地存储路径',
  `network_url` varchar(1000) DEFAULT NULL COMMENT '网络地址',
  `cloud_url` varchar(1000) DEFAULT NULL COMMENT '网盘地址',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  UNIQUE KEY `ix_script_uuid` (`uuid`),
  INDEX `ix_script_name` (`name`(255)),
  INDEX `ix_script_status` (`status`),
  INDEX `ix_script_language` (`language`),
  INDEX `ix_script_type` (`type`),
  KEY `ix_resource_script_created_id` (`created_id`),
  KEY `ix_resource_script_updated_id` (`updated_id`),
  KEY `ix_resource_script_created_time` (`created_time`),
  KEY `ix_resource_script_updated_time` (`updated_time`),
  CONSTRAINT `resource_script_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `resource_script_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='脚本表';

-- 5.模块表
DROP TABLE IF EXISTS `resource_kit`;

CREATE TABLE `resource_kit` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT  '0'  COMMENT '是否启用',
  `name` varchar(500) NOT NULL COMMENT '模块名称',
  `type` varchar(100) DEFAULT '基础图表' COMMENT '模块类型',
  `language` varchar(100) DEFAULT 'Python' COMMENT '编程语言',
  `description` text DEFAULT NULL COMMENT '备注/描述',
  `local_path` varchar(1000) DEFAULT NULL COMMENT '本地存储路径',
  `network_url` varchar(1000) DEFAULT NULL COMMENT '网络地址',
  `cloud_url` varchar(1000) DEFAULT NULL COMMENT '网盘地址',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  UNIQUE KEY `ix_kit_uuid` (`uuid`),
  INDEX `ix_kit_name` (`name`(255)),
  INDEX `ix_kit_status` (`status`),
  INDEX `ix_kit_language` (`language`),
  INDEX `ix_kit_type` (`type`),
  KEY `ix_resource_kit_created_id` (`created_id`),
  KEY `ix_resource_kit_updated_id` (`updated_id`),
  KEY `ix_resource_kit_created_time` (`created_time`),
  KEY `ix_resource_kit_updated_time` (`updated_time`),
  CONSTRAINT `resource_kit_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `resource_kit_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='模块表';

-- 6. 文献作者关联表
DROP TABLE IF EXISTS `resource_paper_authors`;

CREATE TABLE `resource_paper_authors` (
  `paper_id` int NOT NULL COMMENT '文献ID',
  `author_id` int NOT NULL COMMENT '作者ID',
  `author_order` int DEFAULT 1 COMMENT '作者顺序',
  `is_corresponding_author` tinyint DEFAULT 0 COMMENT '是否通讯作者',
  `is_co_first_author` tinyint DEFAULT 0 COMMENT '是否共同第一作者',
  PRIMARY KEY  (`paper_id`, `author_id`),
  KEY `ix_resource_paper_authors_author_id` (`author_id`),
  KEY `is_corresponding_author` (`is_corresponding_author`),
  KEY `is_co_first_author` (`is_co_first_author`),
  FOREIGN KEY (`paper_id`) REFERENCES `resource_paper`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`author_id`) REFERENCES `resource_author`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献作者关联表';

-- 7. 文献数据关联表
DROP TABLE IF EXISTS `resource_paper_datas`;

CREATE TABLE `resource_paper_datas` (
  `paper_id` int NOT NULL COMMENT '文献ID',
  `data_id` int NOT NULL COMMENT '数据ID',
  PRIMARY KEY (`paper_id`, `data_id`),
  KEY `ix_paper_datas_data_id` (`data_id`),
  FOREIGN KEY (`paper_id`) REFERENCES `resource_paper`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`data_id`) REFERENCES `resource_data`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献数据关联表';

-- 8. 文献脚本关联表
DROP TABLE IF EXISTS `resource_paper_scripts`;

CREATE TABLE `resource_paper_scripts` (
  `paper_id` int NOT NULL COMMENT '文献ID',
  `script_id` int NOT NULL COMMENT '脚本ID',
  PRIMARY KEY (`paper_id`, `script_id`),
  KEY `ix_paper_scripts_script_id` (`script_id`),
  FOREIGN KEY (`paper_id`) REFERENCES `resource_paper`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`script_id`) REFERENCES `resource_script`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献脚本关联表';

-- 9. 数据脚本关联表
DROP TABLE IF EXISTS `resource_data_scripts`;

CREATE TABLE `resource_data_scripts` (
  `data_id` int NOT NULL COMMENT '数据ID',
  `script_id` int NOT NULL COMMENT '脚本ID',
  PRIMARY KEY (`data_id`, `script_id`),
  KEY `ix_data_scripts_script_id` (`script_id`),
  FOREIGN KEY (`data_id`) REFERENCES `resource_data`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`script_id`) REFERENCES `resource_script`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据脚本关联表';

-- 10.模块脚本关联表
DROP TABLE IF EXISTS `resource_kit_scripts`;

CREATE TABLE `resource_kit_scripts` (
  `kit_id` int NOT NULL COMMENT '模块ID',
  `script_id` int NOT NULL COMMENT '脚本ID',
  PRIMARY KEY  (`kit_id`, `script_id`),
  KEY `ix_kit_scripts_script_id` (`script_id`),
  FOREIGN KEY (`kit_id`) REFERENCES `resource_kit`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`script_id`) REFERENCES `resource_script`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='模块脚本关联表';

-- 11.数据-模块关联表
DROP TABLE IF EXISTS `resource_data_kits`;

CREATE TABLE `resource_data_kits` (
  `data_id` int NOT NULL COMMENT '数据ID',
  `kit_id` int NOT NULL COMMENT '模块ID',
  PRIMARY KEY  (`data_id`, `kit_id`),
  KEY `ix_data_kits_kit_id` (`kit_id`),
  FOREIGN KEY (`data_id`) REFERENCES `resource_data`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`kit_id`) REFERENCES `resource_kit`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据模块关联表';

-- 12. 案例表
DROP TABLE IF EXISTS `resource_case`;

CREATE TABLE `resource_case` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用',
  `name` varchar(100) NOT NULL COMMENT '案例名称',
  `description` text COMMENT '备注/描述',
  `content` longtext DEFAULT NULL COMMENT '内容',
  `paper_id` int DEFAULT NULL COMMENT '文献ID',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  UNIQUE KEY `ix_resource_case_uuid` (`uuid`),
  KEY `ix_resource_case_paper_id` (`paper_id`),
  KEY `ix_resource_case_created_id` (`created_id`),
  KEY `ix_resource_case_updated_id` (`updated_id`),
  KEY `ix_resource_case_created_time` (`created_time`),
  KEY `ix_resource_case_updated_time` (`updated_time`),
  CONSTRAINT `resource_case_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `resource_case_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `resource_case_ibfk_3` FOREIGN KEY (`paper_id`) REFERENCES `resource_paper` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='案例表';

-- 13. 案例-代码关联表
DROP TABLE IF EXISTS `resource_case_scripts`;

CREATE TABLE `resource_case_scripts` (
  `case_id` int NOT NULL COMMENT '案例ID',
  `script_id` int NOT NULL COMMENT '脚本ID',
  PRIMARY KEY (`case_id`, `script_id`),
  KEY `ix_case_scripts_script_id` (`script_id`),
  CONSTRAINT `fk_case_scripts_case` FOREIGN KEY (`case_id`) REFERENCES `resource_case` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_case_scripts_script` FOREIGN KEY (`script_id`) REFERENCES `resource_script` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='案例脚本关联表';

-- 14. 案例功能模块关联表
DROP TABLE IF EXISTS `resource_case_kits`;

CREATE TABLE `resource_case_kits` (
  `case_id` int NOT NULL COMMENT '案例ID',
  `kit_id` int NOT NULL COMMENT '程序ID',
  PRIMARY KEY (`case_id`, `kit_id`),
  KEY `ix_case_kit_kit_id` (`kit_id`),
  CONSTRAINT `fk_case_kit_case` FOREIGN KEY (`case_id`) REFERENCES `resource_case` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_case_kit_kit` FOREIGN KEY (`kit_id`) REFERENCES `resource_kit` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='案例模块关联表';


-- 15. 语料表
DROP TABLE IF EXISTS `resource_corpus`;

CREATE TABLE `resource_corpus` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT '0' COMMENT '是否启用',
  `paper_id` int DEFAULT NULL COMMENT '文献ID',
  `section` varchar(200) DEFAULT NULL COMMENT '文章章节',
  `content_en` text DEFAULT NULL COMMENT '英文内容',
  `content_cn` text DEFAULT NULL COMMENT '中文内容',
  `description` text DEFAULT NULL COMMENT '备注/描述',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_resource_corpus_uuid` (`uuid`),
  KEY `ix_resource_corpus_created_id` (`created_id`),
  KEY `ix_resource_corpus_updated_id` (`updated_id`),
  KEY `ix_resource_corpus_created_time` (`created_time`),
  KEY `ix_resource_corpus_updated_time` (`updated_time`),
  CONSTRAINT `fk_corpus_paper` FOREIGN KEY (`paper_id`) REFERENCES `resource_paper` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_corpus_created_user` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_corpus_updated_user` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料表';

-- 16. 图表表
DROP TABLE IF EXISTS `resource_chart`;

CREATE TABLE `resource_chart` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT '0' COMMENT '是否启用',
  `paper_id` int DEFAULT NULL COMMENT '文献ID',
  `name` varchar(200) DEFAULT NULL COMMENT '图表名称',
  `code` varchar(50) DEFAULT NULL COMMENT '图表编号',
  `local_path` varchar(500) DEFAULT NULL COMMENT '本地存储路径',
  `network_url` varchar(500) DEFAULT NULL COMMENT '网络地址',
  `description` text DEFAULT NULL COMMENT '备注/描述',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_resource_chart_uuid` (`uuid`),
  KEY `ix_resource_chart_paper_id` (`paper_id`),
  KEY `ix_resource_chart_created_id` (`created_id`),
  KEY `ix_resource_chart_updated_id` (`updated_id`),
  KEY `ix_resource_chart_created_time` (`created_time`),
  KEY `ix_resource_chart_updated_time` (`updated_time`),
  CONSTRAINT `fk_chart_paper` FOREIGN KEY (`paper_id`) REFERENCES `resource_paper` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chart_created_user` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_chart_updated_user` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='图表表';

-- 17. 图表-语料关联表
DROP TABLE IF EXISTS `resource_chart_corpus`;

CREATE TABLE `resource_chart_corpus` (
  `chart_id` int NOT NULL COMMENT '图表ID',
  `corpus_id` int NOT NULL COMMENT '语料ID',
  PRIMARY KEY (`chart_id`, `corpus_id`),
  KEY `ix_chart_corpus_corpus_id` (`corpus_id`),
  CONSTRAINT `fk_chart_corpus_chart` FOREIGN KEY (`chart_id`) REFERENCES `resource_chart` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chart_corpus_corpus` FOREIGN KEY (`corpus_id`) REFERENCES `resource_corpus` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='图表语料关联表';

-- 18. 图表-脚本关联表 
DROP TABLE IF EXISTS `resource_chart_kits`;

CREATE TABLE `resource_chart_kits` (
  `chart_id` int NOT NULL COMMENT '图表ID',
  `kit_id` int NOT NULL COMMENT '模块ID',
  PRIMARY KEY (`chart_id`, `kit_id`),
  KEY `ix_chart_kits_kit_id` (`kit_id`),
  CONSTRAINT `fk_chart_kits_chart` FOREIGN KEY (`chart_id`) REFERENCES `resource_chart` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chart_kits_kit` FOREIGN KEY (`kit_id`) REFERENCES `resource_kit` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='图表模块关联表';

-- 19. 图表-案例关联表
DROP TABLE IF EXISTS `resource_chart_cases`;

CREATE TABLE `resource_chart_cases` (
  `chart_id` int NOT NULL COMMENT '图表ID',
  `case_id` int NOT NULL COMMENT '案例ID',
  PRIMARY KEY (`chart_id`, `case_id`),
  KEY `ix_chart_cases_cases_id` (`case_id`),
  CONSTRAINT `fk_chart_case_chart` FOREIGN KEY (`chart_id`) REFERENCES `resource_chart` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chart_case_case` FOREIGN KEY (`case_id`) REFERENCES `resource_case` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='图表案例关联表';


