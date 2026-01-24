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

-- 研究领域表
DROP TABLE IF EXISTS `resource_field`;
CREATE TABLE `resource_field` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `code` VARCHAR(50),
    `subject_id` INT COMMENT '关联学科分类',
    `parent_id` INT,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    UNIQUE INDEX `uk_resource_field_code` (`code`),
    INDEX `idx_resource_field_name` (`name`),
    INDEX `idx_resource_field_subject_id` (`subject_id`),
    INDEX `idx_resource_field_parent_id` (`parent_id`),
    INDEX `idx_resource_field_created_at` (`created_at`),
    INDEX `idx_resource_field_is_deleted` (`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='研究领域表';

-- 研究方向表
DROP TABLE IF EXISTS `resource_interest`;
CREATE TABLE `resource_interest` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(300) NOT NULL,
    `description` TEXT,
    `subject_id` INT COMMENT '关联学科分类',
    `field_id` INT COMMENT '关联研究领域',
    `lead_member_id` INT COMMENT '负责人',
    `status` VARCHAR(20) DEFAULT 'active' COMMENT '状态：active/inactive/completed',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_interest_title` (`title`),
    INDEX `idx_resource_interest_subject_id` (`subject_id`),
    INDEX `idx_resource_interest_field_id` (`field_id`),
    INDEX `idx_resource_interest_status` (`status`),
    INDEX `idx_resource_interest_created_at` (`created_at`),
    INDEX `idx_resource_interest_is_deleted` (`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='研究方向表';

-- 作者表
DROP TABLE IF EXISTS `resource_author`;
CREATE TABLE `resource_author` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(200) NOT NULL,
    `english_name` VARCHAR(300),
    `orcid` VARCHAR(20),
    `researcher_id` VARCHAR(50),
    `email` VARCHAR(200),
    `research_interests` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    UNIQUE INDEX `uk_resource_author_orcid` (`orcid`),
    INDEX `idx_resource_author_name` (`name`),
    INDEX `idx_resource_author_english_name` (`english_name`),
    INDEX `idx_resource_author_email` (`email`),
    INDEX `idx_resource_author_researcher_id` (`researcher_id`),
    INDEX `idx_resource_author_created_at` (`created_at`),
    INDEX `idx_resource_author_is_deleted` (`is_deleted`),
    
    FULLTEXT INDEX `ft_resource_author_name_interests` (`name`, `research_interests`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='作者表';

-- 机构表
DROP TABLE IF EXISTS `resource_institution`;
CREATE TABLE `resource_institution` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(500) NOT NULL,
    `english_name` VARCHAR(500),
    `type` VARCHAR(50) COMMENT '机构类型：university/research_institute/company等',
    `country` VARCHAR(100),
    `province` VARCHAR(100),
    `city` VARCHAR(100),
    `address` VARCHAR(500),
    `website` VARCHAR(500),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_institution_name` (`name`(100)),
    INDEX `idx_resource_institution_type` (`type`),
    INDEX `idx_resource_institution_country` (`country`),
    INDEX `idx_resource_institution_city` (`city`),
    INDEX `idx_resource_institution_created_at` (`created_at`),
    INDEX `idx_resource_institution_is_deleted` (`is_deleted`),
    
    FULLTEXT INDEX `ft_resource_institution_name` (`name`, `english_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='机构表';

-- 文献表
DROP TABLE IF EXISTS `resource_publication`;
CREATE TABLE `resource_publication` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `doi` VARCHAR(200) UNIQUE COMMENT '数字对象标识符',
    `title` VARCHAR(1000) NOT NULL,
    `english_title` VARCHAR(1000),
    `abstract` TEXT,
    `english_abstract` TEXT,
    `keywords` VARCHAR(500),
    `english_keywords` VARCHAR(500),
    `type` VARCHAR(50) COMMENT '文献类型：journal_article/conference_paper/book_chapter等',
    `publish_date` DATE,
    `online_date` DATE COMMENT '在线发表日期',
    `source_title` VARCHAR(500) COMMENT '来源标题（期刊/会议名称）',
    `source_issn` VARCHAR(20) COMMENT '来源ISSN',
    `volume` VARCHAR(50),
    `issue` VARCHAR(50),
    `pages` VARCHAR(50),
    `article_number` VARCHAR(100) COMMENT '文章编号',
    `citation_count` INT DEFAULT 0,
    `reference_count` INT DEFAULT 0,
    `file_path` VARCHAR(500) COMMENT '文件存储路径',
    `file_url` VARCHAR(500) COMMENT '文件URL',
    `access_level` VARCHAR(20) DEFAULT 'private' COMMENT '访问权限：public/private/team',
    `subject_id` INT COMMENT '主要学科分类',
    `field_id` INT COMMENT '主要研究领域',
    `created_by` INT COMMENT '添加者',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    `has_corpus` TINYINT(1) DEFAULT 0 COMMENT '是否有语料',
    `corpus_status` VARCHAR(20) DEFAULT 'none' COMMENT '语料状态：none/extracted/processed',
    `corpus_processed_at` DATETIME COMMENT '语料处理时间',
    
    UNIQUE INDEX `uk_resource_publication_doi` (`doi`),
    INDEX `idx_resource_publication_title` (`title`(100)),
    INDEX `idx_resource_publication_publish_date` (`publish_date`),
    INDEX `idx_resource_publication_type` (`type`),
    INDEX `idx_resource_publication_access_level` (`access_level`),
    INDEX `idx_resource_publication_subject_id` (`subject_id`),
    INDEX `idx_resource_publication_field_id` (`field_id`),
    INDEX `idx_resource_publication_created_by` (`created_by`),
    INDEX `idx_resource_publication_citation_count` (`citation_count`),
    INDEX `idx_resource_publication_created_at` (`created_at`),
    INDEX `idx_resource_publication_is_deleted` (`is_deleted`),
    INDEX `idx_resource_publication_has_corpus` (`has_corpus`),
    INDEX `idx_resource_publication_corpus_status` (`corpus_status`),
    
    INDEX `idx_resource_publication_subject_date` (`subject_id`, `publish_date`),
    
    FULLTEXT INDEX `ft_resource_publication_title_abstract` (`title`, `english_title`, `abstract`, `english_abstract`),
    FULLTEXT INDEX `ft_resource_publication_keywords` (`keywords`, `english_keywords`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献表';

-- 文献作者关联表
DROP TABLE IF EXISTS `resource_publication_author`;
CREATE TABLE `resource_publication_author` (
    `publication_id` INT NOT NULL,
    `author_id` INT NOT NULL,
    `institution_id` INT COMMENT '作者当时所属机构',
    `author_order` INT NOT NULL COMMENT '作者顺序，从1开始',
    `is_corresponding` TINYINT(1) DEFAULT 0 COMMENT '是否通讯作者',
    `email` VARCHAR(200) COMMENT '作者邮箱（文章中的）',
    `contribution` TEXT COMMENT '作者贡献说明',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`publication_id`, `author_id`),
    
    INDEX `idx_resource_publication_author_publication` (`publication_id`),
    INDEX `idx_resource_publication_author_author` (`author_id`),
    INDEX `idx_resource_publication_author_institution` (`institution_id`),
    INDEX `idx_resource_publication_author_order` (`author_order`),
    INDEX `idx_resource_publication_author_is_corresponding` (`is_corresponding`),
    INDEX `idx_resource_publication_author_created_at` (`created_at`),
    
    INDEX `idx_resource_publication_author_author_institution` (`author_id`, `institution_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献作者关联表';

-- 文献学科关联表
DROP TABLE IF EXISTS `resource_publication_subject`;
CREATE TABLE `resource_publication_subject` (
    `publication_id` INT NOT NULL,
    `subject_id` INT NOT NULL,
    `is_primary` TINYINT(1) DEFAULT 0 COMMENT '是否主要学科',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`publication_id`, `subject_id`),
    
    INDEX `idx_resource_publication_subject_publication` (`publication_id`),
    INDEX `idx_resource_publication_subject_subject` (`subject_id`),
    INDEX `idx_resource_publication_subject_is_primary` (`is_primary`),
    INDEX `idx_resource_publication_subject_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献学科关联表';

-- 文献解读表
DROP TABLE IF EXISTS `resource_interpretation`;
CREATE TABLE `resource_interpretation` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `publication_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `title` VARCHAR(300) NOT NULL,
    `content` LONGTEXT,
    `summary` TEXT,
    `tags` VARCHAR(500),
    `is_public` TINYINT(1) DEFAULT 0,
    `view_count` INT DEFAULT 0,
    `like_count` INT DEFAULT 0,
    `comment_count` INT DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_interpretation_publication` (`publication_id`),
    INDEX `idx_resource_interpretation_user` (`user_id`),
    INDEX `idx_resource_interpretation_is_public` (`is_public`),
    INDEX `idx_resource_interpretation_view_count` (`view_count`),
    INDEX `idx_resource_interpretation_like_count` (`like_count`),
    INDEX `idx_resource_interpretation_created_at` (`created_at`),
    INDEX `idx_resource_interpretation_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_interpretation_publication_user` (`publication_id`, `user_id`),
    
    FULLTEXT INDEX `ft_resource_interpretation_content` (`title`, `content`, `summary`, `tags`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献解读表';

-- 文献附件表
DROP TABLE IF EXISTS `resource_attachment`;
CREATE TABLE `resource_attachment` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `publication_id` INT NOT NULL,
    `type` VARCHAR(50) NOT NULL COMMENT '附件类型：figure/table/data/code/supplement/material',
    `title` VARCHAR(500),
    `description` TEXT,
    `file_path` VARCHAR(500),
    `file_url` VARCHAR(500),
    `file_format` VARCHAR(50),
    `file_size` BIGINT,
    `metadata` JSON,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_attachment_publication` (`publication_id`),
    INDEX `idx_resource_attachment_type` (`type`),
    INDEX `idx_resource_attachment_file_format` (`file_format`),
    INDEX `idx_resource_attachment_created_at` (`created_at`),
    INDEX `idx_resource_attachment_is_deleted` (`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献附件表';

-- 语料表
DROP TABLE IF EXISTS `resource_corpus`;
CREATE TABLE `resource_corpus` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(500) NOT NULL COMMENT '语料标题',
    `content` LONGTEXT NOT NULL COMMENT '语料内容',
    `source_type` VARCHAR(50) COMMENT '来源类型：publication/web/manual等',
    `source_id` INT COMMENT '来源ID，如文献ID',
    `source_reference` VARCHAR(1000) COMMENT '来源引用信息',
    `language` VARCHAR(20) DEFAULT 'zh' COMMENT '语言：zh/en等',
    `character_count` INT COMMENT '字符数',
    `word_count` INT COMMENT '词数',
    `subject_id` INT COMMENT '主要学科分类',
    `field_id` INT COMMENT '主要研究领域',
    `topic_id` INT COMMENT '关联课题',
    `tags` VARCHAR(500) COMMENT '标签',
    `processing_status` VARCHAR(20) DEFAULT 'raw' COMMENT '处理状态：raw/processed/analyzed',
    `access_level` VARCHAR(20) DEFAULT 'private' COMMENT '访问权限：public/private/team',
    `created_by` INT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_corpus_title` (`title`(100)),
    INDEX `idx_resource_corpus_source_type` (`source_type`),
    INDEX `idx_resource_corpus_source_id` (`source_id`),
    INDEX `idx_resource_corpus_language` (`language`),
    INDEX `idx_resource_corpus_subject_id` (`subject_id`),
    INDEX `idx_resource_corpus_field_id` (`field_id`),
    INDEX `idx_resource_corpus_topic_id` (`topic_id`),
    INDEX `idx_resource_corpus_processing_status` (`processing_status`),
    INDEX `idx_resource_corpus_access_level` (`access_level`),
    INDEX `idx_resource_corpus_created_by` (`created_by`),
    INDEX `idx_resource_corpus_created_at` (`created_at`),
    INDEX `idx_resource_corpus_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_corpus_source` (`source_type`, `source_id`),
    INDEX `idx_resource_corpus_language_status` (`language`, `processing_status`),
    
    FULLTEXT INDEX `ft_resource_corpus_content` (`title`, `content`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料表';

-- 文献语料关联表
DROP TABLE IF EXISTS `resource_publication_corpus`;
CREATE TABLE `resource_publication_corpus` (
    `publication_id` INT NOT NULL,
    `corpus_id` INT NOT NULL,
    `corpus_type` VARCHAR(50) COMMENT '语料类型：abstract/full_text/section/conclusion',
    `section_title` VARCHAR(500) COMMENT '章节标题',
    `section_order` INT COMMENT '章节顺序',
    `word_count` INT COMMENT '字数',
    `is_primary` TINYINT(1) DEFAULT 0 COMMENT '是否主要语料',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`publication_id`, `corpus_id`),
    
    INDEX `idx_resource_publication_corpus_publication` (`publication_id`),
    INDEX `idx_resource_publication_corpus_corpus` (`corpus_id`),
    INDEX `idx_resource_publication_corpus_type` (`corpus_type`),
    INDEX `idx_resource_publication_corpus_section_order` (`section_order`),
    INDEX `idx_resource_publication_corpus_is_primary` (`is_primary`),
    INDEX `idx_resource_publication_corpus_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文献语料关联表';

-- 语料处理结果表
DROP TABLE IF EXISTS `resource_corpus_processing`;
CREATE TABLE `resource_corpus_processing` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `corpus_id` INT NOT NULL,
    `processing_type` VARCHAR(50) NOT NULL COMMENT '处理类型：segmentation/pos_tagging/ner/sentiment',
    `processing_tool` VARCHAR(200) COMMENT '处理工具',
    `processing_version` VARCHAR(50) COMMENT '处理版本',
    `parameters` JSON COMMENT '处理参数',
    `result_data` LONGTEXT COMMENT '处理结果数据（JSON格式）',
    `result_summary` TEXT COMMENT '处理结果摘要',
    `accuracy_score` DECIMAL(5,4) COMMENT '准确率',
    `processing_time_ms` INT COMMENT '处理时间（毫秒）',
    `created_by` INT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_corpus_processing_corpus` (`corpus_id`),
    INDEX `idx_resource_corpus_processing_type` (`processing_type`),
    INDEX `idx_resource_corpus_processing_tool` (`processing_tool`),
    INDEX `idx_resource_corpus_processing_created_at` (`created_at`),
    INDEX `idx_resource_corpus_processing_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_corpus_processing_corpus_type` (`corpus_id`, `processing_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料处理结果表';

-- 语料分词表
DROP TABLE IF EXISTS `resource_corpus_token`;
CREATE TABLE `resource_corpus_token` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `corpus_id` INT NOT NULL,
    `processing_id` INT COMMENT '关联处理记录',
    `token_text` VARCHAR(200) NOT NULL COMMENT '词元文本',
    `token_type` VARCHAR(50) COMMENT '词性标签',
    `token_position` INT COMMENT '位置索引',
    `token_length` INT COMMENT '词长度',
    `token_frequency` INT DEFAULT 1 COMMENT '词频',
    `sentiment_score` DECIMAL(5,4) COMMENT '情感得分',
    `entity_type` VARCHAR(50) COMMENT '实体类型',
    `dependency_head` INT COMMENT '依存句法头位置',
    `dependency_relation` VARCHAR(50) COMMENT '依存关系',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX `idx_resource_corpus_token_corpus` (`corpus_id`),
    INDEX `idx_resource_corpus_token_processing` (`processing_id`),
    INDEX `idx_resource_corpus_token_text` (`token_text`),
    INDEX `idx_resource_corpus_token_type` (`token_type`),
    INDEX `idx_resource_corpus_token_position` (`token_position`),
    INDEX `idx_resource_corpus_token_frequency` (`token_frequency`),
    INDEX `idx_resource_corpus_token_entity_type` (`entity_type`),
    INDEX `idx_resource_corpus_token_created_at` (`created_at`),
    
    INDEX `idx_resource_corpus_token_corpus_text` (`corpus_id`, `token_text`),
    INDEX `idx_resource_corpus_token_corpus_type` (`corpus_id`, `token_type`),
    
    FULLTEXT INDEX `ft_resource_corpus_token_text` (`token_text`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料分词表';

-- 语料关键词表
DROP TABLE IF EXISTS `resource_corpus_keyword`;
CREATE TABLE `resource_corpus_keyword` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `corpus_id` INT NOT NULL,
    `processing_id` INT COMMENT '关联处理记录',
    `keyword` VARCHAR(200) NOT NULL COMMENT '关键词',
    `keyword_type` VARCHAR(50) COMMENT '关键词类型：noun/verb/entity',
    `tf` DECIMAL(10,6) COMMENT '词频',
    `tfidf` DECIMAL(10,6) COMMENT 'TF-IDF值',
    `weight` DECIMAL(10,6) COMMENT '权重',
    `rank` INT COMMENT '排名',
    `is_important` TINYINT(1) DEFAULT 0 COMMENT '是否重要关键词',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX `idx_resource_corpus_keyword_corpus` (`corpus_id`),
    INDEX `idx_resource_corpus_keyword_processing` (`processing_id`),
    INDEX `idx_resource_corpus_keyword_keyword` (`keyword`),
    INDEX `idx_resource_corpus_keyword_type` (`keyword_type`),
    INDEX `idx_resource_corpus_keyword_weight` (`weight`),
    INDEX `idx_resource_corpus_keyword_rank` (`rank`),
    INDEX `idx_resource_corpus_keyword_is_important` (`is_important`),
    INDEX `idx_resource_corpus_keyword_created_at` (`created_at`),
    
    INDEX `idx_resource_corpus_keyword_corpus_weight` (`corpus_id`, `weight` DESC),
    
    FULLTEXT INDEX `ft_resource_corpus_keyword_keyword` (`keyword`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料关键词表';

-- 语料主题表
DROP TABLE IF EXISTS `resource_corpus_topic`;
CREATE TABLE `resource_corpus_topic` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `corpus_id` INT NOT NULL,
    `processing_id` INT COMMENT '关联处理记录',
    `topic_id` INT COMMENT '主题编号',
    `topic_name` VARCHAR(200) COMMENT '主题名称',
    `topic_weight` DECIMAL(10,6) COMMENT '主题权重',
    `topic_keywords` TEXT COMMENT '主题关键词（JSON格式）',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX `idx_resource_corpus_topic_corpus` (`corpus_id`),
    INDEX `idx_resource_corpus_topic_processing` (`processing_id`),
    INDEX `idx_resource_corpus_topic_topic_id` (`topic_id`),
    INDEX `idx_resource_corpus_topic_weight` (`topic_weight`),
    INDEX `idx_resource_corpus_topic_created_at` (`created_at`),
    
    INDEX `idx_resource_corpus_topic_corpus_weight` (`corpus_id`, `topic_weight` DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料主题表';

-- 语料情感分析表
DROP TABLE IF EXISTS `resource_corpus_sentiment`;
CREATE TABLE `resource_corpus_sentiment` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `corpus_id` INT NOT NULL,
    `processing_id` INT COMMENT '关联处理记录',
    `sentiment_type` VARCHAR(50) COMMENT '情感类型：positive/negative/neutral',
    `sentiment_score` DECIMAL(5,4) COMMENT '情感得分',
    `confidence` DECIMAL(5,4) COMMENT '置信度',
    `positive_probability` DECIMAL(5,4) COMMENT '积极概率',
    `negative_probability` DECIMAL(5,4) COMMENT '消极概率',
    `neutral_probability` DECIMAL(5,4) COMMENT '中性概率',
    `sentiment_keywords` TEXT COMMENT '情感关键词（JSON格式）',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX `idx_resource_corpus_sentiment_corpus` (`corpus_id`),
    INDEX `idx_resource_corpus_sentiment_processing` (`processing_id`),
    INDEX `idx_resource_corpus_sentiment_type` (`sentiment_type`),
    INDEX `idx_resource_corpus_sentiment_score` (`sentiment_score`),
    INDEX `idx_resource_corpus_sentiment_created_at` (`created_at`),
    
    INDEX `idx_resource_corpus_sentiment_corpus_type` (`corpus_id`, `sentiment_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料情感分析表';

-- 语料向量表
DROP TABLE IF EXISTS `resource_corpus_vector`;
CREATE TABLE `resource_corpus_vector` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `corpus_id` INT NOT NULL,
    `processing_id` INT COMMENT '关联处理记录',
    `model_name` VARCHAR(200) NOT NULL COMMENT '向量模型名称',
    `model_version` VARCHAR(50) COMMENT '模型版本',
    `vector_dimension` INT COMMENT '向量维度',
    `vector_data` LONGTEXT COMMENT '向量数据（JSON格式）',
    `normalized_vector` LONGTEXT COMMENT '归一化向量',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_corpus_vector_corpus` (`corpus_id`),
    INDEX `idx_resource_corpus_vector_processing` (`processing_id`),
    INDEX `idx_resource_corpus_vector_model_name` (`model_name`),
    INDEX `idx_resource_corpus_vector_created_at` (`created_at`),
    INDEX `idx_resource_corpus_vector_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_corpus_vector_corpus_model` (`corpus_id`, `model_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料向量表';

-- 语料相似度表
DROP TABLE IF EXISTS `resource_corpus_similarity`;
CREATE TABLE `resource_corpus_similarity` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `corpus_id_1` INT NOT NULL COMMENT '语料1ID',
    `corpus_id_2` INT NOT NULL COMMENT '语料2ID',
    `processing_id` INT COMMENT '关联处理记录',
    `model_name` VARCHAR(200) COMMENT '相似度计算模型',
    `similarity_type` VARCHAR(50) COMMENT '相似度类型：cosine/euclidean/jaccard',
    `similarity_score` DECIMAL(10,8) COMMENT '相似度得分',
    `is_similar` TINYINT(1) DEFAULT 0 COMMENT '是否相似',
    `similarity_threshold` DECIMAL(5,4) COMMENT '相似度阈值',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX `idx_resource_corpus_similarity_corpus1` (`corpus_id_1`),
    INDEX `idx_resource_corpus_similarity_corpus2` (`corpus_id_2`),
    INDEX `idx_resource_corpus_similarity_processing` (`processing_id`),
    INDEX `idx_resource_corpus_similarity_model_name` (`model_name`),
    INDEX `idx_resource_corpus_similarity_score` (`similarity_score`),
    INDEX `idx_resource_corpus_similarity_is_similar` (`is_similar`),
    INDEX `idx_resource_corpus_similarity_created_at` (`created_at`),
    
    INDEX `idx_resource_corpus_similarity_corpus_pair` (`corpus_id_1`, `corpus_id_2`),
    INDEX `idx_resource_corpus_similarity_score_threshold` (`similarity_score`, `similarity_threshold`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料相似度表';

-- 语料分类表
DROP TABLE IF EXISTS `resource_corpus_category`;
CREATE TABLE `resource_corpus_category` (
    `corpus_id` INT NOT NULL,
    `category_type` VARCHAR(50) NOT NULL COMMENT '分类类型：topic/subject/field',
    `category_id` INT NOT NULL COMMENT '分类ID',
    `confidence` DECIMAL(5,4) COMMENT '分类置信度',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`corpus_id`, `category_type`, `category_id`),
    
    INDEX `idx_resource_corpus_category_corpus` (`corpus_id`),
    INDEX `idx_resource_corpus_category_type` (`category_type`),
    INDEX `idx_resource_corpus_category_id` (`category_id`),
    INDEX `idx_resource_corpus_category_confidence` (`confidence`),
    INDEX `idx_resource_corpus_category_created_at` (`created_at`),
    
    INDEX `idx_resource_corpus_category_type_id` (`category_type`, `category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料分类表';

-- 语料统计表
DROP TABLE IF EXISTS `resource_corpus_statistics`;
CREATE TABLE `resource_corpus_statistics` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `corpus_id` INT NOT NULL,
    `total_characters` INT DEFAULT 0 COMMENT '总字符数',
    `total_words` INT DEFAULT 0 COMMENT '总词数',
    `unique_words` INT DEFAULT 0 COMMENT '唯一词数',
    `average_word_length` DECIMAL(6,2) COMMENT '平均词长',
    `sentence_count` INT DEFAULT 0 COMMENT '句子数',
    `paragraph_count` INT DEFAULT 0 COMMENT '段落数',
    `keyword_count` INT DEFAULT 0 COMMENT '关键词数',
    `named_entity_count` INT DEFAULT 0 COMMENT '命名实体数',
    `topic_count` INT DEFAULT 0 COMMENT '主题数',
    `sentiment_score_avg` DECIMAL(5,4) COMMENT '平均情感得分',
    `readability_score` DECIMAL(6,2) COMMENT '可读性得分',
    `statistics_date` DATE COMMENT '统计日期',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX `idx_resource_corpus_statistics_corpus` (`corpus_id`),
    INDEX `idx_resource_corpus_statistics_date` (`statistics_date`),
    INDEX `idx_resource_corpus_statistics_created_at` (`created_at`),
    
    UNIQUE INDEX `uk_resource_corpus_statistics_corpus_date` (`corpus_id`, `statistics_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料统计表';

-- 词频统计表
DROP TABLE IF EXISTS `resource_word_frequency`;
CREATE TABLE `resource_word_frequency` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `word` VARCHAR(200) NOT NULL COMMENT '词语',
    `word_type` VARCHAR(50) COMMENT '词性',
    `corpus_id` INT COMMENT '语料ID（为空表示全局统计）',
    `frequency` INT DEFAULT 0 COMMENT '频率',
    `document_frequency` INT DEFAULT 0 COMMENT '文档频率',
    `tfidf` DECIMAL(10,6) COMMENT 'TF-IDF值',
    `statistics_date` DATE COMMENT '统计日期',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX `idx_resource_word_frequency_word` (`word`),
    INDEX `idx_resource_word_frequency_corpus` (`corpus_id`),
    INDEX `idx_resource_word_frequency_frequency` (`frequency`),
    INDEX `idx_resource_word_frequency_tfidf` (`tfidf`),
    INDEX `idx_resource_word_frequency_date` (`statistics_date`),
    INDEX `idx_resource_word_frequency_created_at` (`created_at`),
    
    INDEX `idx_resource_word_frequency_corpus_word` (`corpus_id`, `word`),
    
    UNIQUE INDEX `uk_resource_word_frequency_word_corpus_date` (`word`, `corpus_id`, `statistics_date`),
    
    FULLTEXT INDEX `ft_resource_word_frequency_word` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='词频统计表';

-- 语料分析工具表
DROP TABLE IF EXISTS `resource_corpus_tool`;
CREATE TABLE `resource_corpus_tool` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(200) NOT NULL COMMENT '工具名称',
    `type` VARCHAR(50) COMMENT '工具类型：segmentation/pos_tagging/ner/sentiment/topic',
    `description` TEXT COMMENT '工具描述',
    `version` VARCHAR(50) COMMENT '版本',
    `programming_language` VARCHAR(100) COMMENT '编程语言',
    `repository_url` VARCHAR(500) COMMENT '代码库地址',
    `api_endpoint` VARCHAR(500) COMMENT 'API接口地址',
    `parameters_schema` JSON COMMENT '参数模式',
    `is_active` TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    `created_by` INT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_corpus_tool_name` (`name`),
    INDEX `idx_resource_corpus_tool_type` (`type`),
    INDEX `idx_resource_corpus_tool_is_active` (`is_active`),
    INDEX `idx_resource_corpus_tool_created_by` (`created_by`),
    INDEX `idx_resource_corpus_tool_created_at` (`created_at`),
    INDEX `idx_resource_corpus_tool_is_deleted` (`is_deleted`),
    
    UNIQUE INDEX `uk_resource_corpus_tool_name_version` (`name`, `version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料分析工具表';

-- 语料处理任务表
DROP TABLE IF EXISTS `resource_corpus_task`;
CREATE TABLE `resource_corpus_task` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `task_uuid` VARCHAR(36) UNIQUE,
    `corpus_id` INT NOT NULL,
    `tool_id` INT COMMENT '分析工具ID',
    `processing_type` VARCHAR(50) NOT NULL COMMENT '处理类型',
    `parameters` JSON COMMENT '处理参数',
    `status` VARCHAR(20) DEFAULT 'pending' COMMENT '状态：pending/processing/completed/failed',
    `progress_percentage` INT DEFAULT 0 COMMENT '进度百分比',
    `submitted_at` DATETIME,
    `started_at` DATETIME,
    `completed_at` DATETIME,
    `execution_time_ms` INT COMMENT '执行时间（毫秒）',
    `error_message` TEXT COMMENT '错误信息',
    `result_summary` TEXT COMMENT '结果摘要',
    `created_by` INT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    UNIQUE INDEX `uk_resource_corpus_task_uuid` (`task_uuid`),
    INDEX `idx_resource_corpus_task_corpus` (`corpus_id`),
    INDEX `idx_resource_corpus_task_tool` (`tool_id`),
    INDEX `idx_resource_corpus_task_type` (`processing_type`),
    INDEX `idx_resource_corpus_task_status` (`status`),
    INDEX `idx_resource_corpus_task_submitted_at` (`submitted_at`),
    INDEX `idx_resource_corpus_task_created_by` (`created_by`),
    INDEX `idx_resource_corpus_task_created_at` (`created_at`),
    INDEX `idx_resource_corpus_task_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_corpus_task_corpus_status` (`corpus_id`, `status`),
    INDEX `idx_resource_corpus_task_date_range` (`submitted_at`, `completed_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='语料处理任务表';

-- 方法表
DROP TABLE IF EXISTS `resource_method`;
CREATE TABLE `resource_method` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(300) NOT NULL,
    `english_name` VARCHAR(500),
    `field_id` INT,
    `subject_id` INT COMMENT '关联学科分类',
    `type` VARCHAR(100) COMMENT '方法类型：algorithm/statistical/experimental/computational',
    `description` TEXT,
    `principle` LONGTEXT,
    `advantages` TEXT,
    `limitations` TEXT,
    `application_scenarios` TEXT,
    `references` TEXT,
    `created_by` INT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_method_name` (`name`),
    INDEX `idx_resource_method_field_id` (`field_id`),
    INDEX `idx_resource_method_subject_id` (`subject_id`),
    INDEX `idx_resource_method_type` (`type`),
    INDEX `idx_resource_method_created_by` (`created_by`),
    INDEX `idx_resource_method_created_at` (`created_at`),
    INDEX `idx_resource_method_is_deleted` (`is_deleted`),
    
    FULLTEXT INDEX `ft_resource_method_description` (`name`, `description`, `application_scenarios`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='方法表';

-- 方法资源表
DROP TABLE IF EXISTS `resource_method_resource`;
CREATE TABLE `resource_method_resource` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `method_id` INT NOT NULL,
    `type` VARCHAR(50) NOT NULL COMMENT '资源类型：image/video/document/code/slide',
    `title` VARCHAR(300),
    `description` TEXT,
    `file_path` VARCHAR(500),
    `file_url` VARCHAR(500),
    `file_format` VARCHAR(50),
    `file_size` BIGINT,
    `version` VARCHAR(50),
    `download_count` INT DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_method_resource_method` (`method_id`),
    INDEX `idx_resource_method_resource_type` (`type`),
    INDEX `idx_resource_method_resource_version` (`version`),
    INDEX `idx_resource_method_resource_download_count` (`download_count`),
    INDEX `idx_resource_method_resource_created_at` (`created_at`),
    INDEX `idx_resource_method_resource_is_deleted` (`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='方法资源表';

-- 数据集表
DROP TABLE IF EXISTS `resource_dataset`;
CREATE TABLE `resource_dataset` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(300) NOT NULL,
    `english_name` VARCHAR(500),
    `description` TEXT,
    `field_id` INT,
    `subject_id` INT COMMENT '关联学科分类',
    `type` VARCHAR(100) COMMENT '数据类型：structured/unstructured/time_series/spatial',
    `format` VARCHAR(100) COMMENT '数据格式：CSV/JSON/XML/HDF5等',
    `size` BIGINT COMMENT '数据大小（字节）',
    `record_count` BIGINT COMMENT '记录条数',
    `source` VARCHAR(500) COMMENT '数据来源',
    `access_info` TEXT COMMENT '访问信息',
    `license` VARCHAR(200) COMMENT '使用许可',
    `download_count` INT DEFAULT 0,
    `citation_count` INT DEFAULT 0,
    `created_by` INT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_dataset_name` (`name`),
    INDEX `idx_resource_dataset_field_id` (`field_id`),
    INDEX `idx_resource_dataset_subject_id` (`subject_id`),
    INDEX `idx_resource_dataset_type` (`type`),
    INDEX `idx_resource_dataset_format` (`format`),
    INDEX `idx_resource_dataset_license` (`license`),
    INDEX `idx_resource_dataset_download_count` (`download_count`),
    INDEX `idx_resource_dataset_citation_count` (`citation_count`),
    INDEX `idx_resource_dataset_created_by` (`created_by`),
    INDEX `idx_resource_dataset_created_at` (`created_at`),
    INDEX `idx_resource_dataset_is_deleted` (`is_deleted`),
    
    FULLTEXT INDEX `ft_resource_dataset_description` (`name`, `description`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集表';

-- 代码库表
DROP TABLE IF EXISTS `resource_repository`;
CREATE TABLE `resource_repository` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(300) NOT NULL,
    `description` TEXT,
    `method_id` INT COMMENT '关联方法',
    `subject_id` INT COMMENT '关联学科分类',
    `programming_language` VARCHAR(100),
    `version` VARCHAR(50),
    `url` VARCHAR(500),
    `documentation_url` VARCHAR(500),
    `license` VARCHAR(200),
    `star_count` INT DEFAULT 0,
    `fork_count` INT DEFAULT 0,
    `download_count` INT DEFAULT 0,
    `citation_count` INT DEFAULT 0,
    `created_by` INT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_repository_name` (`name`),
    INDEX `idx_resource_repository_method_id` (`method_id`),
    INDEX `idx_resource_repository_subject_id` (`subject_id`),
    INDEX `idx_resource_repository_programming_language` (`programming_language`),
    INDEX `idx_resource_repository_version` (`version`),
    INDEX `idx_resource_repository_license` (`license`),
    INDEX `idx_resource_repository_star_count` (`star_count`),
    INDEX `idx_resource_repository_download_count` (`download_count`),
    INDEX `idx_resource_repository_citation_count` (`citation_count`),
    INDEX `idx_resource_repository_created_by` (`created_by`),
    INDEX `idx_resource_repository_created_at` (`created_at`),
    INDEX `idx_resource_repository_is_deleted` (`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='代码库表';

-- 成员表
DROP TABLE IF EXISTS `resource_member`;
CREATE TABLE `resource_member` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT UNIQUE NOT NULL,
    `position` VARCHAR(100) COMMENT '职位/职称',
    `position_level` VARCHAR(50) COMMENT '职称级别：教授/副教授等',
    `research_interests` TEXT,
    `education_background` TEXT,
    `work_experience` TEXT,
    `biography` LONGTEXT,
    `avatar_url` VARCHAR(500),
    `personal_website` VARCHAR(500),
    `orcid` VARCHAR(20),
    `google_scholar` VARCHAR(500),
    `researchgate` VARCHAR(500),
    `join_date` DATE,
    `leave_date` DATE,
    `status` VARCHAR(20) DEFAULT 'active' COMMENT '状态：active/inactive/alumni/visiting',
    `display_order` INT DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_member_user_id` (`user_id`),
    INDEX `idx_resource_member_position` (`position`),
    INDEX `idx_resource_member_status` (`status`),
    INDEX `idx_resource_member_join_date` (`join_date`),
    INDEX `idx_resource_member_display_order` (`display_order`),
    INDEX `idx_resource_member_created_at` (`created_at`),
    INDEX `idx_resource_member_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_member_status_join_date` (`status`, `join_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='成员表';

-- 成员学科关联表
DROP TABLE IF EXISTS `resource_member_subject`;
CREATE TABLE `resource_member_subject` (
    `member_id` INT NOT NULL,
    `subject_id` INT NOT NULL,
    `is_primary` TINYINT(1) DEFAULT 0 COMMENT '是否主要研究方向',
    `expertise_level` VARCHAR(20) COMMENT '专长级别：expert/proficient/familiar',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`member_id`, `subject_id`),
    
    INDEX `idx_resource_member_subject_member` (`member_id`),
    INDEX `idx_resource_member_subject_subject` (`subject_id`),
    INDEX `idx_resource_member_subject_is_primary` (`is_primary`),
    INDEX `idx_resource_member_subject_expertise_level` (`expertise_level`),
    INDEX `idx_resource_member_subject_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='成员学科关联表';

-- 项目表
DROP TABLE IF EXISTS `resource_project`;
CREATE TABLE `resource_project` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `code` VARCHAR(100) UNIQUE COMMENT '项目编号',
    `name` VARCHAR(500) NOT NULL,
    `english_name` VARCHAR(500),
    `description` TEXT,
    `type` VARCHAR(100) COMMENT '项目类型：national/provincial/cooperation/enterprise',
    `funding_source` VARCHAR(300) COMMENT '资金来源',
    `budget` DECIMAL(14,2) COMMENT '预算（万元）',
    `start_date` DATE,
    `end_date` DATE,
    `actual_end_date` DATE COMMENT '实际结束日期',
    `status` VARCHAR(20) COMMENT '状态：planning/ongoing/completed/suspended',
    `subject_id` INT COMMENT '主要学科分类',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    UNIQUE INDEX `uk_resource_project_code` (`code`),
    INDEX `idx_resource_project_name` (`name`(100)),
    INDEX `idx_resource_project_type` (`type`),
    INDEX `idx_resource_project_status` (`status`),
    INDEX `idx_resource_project_subject_id` (`subject_id`),
    INDEX `idx_resource_project_start_date` (`start_date`),
    INDEX `idx_resource_project_end_date` (`end_date`),
    INDEX `idx_resource_project_created_at` (`created_at`),
    INDEX `idx_resource_project_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_project_dates_status` (`start_date`, `end_date`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='项目表';

-- 项目成员关联表
DROP TABLE IF EXISTS `resource_project_member`;
CREATE TABLE `resource_project_member` (
    `project_id` INT NOT NULL,
    `member_id` INT NOT NULL,
    `role` VARCHAR(50) COMMENT '角色：PI/co-PI/researcher/student/administrator',
    `responsibility` TEXT COMMENT '职责说明',
    `contribution` TEXT COMMENT '贡献说明',
    `join_date` DATE,
    `leave_date` DATE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`project_id`, `member_id`),
    
    INDEX `idx_resource_project_member_project` (`project_id`),
    INDEX `idx_resource_project_member_member` (`member_id`),
    INDEX `idx_resource_project_member_role` (`role`),
    INDEX `idx_resource_project_member_join_date` (`join_date`),
    INDEX `idx_resource_project_member_created_at` (`created_at`),
    
    INDEX `idx_resource_project_member_project_role` (`project_id`, `role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='项目成员关联表';

-- 项目学科关联表
DROP TABLE IF EXISTS `resource_project_subject`;
CREATE TABLE `resource_project_subject` (
    `project_id` INT NOT NULL,
    `subject_id` INT NOT NULL,
    `is_primary` TINYINT(1) DEFAULT 0 COMMENT '是否主要学科',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`project_id`, `subject_id`),
    
    INDEX `idx_resource_project_subject_project` (`project_id`),
    INDEX `idx_resource_project_subject_subject` (`subject_id`),
    INDEX `idx_resource_project_subject_is_primary` (`is_primary`),
    INDEX `idx_resource_project_subject_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='项目学科关联表';

-- 成果表
DROP TABLE IF EXISTS `resource_achievement`;
CREATE TABLE `resource_achievement` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `type` VARCHAR(50) NOT NULL COMMENT '成果类型：paper/patent/award/book/software/dataset',
    `title` VARCHAR(500) NOT NULL,
    `english_title` VARCHAR(500),
    `description` TEXT,
    `achievement_date` DATE,
    `issuing_authority` VARCHAR(300) COMMENT '颁发机构',
    `certificate_number` VARCHAR(200) COMMENT '证书编号',
    `attachment_url` VARCHAR(500) COMMENT '证书附件',
    `external_url` VARCHAR(500) COMMENT '外部链接',
    `subject_id` INT COMMENT '主要学科分类',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_achievement_type` (`type`),
    INDEX `idx_resource_achievement_title` (`title`(100)),
    INDEX `idx_resource_achievement_date` (`achievement_date`),
    INDEX `idx_resource_achievement_authority` (`issuing_authority`),
    INDEX `idx_resource_achievement_subject_id` (`subject_id`),
    INDEX `idx_resource_achievement_created_at` (`created_at`),
    INDEX `idx_resource_achievement_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_achievement_type_date` (`type`, `achievement_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='成果表';

-- 成果参与人表
DROP TABLE IF EXISTS `resource_achievement_participant`;
CREATE TABLE `resource_achievement_participant` (
    `achievement_id` INT NOT NULL,
    `member_id` INT NOT NULL,
    `role` VARCHAR(50) COMMENT '角色：author/inventor/contributor/advisor',
    `contribution_order` INT COMMENT '贡献顺序',
    `contribution_description` TEXT COMMENT '贡献描述',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`achievement_id`, `member_id`),
    
    INDEX `idx_resource_achievement_participant_achievement` (`achievement_id`),
    INDEX `idx_resource_achievement_participant_member` (`member_id`),
    INDEX `idx_resource_achievement_participant_role` (`role`),
    INDEX `idx_resource_achievement_participant_contribution_order` (`contribution_order`),
    INDEX `idx_resource_achievement_participant_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='成果参与人表';

-- 成果学科关联表
DROP TABLE IF EXISTS `resource_achievement_subject`;
CREATE TABLE `resource_achievement_subject` (
    `achievement_id` INT NOT NULL,
    `subject_id` INT NOT NULL,
    `is_primary` TINYINT(1) DEFAULT 0 COMMENT '是否主要学科',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`achievement_id`, `subject_id`),
    
    INDEX `idx_resource_achievement_subject_achievement` (`achievement_id`),
    INDEX `idx_resource_achievement_subject_subject` (`subject_id`),
    INDEX `idx_resource_achievement_subject_is_primary` (`is_primary`),
    INDEX `idx_resource_achievement_subject_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='成果学科关联表';

-- 通知表
DROP TABLE IF EXISTS `resource_announcement`;
CREATE TABLE `resource_announcement` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(300) NOT NULL,
    `content` LONGTEXT,
    `type` VARCHAR(50) COMMENT '通知类型：meeting/event/deadline/news/achievement',
    `publish_date` DATETIME,
    `expire_date` DATETIME,
    `priority` VARCHAR(20) DEFAULT 'normal' COMMENT '优先级：high/normal/low',
    `attachment_url` VARCHAR(500),
    `created_by` INT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_announcement_type` (`type`),
    INDEX `idx_resource_announcement_publish_date` (`publish_date`),
    INDEX `idx_resource_announcement_expire_date` (`expire_date`),
    INDEX `idx_resource_announcement_priority` (`priority`),
    INDEX `idx_resource_announcement_created_by` (`created_by`),
    INDEX `idx_resource_announcement_created_at` (`created_at`),
    INDEX `idx_resource_announcement_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_announcement_active` (`publish_date`, `expire_date`, `is_deleted`),
    
    FULLTEXT INDEX `ft_resource_announcement_title_content` (`title`, `content`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='通知表';

-- 交流表
DROP TABLE IF EXISTS `resource_exchange`;
CREATE TABLE `resource_exchange` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(300) NOT NULL,
    `english_title` VARCHAR(300),
    `type` VARCHAR(50) COMMENT '交流类型：conference/visit/seminar/workshop',
    `location` VARCHAR(500),
    `start_date` DATETIME,
    `end_date` DATETIME,
    `description` TEXT,
    `participants` TEXT COMMENT '参与人员',
    `report_url` VARCHAR(500) COMMENT '报告文件',
    `photos_url` TEXT COMMENT '活动照片',
    `subject_id` INT COMMENT '关联学科分类',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_exchange_type` (`type`),
    INDEX `idx_resource_exchange_start_date` (`start_date`),
    INDEX `idx_resource_exchange_end_date` (`end_date`),
    INDEX `idx_resource_exchange_location` (`location`(100)),
    INDEX `idx_resource_exchange_subject_id` (`subject_id`),
    INDEX `idx_resource_exchange_created_at` (`created_at`),
    INDEX `idx_resource_exchange_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_exchange_date_range` (`start_date`, `end_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='交流表';

-- 交流参与人表
DROP TABLE IF EXISTS `resource_exchange_participant`;
CREATE TABLE `resource_exchange_participant` (
    `exchange_id` INT NOT NULL,
    `member_id` INT NOT NULL,
    `role` VARCHAR(50) COMMENT '角色：speaker/participant/organizer',
    `contribution` TEXT COMMENT '贡献说明',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`exchange_id`, `member_id`),
    
    INDEX `idx_resource_exchange_participant_exchange` (`exchange_id`),
    INDEX `idx_resource_exchange_participant_member` (`member_id`),
    INDEX `idx_resource_exchange_participant_role` (`role`),
    INDEX `idx_resource_exchange_participant_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='交流参与人表';

-- 课题表
DROP TABLE IF EXISTS `resource_topic`;
CREATE TABLE `resource_topic` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `code` VARCHAR(100) UNIQUE COMMENT '课题编号',
    `title` VARCHAR(500) NOT NULL,
    `english_title` VARCHAR(500),
    `description` TEXT,
    `research_background` LONGTEXT COMMENT '研究背景',
    `research_objectives` LONGTEXT COMMENT '研究目标',
    `research_content` LONGTEXT COMMENT '研究内容',
    `expected_outcomes` LONGTEXT COMMENT '预期成果',
    `subject_id` INT COMMENT '主要学科分类',
    `project_id` INT COMMENT '关联项目',
    `lead_member_id` INT COMMENT '课题负责人',
    `start_date` DATE,
    `end_date` DATE,
    `actual_end_date` DATE COMMENT '实际结束日期',
    `status` VARCHAR(20) COMMENT '状态：planning/active/completed/paused/terminated',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    UNIQUE INDEX `uk_resource_topic_code` (`code`),
    INDEX `idx_resource_topic_title` (`title`(100)),
    INDEX `idx_resource_topic_subject_id` (`subject_id`),
    INDEX `idx_resource_topic_project_id` (`project_id`),
    INDEX `idx_resource_topic_lead_member_id` (`lead_member_id`),
    INDEX `idx_resource_topic_status` (`status`),
    INDEX `idx_resource_topic_start_date` (`start_date`),
    INDEX `idx_resource_topic_end_date` (`end_date`),
    INDEX `idx_resource_topic_created_at` (`created_at`),
    INDEX `idx_resource_topic_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_topic_status_dates` (`status`, `start_date`, `end_date`),
    
    FULLTEXT INDEX `ft_resource_topic_description` (`title`, `description`, `research_objectives`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='课题表';

-- 课题成员表
DROP TABLE IF EXISTS `resource_topic_member`;
CREATE TABLE `resource_topic_member` (
    `topic_id` INT NOT NULL,
    `member_id` INT NOT NULL,
    `role` VARCHAR(50) COMMENT '角色：leader/researcher/assistant/student',
    `responsibility` TEXT COMMENT '具体职责',
    `contribution` TEXT COMMENT '贡献说明',
    `join_date` DATE,
    `leave_date` DATE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`topic_id`, `member_id`),
    
    INDEX `idx_resource_topic_member_topic` (`topic_id`),
    INDEX `idx_resource_topic_member_member` (`member_id`),
    INDEX `idx_resource_topic_member_role` (`role`),
    INDEX `idx_resource_topic_member_join_date` (`join_date`),
    INDEX `idx_resource_topic_member_created_at` (`created_at`),
    
    INDEX `idx_resource_topic_member_topic_role` (`topic_id`, `role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='课题成员表';

-- 课题学科关联表
DROP TABLE IF EXISTS `resource_topic_subject`;
CREATE TABLE `resource_topic_subject` (
    `topic_id` INT NOT NULL,
    `subject_id` INT NOT NULL,
    `is_primary` TINYINT(1) DEFAULT 0 COMMENT '是否主要学科',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`topic_id`, `subject_id`),
    
    INDEX `idx_resource_topic_subject_topic` (`topic_id`),
    INDEX `idx_resource_topic_subject_subject` (`subject_id`),
    INDEX `idx_resource_topic_subject_is_primary` (`is_primary`),
    INDEX `idx_resource_topic_subject_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='课题学科关联表';

-- 里程碑表
DROP TABLE IF EXISTS `resource_milestone`;
CREATE TABLE `resource_milestone` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `topic_id` INT NOT NULL,
    `name` VARCHAR(300) NOT NULL,
    `description` TEXT,
    `planned_start_date` DATE,
    `planned_end_date` DATE,
    `actual_start_date` DATE,
    `actual_end_date` DATE,
    `status` VARCHAR(20) COMMENT '状态：not_started/in_progress/completed/delayed',
    `completion_percentage` INT DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_milestone_topic` (`topic_id`),
    INDEX `idx_resource_milestone_status` (`status`),
    INDEX `idx_resource_milestone_planned_start_date` (`planned_start_date`),
    INDEX `idx_resource_milestone_planned_end_date` (`planned_end_date`),
    INDEX `idx_resource_milestone_actual_start_date` (`actual_start_date`),
    INDEX `idx_resource_milestone_actual_end_date` (`actual_end_date`),
    INDEX `idx_resource_milestone_completion_percentage` (`completion_percentage`),
    INDEX `idx_resource_milestone_created_at` (`created_at`),
    INDEX `idx_resource_milestone_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_milestone_topic_status` (`topic_id`, `status`),
    INDEX `idx_resource_milestone_dates` (`planned_start_date`, `planned_end_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='里程碑表';

-- 成果表
DROP TABLE IF EXISTS `resource_deliverable`;
CREATE TABLE `resource_deliverable` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `topic_id` INT NOT NULL,
    `milestone_id` INT COMMENT '关联里程碑',
    `type` VARCHAR(50) COMMENT '成果类型：report/data/code/paper/patent/software',
    `title` VARCHAR(500),
    `description` TEXT,
    `file_path` VARCHAR(500),
    `file_url` VARCHAR(500),
    `submitted_by` INT COMMENT '提交人',
    `submitted_at` DATETIME,
    `approval_status` VARCHAR(20) DEFAULT 'pending' COMMENT '审核状态：pending/approved/rejected/revised',
    `reviewer_comments` TEXT COMMENT '审核意见',
    `reviewed_by` INT COMMENT '审核人',
    `reviewed_at` DATETIME COMMENT '审核时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_deliverable_topic` (`topic_id`),
    INDEX `idx_resource_deliverable_milestone` (`milestone_id`),
    INDEX `idx_resource_deliverable_type` (`type`),
    INDEX `idx_resource_deliverable_submitted_by` (`submitted_by`),
    INDEX `idx_resource_deliverable_submitted_at` (`submitted_at`),
    INDEX `idx_resource_deliverable_approval_status` (`approval_status`),
    INDEX `idx_resource_deliverable_created_at` (`created_at`),
    INDEX `idx_resource_deliverable_is_deleted` (`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='课题成果表';

-- 课题文献关联表
DROP TABLE IF EXISTS `resource_topic_publication`;
CREATE TABLE `resource_topic_publication` (
    `topic_id` INT NOT NULL,
    `publication_id` INT NOT NULL,
    `relevance_level` VARCHAR(20) COMMENT '关联程度：high/medium/low',
    `notes` TEXT COMMENT '关联说明',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`topic_id`, `publication_id`),
    
    INDEX `idx_resource_topic_publication_topic` (`topic_id`),
    INDEX `idx_resource_topic_publication_publication` (`publication_id`),
    INDEX `idx_resource_topic_publication_relevance_level` (`relevance_level`),
    INDEX `idx_resource_topic_publication_created_at` (`created_at`),
    
    INDEX `idx_resource_topic_publication_topic_relevance` (`topic_id`, `relevance_level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='课题文献关联表';

-- 程序表
DROP TABLE IF EXISTS `resource_program`;
CREATE TABLE `resource_program` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(300) NOT NULL,
    `description` TEXT,
    `type` VARCHAR(50) COMMENT '程序类型：web_service/desktop/script/notebook',
    `version` VARCHAR(50),
    `repository_id` INT COMMENT '关联代码库',
    `subject_id` INT COMMENT '关联学科分类',
    `entry_point` VARCHAR(500) COMMENT '程序入口',
    `execution_environment` TEXT COMMENT '运行环境要求',
    `parameters` JSON COMMENT '参数配置',
    `input_specification` TEXT COMMENT '输入说明',
    `output_specification` TEXT COMMENT '输出说明',
    `max_execution_time` INT COMMENT '最长执行时间（秒）',
    `max_memory_mb` INT COMMENT '最大内存（MB）',
    `max_disk_mb` INT COMMENT '最大磁盘空间（MB）',
    `concurrent_limit` INT DEFAULT 1 COMMENT '并发限制',
    `is_active` TINYINT(1) DEFAULT 1,
    `usage_count` INT DEFAULT 0,
    `avg_execution_time` INT DEFAULT 0 COMMENT '平均执行时间（毫秒）',
    `success_rate` DECIMAL(5,2) DEFAULT 100.00 COMMENT '成功率（%）',
    `created_by` INT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_program_name` (`name`),
    INDEX `idx_resource_program_type` (`type`),
    INDEX `idx_resource_program_version` (`version`),
    INDEX `idx_resource_program_repository_id` (`repository_id`),
    INDEX `idx_resource_program_subject_id` (`subject_id`),
    INDEX `idx_resource_program_is_active` (`is_active`),
    INDEX `idx_resource_program_usage_count` (`usage_count`),
    INDEX `idx_resource_program_created_by` (`created_by`),
    INDEX `idx_resource_program_created_at` (`created_at`),
    INDEX `idx_resource_program_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_program_active_usage` (`is_active`, `usage_count`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='程序表';

-- 任务表
DROP TABLE IF EXISTS `resource_task`;
CREATE TABLE `resource_task` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `uuid` VARCHAR(36) UNIQUE,
    `program_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `name` VARCHAR(300),
    `parameters` JSON,
    `input_files` JSON,
    `priority` INT DEFAULT 5 COMMENT '优先级：1-10，数字越小优先级越高',
    `status` VARCHAR(20) DEFAULT 'pending' COMMENT '状态：pending/queued/running/completed/failed/cancelled',
    `submitted_at` DATETIME,
    `started_at` DATETIME,
    `completed_at` DATETIME,
    `execution_time_ms` INT COMMENT '执行时间（毫秒）',
    `resource_usage` JSON COMMENT '资源使用情况',
    `error_message` TEXT,
    `error_stack` TEXT COMMENT '错误堆栈信息',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    UNIQUE INDEX `uk_resource_task_uuid` (`uuid`),
    INDEX `idx_resource_task_program` (`program_id`),
    INDEX `idx_resource_task_user` (`user_id`),
    INDEX `idx_resource_task_status` (`status`),
    INDEX `idx_resource_task_priority` (`priority`),
    INDEX `idx_resource_task_submitted_at` (`submitted_at`),
    INDEX `idx_resource_task_started_at` (`started_at`),
    INDEX `idx_resource_task_completed_at` (`completed_at`),
    INDEX `idx_resource_task_created_at` (`created_at`),
    INDEX `idx_resource_task_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_task_user_status` (`user_id`, `status`),
    INDEX `idx_resource_task_program_status` (`program_id`, `status`),
    INDEX `idx_resource_task_date_range` (`submitted_at`, `completed_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='任务表';

-- 任务结果表
DROP TABLE IF EXISTS `resource_task_result`;
CREATE TABLE `resource_task_result` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `task_id` INT NOT NULL,
    `type` VARCHAR(50) COMMENT '结果类型：file/chart/text/table/json',
    `key` VARCHAR(100) COMMENT '结果标识',
    `title` VARCHAR(500),
    `description` TEXT,
    `file_path` VARCHAR(500),
    `file_url` VARCHAR(500),
    `file_size` BIGINT,
    `preview_url` VARCHAR(500),
    `metadata` JSON,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_task_result_task` (`task_id`),
    INDEX `idx_resource_task_result_type` (`type`),
    INDEX `idx_resource_task_result_key` (`key`),
    INDEX `idx_resource_task_result_created_at` (`created_at`),
    INDEX `idx_resource_task_result_is_deleted` (`is_deleted`),
    
    INDEX `idx_resource_task_result_task_type` (`task_id`, `type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='任务结果表';

-- 内置数据集表
DROP TABLE IF EXISTS `resource_builtin_dataset`;
CREATE TABLE `resource_builtin_dataset` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `program_id` INT NOT NULL,
    `dataset_id` INT COMMENT '关联数据集表',
    `name` VARCHAR(300),
    `description` TEXT,
    `file_path` VARCHAR(500),
    `file_url` VARCHAR(500),
    `format` VARCHAR(50),
    `is_required` TINYINT(1) DEFAULT 0 COMMENT '是否必需',
    `version` VARCHAR(50),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted` TINYINT(1) DEFAULT 0,
    `deleted_at` TIMESTAMP NULL,
    
    INDEX `idx_resource_builtin_dataset_program` (`program_id`),
    INDEX `idx_resource_builtin_dataset_dataset` (`dataset_id`),
    INDEX `idx_resource_builtin_dataset_is_required` (`is_required`),
    INDEX `idx_resource_builtin_dataset_format` (`format`),
    INDEX `idx_resource_builtin_dataset_created_at` (`created_at`),
    INDEX `idx_resource_builtin_dataset_is_deleted` (`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='内置数据集表';

-- 程序学科关联表
DROP TABLE IF EXISTS `resource_program_subject`;
CREATE TABLE `resource_program_subject` (
    `program_id` INT NOT NULL,
    `subject_id` INT NOT NULL,
    `is_primary` TINYINT(1) DEFAULT 0 COMMENT '是否主要学科',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`program_id`, `subject_id`),
    
    INDEX `idx_resource_program_subject_program` (`program_id`),
    INDEX `idx_resource_program_subject_subject` (`subject_id`),
    INDEX `idx_resource_program_subject_is_primary` (`is_primary`),
    INDEX `idx_resource_program_subject_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='程序学科关联表';