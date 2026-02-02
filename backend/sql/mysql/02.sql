-- 1. 绘图模块表
DROP TABLE IF EXISTS `plot_category`;

CREATE TABLE `plot_category` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` VARCHAR(20) NOT NULL COMMENT '模块名称',
  `code` VARCHAR(20) NOT NULL COMMENT '模块编码',
  `category` VARCHAR(20) NOT NULL COMMENT '模块大类',
  `subcategory` VARCHAR(20) NOT NULL COMMENT '模块子类',
  `image` TEXT DEFAULT NULL COMMENT '模块图片',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_id` INT DEFAULT NULL COMMENT '创建人ID',
  `updated_id` INT DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  INDEX `ix_plot_category_created_id` (`created_id`),
  INDEX `ix_plot_category_updated_id` (`updated_id`),
  INDEX `ix_plot_category_created_time` (`created_time`),
  INDEX `ix_plot_category_updated_time` (`updated_time`),
  INDEX `ix_plot_category_code` (`code`),
  CONSTRAINT `plot_category_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `plot_category_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='绘图模块表';