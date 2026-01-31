-- 1. 研究课题表
DROP TABLE IF EXISTS `project_subject`;
CREATE TABLE `project_subject` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(255) NOT NULL COMMENT '课题名称',
  `code` varchar(20) DEFAULT NULL COMMENT '课题编号',
  `field` varchar(10) DEFAULT NULL COMMENT '课题领域',
  `content` longtext DEFAULT NULL COMMENT '课题简介',
  `start_date` datetime DEFAULT NULL COMMENT '开始日期',
  `end_date` datetime DEFAULT NULL COMMENT '结束日期',
  `progress` varchar(10) DEFAULT NULL COMMENT '课题进度',
  `description` text DEFAULT NULL COMMENT '备注/描述',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  KEY `ix_project_subject_name` (`name`),
  KEY `ix_project_subject_field` (`field`),
  KEY `ix_project_subject_code` (`code`),
  KEY `ix_project_subject_progress` (`progress`),
  CONSTRAINT `fk_project_subject_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_project_subject_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='研究课题表';

-- 2. 研究内容表
DROP TABLE IF EXISTS `project_topic`;
CREATE TABLE `project_topic` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(100) NOT NULL COMMENT '内容名称',
  `type` varchar(20) DEFAULT NULL COMMENT '内容类型',
  `subject_id` int DEFAULT NULL COMMENT '所属课题ID',
  `content` longtext DEFAULT NULL COMMENT '内容简介',
  `description` text DEFAULT NULL COMMENT '备注/描述',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  KEY `ix_project_topic_name` (`name`),
  KEY `ix_project_topic_subject_id` (`subject_id`),
  CONSTRAINT `fk_project_topic_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_project_topic_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_project_topic_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `project_subject` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='研究内容表';

-- 3. 研究方法表
DROP TABLE IF EXISTS `project_method`;
CREATE TABLE `project_method` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(255) NOT NULL COMMENT '方法名称',
  `type` varchar(10) DEFAULT NULL COMMENT '方法类型',
  `category` varchar(10) DEFAULT NULL COMMENT '方法分类',
  `topic_id` int DEFAULT NULL COMMENT '所属内容ID',
  `content` longtext DEFAULT NULL COMMENT '方法简介',
  `description` text DEFAULT NULL COMMENT '备注/描述',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  KEY `ix_project_method_name` (`name`),
  KEY `ix_project_method_topic_id` (`topic_id`),
  KEY `ix_project_method_type` (`type`),
  KEY `ix_project_method_category` (`category`),
  CONSTRAINT `fk_project_method_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_project_method_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_project_method_topic_id` FOREIGN KEY (`topic_id`) REFERENCES `project_topic` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='研究方法表';

-- 4. 研究结果表
DROP TABLE IF EXISTS `project_result`;
CREATE TABLE `project_result` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(100) NOT NULL COMMENT '结果名称',
  `type` varchar(10) DEFAULT NULL COMMENT '结果类型',
  `method_id` int DEFAULT NULL COMMENT '所属方法ID',
  `content` longtext DEFAULT NULL COMMENT '结果内容',
  `description` text DEFAULT NULL COMMENT '备注/描述',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  KEY `ix_project_result_name` (`name`),
  KEY `ix_project_result_method_id` (`method_id`),
  CONSTRAINT `fk_project_result_method_id` FOREIGN KEY (`method_id`) REFERENCES `project_method` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_project_result_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_project_result_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='研究结果表';

-- 5. 研究成果表
DROP TABLE IF EXISTS `project_achievement`;
CREATE TABLE `project_achievement` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(255) NOT NULL COMMENT '成果名称',
  `type` varchar(10) DEFAULT NULL COMMENT '成果类型',
  `subject_id` int DEFAULT NULL COMMENT '所属课题ID',
  `local_path` varchar(1000) DEFAULT NULL COMMENT '本地文件',
  `network_url` varchar(1000) DEFAULT NULL COMMENT '网络地址',
  `cloud_url` varchar(1000) DEFAULT NULL COMMENT '网盘地址',
  `description` text DEFAULT NULL COMMENT '备注/描述',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  KEY `ix_project_achievement_name` (`name`),
  KEY `ix_project_achievement_subject_id` (`subject_id`),
  CONSTRAINT `fk_project_achievement_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `project_subject` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_project_achievement_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_project_achievement_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='研究成果表';

-- 6. 方法-文献关联表
DROP TABLE IF EXISTS `project_method_papers`;
CREATE TABLE `project_method_papers` (
  `method_id` int NOT NULL COMMENT '方法ID',
  `paper_id` int NOT NULL COMMENT '文献ID',
  PRIMARY KEY (`method_id`, `paper_id`),
  KEY `ix_project_method_papers_paper_id` (`paper_id`),
  CONSTRAINT `fk_project_method_papers_method_id` FOREIGN KEY (`method_id`) REFERENCES `project_method` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_project_method_papers_paper_id` FOREIGN KEY (`paper_id`) REFERENCES `resource_paper` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='方法文献关联表';

-- 7. 方法-数据关联表
DROP TABLE IF EXISTS `project_method_datas`;
CREATE TABLE `project_method_datas` (
  `method_id` int NOT NULL COMMENT '方法ID',
  `data_id` int NOT NULL COMMENT '数据ID',
  PRIMARY KEY (`method_id`, `data_id`),
  KEY `ix_project_method_datas_data_id` (`data_id`),
  CONSTRAINT `fk_project_method_datas_method_id` FOREIGN KEY (`method_id`) REFERENCES `project_method` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_project_method_datas_data_id` FOREIGN KEY (`data_id`) REFERENCES `resource_data` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='方法数据关联表';

-- 8. 方法-脚本关联表
DROP TABLE IF EXISTS `project_method_scripts`;
CREATE TABLE `project_method_scripts` (
  `method_id` int NOT NULL COMMENT '方法ID',
  `script_id` int NOT NULL COMMENT '脚本ID',
  PRIMARY KEY (`method_id`, `script_id`),
  KEY `ix_project_method_scripts_script_id` (`script_id`),
  CONSTRAINT `fk_project_method_scripts_method_id` FOREIGN KEY (`method_id`) REFERENCES `project_method` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_project_method_scripts_script_id` FOREIGN KEY (`script_id`) REFERENCES `resource_script` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='方法脚本关联表';

-- 9. 方法-功能关联表
DROP TABLE IF EXISTS `project_method_kits`;
CREATE TABLE `project_method_kits` (
  `method_id` int NOT NULL COMMENT '方法ID',
  `kit_id` int NOT NULL COMMENT '功能ID',
  PRIMARY KEY (`method_id`, `kit_id`),
  KEY `ix_project_method_kits_kit_id` (`kit_id`),
  CONSTRAINT `fk_project_method_kits_method_id` FOREIGN KEY (`method_id`) REFERENCES `project_method` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_project_method_kits_kit_id` FOREIGN KEY (`kit_id`) REFERENCES `resource_kit` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='方法功能关联表';