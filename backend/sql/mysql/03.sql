-- 1. 绘图脚本管理表
DROP TABLE IF EXISTS `plot_script`;

CREATE TABLE `plot_script` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `name` varchar(20) NOT NULL COMMENT '绘图脚本名称',
  `alias` varchar(30) NOT NULL COMMENT '脚本英文名称',
  `version` varchar(20) NOT NULL COMMENT '软件版本',
  `field` varchar(20) DEFAULT NULL COMMENT '应用领域',
  `category` varchar(20) DEFAULT NULL COMMENT '功能类别',
  `description` text DEFAULT NULL COMMENT '功能描述',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  -- 索引名称保持与表名一致，语义清晰
  -- 封面图片不单列，用alias命名
  KEY `ix_plot_script_name` (`name`),
  KEY `ix_plot_script_alias` (`alias`),
  KEY `ix_plot_script_field` (`field`),
  KEY `ix_plot_script_category` (`category`),
  KEY `ix_plot_script_description` (`description`(100)),
  KEY `ix_plot_script_created_id` (`created_id`),
  KEY `ix_plot_script_updated_id` (`updated_id`),
  -- 修正外键名称，与表名 plot_script 保持一致，便于识别
  CONSTRAINT `fk_plot_script_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_plot_script_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='绘图脚本管理表';


-- 2. 绘图库包管理表
DROP TABLE IF EXISTS `plot_package`;

CREATE TABLE `plot_package` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `version` varchar(30) NOT NULL COMMENT '库包版本',
  `script_id` int NOT NULL COMMENT '脚本主键ID',
  `url` varchar(200) DEFAULT NULL COMMENT '教程网址',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID（关联sys_user表）',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID（关联sys_user表）',
  -- 索引：外键字段、常用查询字段添加索引，提升查询效率
  KEY `ix_plot_package_version` (`version`),
  KEY `ix_plot_package_script_id` (`script_id`),
  KEY `ix_plot_package_c_reated_id` (`created_id`),
  KEY `ix_plot_package_updated_id` (`updated_id`),
  -- 外键约束：命名规范（fk_表名_字段名），关联关系清晰
  CONSTRAINT `fk_plot_package_script_id` FOREIGN KEY (`script_id`) REFERENCES `plot_script` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_plot_package_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_plot_package_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='绘图库包管理表';

-- 3.绘图方法管理表
DROP TABLE IF EXISTS `plot_method`;

CREATE TABLE `plot_method` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `description` varchar(255) NOT NULL COMMENT '方法描述',
  `order` int NOT NULL DEFAULT 1 COMMENT '方法步骤',
  `script_id` int NOT NULL COMMENT '脚本主键ID',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID（关联sys_user表）',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID（关联sys_user表）',
  -- 索引：外键字段、常用查询字段添加索引，提升查询效率
  KEY `ix_plot_method_order` (`order`),
  KEY `ix_plot_method_script_id` (`script_id`),
  KEY `ix_plot_method_description` (`description`(100)),
  KEY `ix_plot_method_created_id` (`created_id`),
  KEY `ix_plot_method_updated_id` (`updated_id`),
  -- 外键约束：命名规范（fk_表名_字段名），关联关系清晰
  CONSTRAINT `fk_plot_method_script_id` FOREIGN KEY (`script_id`) REFERENCES `plot_script` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_plot_method_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_plot_method_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='绘图方法管理表';


-- 4.绘图实例管理表
DROP TABLE IF EXISTS `plot_sample`;

CREATE TABLE `plot_sample` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `order` int NOT NULL DEFAULT 1 COMMENT '实例序号',
  `description` text NOT NULL COMMENT '实例内容',
  `script_id` int NOT NULL COMMENT '脚本主键ID',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID（关联sys_user表）',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID（关联sys_user表）',
  -- 索引：外键字段、常用查询字段添加索引，提升查询效率
  KEY `ix_plot_sample_order` (`order`),
  KEY `ix_plot_sample_script_id` (`script_id`),
  KEY `ix_plot_sample_description` (`description`(100)),
  KEY `ix_plot_sample_created_id` (`created_id`),
  KEY `ix_plot_sample_updated_id` (`updated_id`),
  -- 外键约束：命名规范（fk_表名_字段名），关联关系清晰
  CONSTRAINT `fk_plot_sample_script_id` FOREIGN KEY (`script_id`) REFERENCES `plot_script` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_plot_sample_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_plot_sample_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='绘图实例管理表';

-- 5.绘图参数管理表
DROP TABLE IF EXISTS `plot_param`;

CREATE TABLE `plot_param` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `group` varchar(10) NOT NULL COMMENT '参数组别',
  `name`  varchar(20) NOT NULL COMMENT '参数名称',
  `order` int NOT NULL DEFAULT 1 COMMENT '参数序号',
  `script_id` int NOT NULL COMMENT '脚本主键ID',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID（关联sys_user表）',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID（关联sys_user表）',
  -- 索引：外键字段、常用查询字段添加索引，提升查询效率
  KEY `ix_plot_param_order` (`order`),
  KEY `ix_plot_param_script_id` (`script_id`),
  KEY `ix_plot_param_group` (`group`),
  KEY `ix_plot_param_name` (`name`),
  KEY `ix_plot_param_created_id` (`created_id`),
  KEY `ix_plot_param_updated_id` (`updated_id`),
  -- 外键约束：命名规范（fk_表名_字段名），关联关系清晰
  CONSTRAINT `fk_plot_param_script_id` FOREIGN KEY (`script_id`) REFERENCES `plot_script` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_plot_param_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_plot_param_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='绘图参数管理表';

-- 6.绘图结果管理表
DROP TABLE IF EXISTS `plot_output`;

CREATE TABLE `plot_output` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键ID',
  `order` int NOT NULL DEFAULT 1 COMMENT '结果序号',
  `name`  varchar(20) NOT NULL COMMENT '结果标题',
  `description` text NOT NULL COMMENT '结果内容',
  `script_id` int NOT NULL COMMENT '脚本主键ID',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID（关联sys_user表）',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID（关联sys_user表）',
  -- 索引：外键字段、常用查询字段添加索引，提升查询效率
  KEY `ix_plot_output_order` (`order`),
  KEY `ix_plot_output_script_id` (`script_id`),
  KEY `ix_plot_output_description` (`description`(100)),
  KEY `ix_plot_output_name` (`name`),
  KEY `ix_plot_output_created_id` (`created_id`),
  KEY `ix_plot_output_updated_id` (`updated_id`),
  -- 外键约束：命名规范（fk_表名_字段名），关联关系清晰
  CONSTRAINT `fk_plot_output_script_id` FOREIGN KEY (`script_id`) REFERENCES `plot_script` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_plot_output_created_id` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_plot_output_updated_id` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='绘图结果管理表';
