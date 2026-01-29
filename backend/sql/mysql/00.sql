-- 1. 文献表
DROP TABLE IF EXISTS `rsc_literature`;

CREATE TABLE `rsc_literature` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT  '0'  COMMENT '是否启用(0:启用 1:禁用)',
  `type` varchar(50) COMMENT '文章类型，如期刊论文、会议论文等',
  `title` varchar(1000) NOT NULL COMMENT '标题',
  `source` varchar(500) COMMENT '期刊/会议名称',
  `year` int COMMENT '年份',
  `volume` varchar(50) COMMENT '卷',
  `issue` varchar(50) COMMENT '期',
  `pages` varchar(100) COMMENT '页码',
  `doi` varchar(500) COMMENT 'DOI标识',
  `pmid` varchar(100) COMMENT 'PubMed ID',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  UNIQUE KEY `uk_literature_uuid` (`uuid`),
  INDEX `idx_literature_doi` (`doi`(255)),
  INDEX `idx_literature_pmid` (`pmid`),
  INDEX `idx_literature_status` (`status`),
  INDEX `idx_literature_title` (`title`(255)),
  INDEX `idx_literature_year` (`year`),
  INDEX `idx_literature_type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献表';

-- 2. 作者表
DROP TABLE IF EXISTS `rsc_author`;

CREATE TABLE `rsc_author` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT  '0'  COMMENT '是否启用(0:启用 1:禁用)',
  `name` varchar(255) NOT NULL COMMENT '作者姓名',
  `institution` varchar(500) COMMENT '机构/单位',
  `email` varchar(255) COMMENT '邮箱',
  `orcid` varchar(50) COMMENT 'ORCID标识',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  UNIQUE KEY `uk_author_uuid` (`uuid`),
  UNIQUE KEY `uk_author_orcid` (`orcid`),
  INDEX `idx_author_name` (`name`),
  INDEX `idx_author_status` (`status`),
  INDEX `idx_author_institution` (`institution`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='作者表';


-- 3. 数据表
DROP TABLE IF EXISTS `rsc_data`;

CREATE TABLE `rsc_data` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT  '0'  COMMENT '是否启用(0:启用 1:禁用)',
  `name` varchar(500) NOT NULL COMMENT '数据名称',
  `type` varchar(100) COMMENT '数据类型',
  `format` varchar(100) COMMENT '数据格式',
  `description` text COMMENT '备注/描述',
  `local_path` varchar(1000) COMMENT '本地存储路径',
  `network_url` varchar(1000) COMMENT '网络地址',
  `cloud_url` varchar(1000) COMMENT '网盘地址',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  UNIQUE KEY `uk_data_uuid` (`uuid`),
  INDEX `idx_data_name` (`name`(255)),
  INDEX `idx_data_status` (`status`),
  INDEX `idx_data_type` (`type`),
  INDEX `idx_data_format` (`format`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据表';

-- 4. 代码表
DROP TABLE IF EXISTS `rsc_code`;

CREATE TABLE `rsc_code` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT  '0'  COMMENT '是否启用(0:启用 1:禁用)',
  `name` varchar(500) NOT NULL COMMENT '代码名称',
  `type` varchar(100) COMMENT '代码类型',
  `language` varchar(100) COMMENT '编程语言',
  `description` text COMMENT '备注/描述',
  `local_path` varchar(1000) COMMENT '本地存储路径',
  `network_url` varchar(1000) COMMENT '网络地址',
  `cloud_url` varchar(1000) COMMENT '网盘地址',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  UNIQUE KEY `uk_code_uuid` (`uuid`),
  INDEX `idx_code_name` (`name`(255)),
  INDEX `idx_code_status` (`status`),
  INDEX `idx_code_language` (`language`),
  INDEX `idx_code_type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='代码表';

-- 5.功能模块表
DROP TABLE IF EXISTS `rsc_module`;

CREATE TABLE `rsc_module` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) DEFAULT  '0'  COMMENT '是否启用(0:启用 1:禁用)',
  `name` varchar(500) NOT NULL COMMENT '模块名称',
  `type` varchar(100) COMMENT '模块类型',
  `language` varchar(100) COMMENT '编程语言',
  `description` text COMMENT '备注/描述',
  `local_path` varchar(1000) COMMENT '本地存储路径',
  `network_url` varchar(1000) COMMENT '网络地址',
  `cloud_url` varchar(1000) COMMENT '网盘地址',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  UNIQUE KEY `uk_module_uuid` (`uuid`),
  INDEX `idx_module_name` (`name`(255)),
  INDEX `idx_module_status` (`status`),
  INDEX `idx_module_language` (`language`),
  INDEX `idx_module_type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='功能模块表';

-- 6. 文献-作者关联表
DROP TABLE IF EXISTS `rsc_literature_authors`;

CREATE TABLE `rsc_literature_authors` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `literature_id` bigint NOT NULL COMMENT '文献ID',
  `author_id` bigint NOT NULL COMMENT '作者ID',
  `author_order` int DEFAULT 0 COMMENT '作者顺序',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  UNIQUE KEY `uk_literature_author` (`literature_id`, `author_id`),
  INDEX `idx_literature_authors_author_literature` (`author_id`, `literature_id`),
  INDEX `idx_literature_authors_order` (`author_order`),
  INDEX `idx_literature_authors_literature` (`literature_id`),
  FOREIGN KEY (`literature_id`) REFERENCES `rsc_literature`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`author_id`) REFERENCES `rsc_author`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献-作者关联表';

-- 7. 文献-数据关联表
DROP TABLE IF EXISTS `rsc_literature_datas`;

CREATE TABLE `rsc_literature_datas` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `literature_id` bigint NOT NULL COMMENT '文献ID',
  `data_id` bigint NOT NULL COMMENT '数据ID',
  `relationship_type` varchar(100) COMMENT '关联类型，如"引用","使用"',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  UNIQUE KEY `uk_literature_data` (`literature_id`, `data_id`),
  INDEX `idx_literature_datas_data_literature` (`data_id`, `literature_id`),
  INDEX `idx_literature_datas_literature` (`literature_id`),
  INDEX `idx_literature_datas_relationship` (`relationship_type`),
  FOREIGN KEY (`literature_id`) REFERENCES `rsc_literature`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`data_id`) REFERENCES `rsc_data`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献-数据关联表';

-- 8. 文献-代码关联表
DROP TABLE IF EXISTS `rsc_literature_codes`;

CREATE TABLE `rsc_literature_codes` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `literature_id` bigint NOT NULL COMMENT '文献ID',
  `code_id` bigint NOT NULL COMMENT '代码ID',
  `relationship_type` varchar(100) COMMENT '关联类型',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  UNIQUE KEY `uk_literature_code` (`literature_id`, `code_id`),
  INDEX `idx_literature_codes_code_literature` (`code_id`, `literature_id`),
  INDEX `idx_literature_codes_literature` (`literature_id`),
  INDEX `idx_literature_codes_relationship` (`relationship_type`),
  FOREIGN KEY (`literature_id`) REFERENCES `rsc_literature`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`code_id`) REFERENCES `rsc_code`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献-代码关联表';

-- 9. 数据-代码关联表
DROP TABLE IF EXISTS `rsc_data_codes`;

CREATE TABLE `rsc_data_codes` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `data_id` bigint NOT NULL COMMENT '数据ID',
  `code_id` bigint NOT NULL COMMENT '代码ID',
  `relationship_type` varchar(100) COMMENT '关联类型，如"分析","处理"',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  UNIQUE KEY `uk_data_code` (`data_id`, `code_id`),
  INDEX `idx_data_codes_code_data` (`code_id`, `data_id`),
  INDEX `idx_data_codes_data` (`data_id`),
  INDEX `idx_data_codes_relationship` (`relationship_type`),
  FOREIGN KEY (`data_id`) REFERENCES `rsc_data`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`code_id`) REFERENCES `rsc_code`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据-代码关联表';

-- 10.模块-代码关联表
DROP TABLE IF EXISTS `rsc_module_codes`;

CREATE TABLE `rsc_module_codes` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `module_id` bigint NOT NULL COMMENT '模块ID',
  `code_id` bigint NOT NULL COMMENT '代码ID',
  `relationship_type` varchar(100) COMMENT '关联类型，如"依赖","调用"',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  UNIQUE KEY `uk_module_code` (`module_id`, `code_id`),
  INDEX `idx_module_codes_code_module` (`code_id`, `module_id`),
  INDEX `idx_module_codes_module` (`module_id`),
  INDEX `idx_module_codes_relationship` (`relationship_type`),
  FOREIGN KEY (`module_id`) REFERENCES `rsc_module`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`code_id`) REFERENCES `rsc_code`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='模块-代码关联表';

-- 11.数据-模块关联表
DROP TABLE IF EXISTS `rsc_data_modules`;

CREATE TABLE `rsc_data_modules` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `data_id` bigint NOT NULL COMMENT '数据ID',
  `module_id` bigint NOT NULL COMMENT '模块ID',
  `relationship_type` varchar(100) COMMENT '关联类型，如"处理","分析"',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  UNIQUE KEY `uk_data_module` (`data_id`, `module_id`),
  INDEX `idx_data_modules_module_data` (`module_id`, `data_id`),
  INDEX `idx_data_modules_data` (`data_id`),
  INDEX `idx_data_modules_relationship` (`relationship_type`),
  FOREIGN KEY (`data_id`) REFERENCES `rsc_data`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`module_id`) REFERENCES `rsc_module`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据-模块关联表';