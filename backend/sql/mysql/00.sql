-- 学科分类表
DROP TABLE IF EXISTS `resource_subject`;
CREATE TABLE `resource_subject` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `code` VARCHAR(50) NOT NULL UNIQUE COMMENT '学科代码，如0809、080901',
    `name` VARCHAR(200) NOT NULL COMMENT '学科名称',
    `english_name` VARCHAR(300) COMMENT '英文名称',
    `level` TINYINT NOT NULL DEFAULT 1 COMMENT '层级：1-一级学科，2-二级学科',
    `parent_id` INT DEFAULT NULL COMMENT '上级学科ID，一级学科为NULL',
    `description` TEXT COMMENT '学科描述',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    UNIQUE INDEX `uk_resource_subject_code` (`code`),
    INDEX `idx_resource_subject_name` (`name`),
    INDEX `idx_resource_subject_level` (`level`),
    INDEX `idx_resource_subject_parent_id` (`parent_id`),
    INDEX `idx_resource_subject_created_at` (`created_at`),
    INDEX `idx_resource_subject_is_deleted` (`is_deleted`),
    
    FULLTEXT INDEX `ft_resource_subject_name_desc` (`name`, `description`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='学科分类表';