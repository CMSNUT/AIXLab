-- 1. 数据仓库管理表
DROP TABLE IF EXISTS `repo_dataset`;

CREATE TABLE `repo_dataset` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `name` varchar(20) NOT NULL COMMENT '数据仓库名称',
  `alias` varchar(30) NOT NULL COMMENT '数据英文名称',
  `format` varchar(20) NOT NULL COMMENT '数据格式',
  `field` varchar(20) DEFAULT NULL COMMENT '应用领域',
  `category` varchar(20) DEFAULT NULL COMMENT '数据类别',
  `description` text DEFAULT NULL COMMENT '数据描述',
  `local_file` varchar(1000) DEFAULT NULL COMMENT '本地文件',
  `url_link`  varchar(1000) DEFAULT NULL COMMENT '网络地址',
  `cloud_link` varchar(1000) DEFAULT NULL COMMENT '网盘链接',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  KEY `ix_repo_dataset_name` (`name`),
  KEY `ix_repo_dataset_alias` (`alias`),
  KEY `ix_repo_dataset_field` (`field`),
  KEY `ix_repo_dataset_category` (`category`),
  KEY `ix_repo_dataset_description` (`description`(100)),
  KEY `ix_repo_dataset_created_id` (`created_id`),
  KEY `ix_repo_dataset_updated_id` (`updated_id`),
  CONSTRAINT `fk_repo_dataset_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_repo_dataset_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据仓库管理表';


-- 2. 代码仓库管理表
DROP TABLE IF EXISTS `repo_program`;

CREATE TABLE `repo_program` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `name` varchar(20) NOT NULL COMMENT '代码仓库名称',
  `alias` varchar(30) NOT NULL COMMENT '代码英文名称',
  `language` varchar(20) NOT NULL COMMENT '代码语言',
  `field` varchar(20) DEFAULT NULL COMMENT '应用领域',
  `category` varchar(20) DEFAULT NULL COMMENT '功能类别',
  `description` text DEFAULT NULL COMMENT '功能描述',
  `local_file` varchar(1000) DEFAULT NULL COMMENT '本地文件',
  `url_link`  varchar(1000) DEFAULT NULL COMMENT '网络地址',
  `cloud_link` varchar(1000) DEFAULT NULL COMMENT '网盘链接',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  -- 索引名称保持与表名一致，语义清晰
  KEY `ix_repo_program_name` (`name`),
  KEY `ix_repo_program_alias` (`alias`),
  KEY `ix_repo_program_field` (`field`),
  KEY `ix_repo_program_category` (`category`),
  KEY `ix_repo_program_description` (`description`(100)),
  KEY `ix_repo_program_created_id` (`created_id`),
  KEY `ix_repo_program_updated_id` (`updated_id`),
  -- 修正外键名称，与表名 dataset_script 保持一致，便于识别
  CONSTRAINT `fk_repo_program_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_repo_program_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='代码仓库管理表';



-- 3. 案例分析管理表
DROP TABLE IF EXISTS `example_analysis`;

CREATE TABLE `example_analysis` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `name` varchar(20) NOT NULL COMMENT '研究案例名称',
  `field` varchar(20) DEFAULT NULL COMMENT '研究领域',
  `category` varchar(20) DEFAULT NULL COMMENT '研究主题',
  `description` text DEFAULT NULL COMMENT '案例详情内容',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  KEY `ix_example_analysis_name` (`name`),
  KEY `ix_example_analysis_field` (`field`),
  KEY `ix_example_analysis_category` (`category`),
  KEY `ix_example_analysis_description` (`description`(100)),
  KEY `ix_example_analysis_created_id` (`created_id`),
  KEY `ix_example_analysis_updated_id` (`updated_id`),
  CONSTRAINT `fk_example_analysis_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_example_analysis_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='案例分析管理表';


-- 4. 案例节点管理表
DROP TABLE IF EXISTS `example_section`;

CREATE TABLE `example_section` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `name` varchar(50) NOT NULL COMMENT '案例节点研究主题',
  `description` text DEFAULT NULL COMMENT '案例节点研究内容',
  `analysis_id` int NOT NULL COMMENT '案例分析ID',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  KEY `ix_example_section_name` (`name`),
  KEY `ix_example_section_description` (`description`(100)),
  KEY `ix_example_section_created_id` (`created_id`),
  KEY `ix_example_section_updated_id` (`updated_id`),
  CONSTRAINT `fk_example_section_analysis_id` FOREIGN KEY (`analysis_id`) REFERENCES `example_analysis` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_example_section_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_example_section_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='案例节点管理表';

-- 5. 案例节点数据管理表
DROP TABLE IF EXISTS `example_section_datasets`;

CREATE TABLE `example_section_datasets` (
  `node_id` int NOT NULL COMMENT '案例节点ID',
  `dataset_id` int NOT NULL COMMENT '数据仓库ID',
  PRIMARY KEY (`node_id`,`dataset_id`),
  KEY `ix_example_section_datasets_dataset_id` (`dataset_id`),
  CONSTRAINT `example_section_datasets_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `example_section` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `example_section_datasets_ibfk_2` FOREIGN KEY (`dataset_id`) REFERENCES `repo_program` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='案例节点数据关联表';

-- 6. 案例节点代码管理表
DROP TABLE IF EXISTS `example_section_programs`;

CREATE TABLE `example_section_programs` (
  `node_id` int NOT NULL COMMENT '案例节点ID',
  `program_id` int NOT NULL COMMENT '代码仓库ID',
  PRIMARY KEY (`node_id`,`program_id`),
  KEY `ix_example_section_programs_program_id` (`program_id`),
  CONSTRAINT `example_section_programs_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `example_section` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `example_section_programs_ibfk_2` FOREIGN KEY (`program_id`) REFERENCES `repo_program` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='案例节点代码关联表';


-- 7. 案例分析笔记管理表
DROP TABLE IF EXISTS `example_note`;

CREATE TABLE `example_note` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `name` varchar(50) NOT NULL COMMENT '笔记名称',
  `description` text DEFAULT NULL COMMENT '笔记内容',
  `analysis_id` int NOT NULL COMMENT '案例分析ID',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  KEY `ix_example_note_name` (`name`),
  KEY `ix_example_note_description` (`description`(100)),
  KEY `ix_example_note_created_id` (`created_id`),
  KEY `ix_example_note_updated_id` (`updated_id`),
  CONSTRAINT `fk_example_analysis_note_id` FOREIGN KEY (`analysis_id`) REFERENCES `example_analysis` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_example_note_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_example_note_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='案例分析笔记管理表';



