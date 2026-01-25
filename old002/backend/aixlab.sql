-- 用户表 - 存储用户基本信息
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '真实姓名',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT '邮箱',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    display_name VARCHAR(100) COMMENT '显示名称',
    avatar_url VARCHAR(500) COMMENT '头像URL',
    role ENUM('admin', 'researcher', 'student', 'guest') DEFAULT 'researcher' COMMENT '用户角色',
    status ENUM('active', 'inactive', 'suspended', 'pending') DEFAULT 'active' COMMENT '账户状态',
    storage_quota_mb INT DEFAULT 1024 COMMENT '存储配额(MB)',
    used_storage_mb INT DEFAULT 0 COMMENT '已用存储(MB)',
    api_key VARCHAR(64) UNIQUE COMMENT 'API密钥',
    last_login_time DATETIME COMMENT '最后登录时间',
    preferences JSON COMMENT '用户偏好设置(JSON格式)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 用户会话表 - 用于管理用户登录会话
CREATE TABLE IF NOT EXISTS user_sessions (
    session_id VARCHAR(128) PRIMARY KEY COMMENT '会话ID',
    user_id INT NOT NULL COMMENT '用户ID',
    refresh_token VARCHAR(255) NOT NULL COMMENT '刷新令牌',
    user_agent TEXT COMMENT '用户代理',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    expires_at DATETIME NOT NULL COMMENT '过期时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户会话表';

-- 用户操作日志表 - 记录用户重要操作
CREATE TABLE IF NOT EXISTS user_activity_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '日志ID',
    user_id INT NOT NULL COMMENT '用户ID',
    action_type VARCHAR(50) NOT NULL COMMENT '操作类型',
    resource_type VARCHAR(50) COMMENT '资源类型',
    resource_id VARCHAR(100) COMMENT '资源ID',
    description TEXT COMMENT '操作描述',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    metadata JSON COMMENT '额外元数据(JSON格式)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_action (user_id, action_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户操作日志表';


-- 数据集分类表 - 用于组织内置数据集
CREATE TABLE IF NOT EXISTS dataset_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '分类ID',
    category_name VARCHAR(100) NOT NULL COMMENT '分类名称',
    category_slug VARCHAR(100) UNIQUE NOT NULL COMMENT '分类标识符',
    description TEXT COMMENT '分类描述',
    icon_class VARCHAR(50) COMMENT '图标类名',
    display_order INT DEFAULT 0 COMMENT '显示顺序',
    parent_category_id INT COMMENT '父分类ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (parent_category_id) REFERENCES dataset_categories(category_id) ON DELETE SET NULL,
    INDEX idx_slug (category_slug),
    INDEX idx_parent (parent_category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='数据集分类表';

-- 内置数据集表 - 存储内置数据集元数据
CREATE TABLE IF NOT EXISTS builtin_datasets (
    dataset_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '数据集ID',
    dataset_name VARCHAR(200) NOT NULL COMMENT '数据集名称',
    dataset_slug VARCHAR(200) UNIQUE NOT NULL COMMENT '数据集标识符',
    description TEXT COMMENT '数据集描述',
    category_id INT NOT NULL COMMENT '分类ID',
    source_name VARCHAR(200) COMMENT '数据来源',
    source_url VARCHAR(500) COMMENT '来源URL',
    license_type VARCHAR(100) COMMENT '许可证类型',
    data_type ENUM('tabular', 'timeseries', 'spatial', 'text', 'image', 'other') DEFAULT 'tabular' COMMENT '数据类型',
    
    -- 数据集统计信息
    row_count INT DEFAULT 0 COMMENT '行数',
    column_count INT DEFAULT 0 COMMENT '列数',
    file_size_mb DECIMAL(10,2) DEFAULT 0.00 COMMENT '文件大小(MB) -- 补充默认值',
    data_format VARCHAR(50) COMMENT '数据格式(csv, json, parquet等)',
    
    -- 文件路径信息
    file_path VARCHAR(500) NOT NULL COMMENT '文件存储路径',
    preview_file_path VARCHAR(500) COMMENT '预览数据文件路径',
    
    -- 字段信息(JSON格式存储字段元数据)
    column_schema JSON COMMENT '列结构定义',
    
    -- 使用统计
    view_count INT DEFAULT 0 COMMENT '查看次数',
    download_count INT DEFAULT 0 COMMENT '下载次数',
    
    -- 标签系统
    tags JSON COMMENT '标签(JSON数组)',
    
    -- 版本信息
    version VARCHAR(20) DEFAULT '1.0' COMMENT '版本号',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    is_featured BOOLEAN DEFAULT FALSE COMMENT '是否推荐',
    
    created_by INT COMMENT '创建者用户ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (category_id) REFERENCES dataset_categories(category_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE SET NULL,
    
    INDEX idx_slug (dataset_slug),
    INDEX idx_category (category_id),
    INDEX idx_created_at (created_at),
    INDEX idx_is_featured (is_featured),
    INDEX idx_is_active (is_active),
    -- 修正: 移除全文索引中的JSON类型字段tags, 仅保留字符类型的字段
    FULLTEXT INDEX ft_search (dataset_name, description) COMMENT '全文搜索索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='内置数据集表';

-- 数据集示例代码表 - 存储针对数据集的示例分析代码
CREATE TABLE IF NOT EXISTS dataset_examples (
    example_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '示例ID',
    dataset_id INT NOT NULL COMMENT '数据集ID',
    language ENUM('python', 'r', 'both') NOT NULL COMMENT '编程语言',
    title VARCHAR(200) NOT NULL COMMENT '示例标题',
    description TEXT COMMENT '示例描述',
    
    -- 代码内容
    code_content LONGTEXT NOT NULL COMMENT '代码内容',
    expected_output TEXT COMMENT '预期输出',
    
    -- 分析类型标签
    analysis_type VARCHAR(100) COMMENT '分析类型',
    difficulty ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner' COMMENT '难度级别',
    
    view_count INT DEFAULT 0 COMMENT '查看次数',
    run_count INT DEFAULT 0 COMMENT '运行次数',
    
    created_by INT COMMENT '创建者用户ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (dataset_id) REFERENCES builtin_datasets(dataset_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE SET NULL,
    
    INDEX idx_dataset (dataset_id),
    INDEX idx_language (language),
    INDEX idx_analysis_type (analysis_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='数据集示例代码表';

-- 数据集使用统计表 - 记录数据集的使用情况
CREATE TABLE IF NOT EXISTS dataset_usage_stats (
    stat_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '统计ID',
    dataset_id INT NOT NULL COMMENT '数据集ID',
    user_id INT COMMENT '用户ID',
    
    action_type ENUM('view', 'download', 'preview', 'analyze') NOT NULL COMMENT '操作类型',
    analysis_language ENUM('python', 'r', 'none') DEFAULT 'none' COMMENT '分析语言',
    
    session_id VARCHAR(128) COMMENT '会话ID',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    
    metadata JSON COMMENT '额外元数据',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    FOREIGN KEY (dataset_id) REFERENCES builtin_datasets(dataset_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    
    INDEX idx_dataset_action (dataset_id, action_type),
    INDEX idx_created_at (created_at),
    INDEX idx_user_dataset (user_id, dataset_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='数据集使用统计表';

-- 插入初始管理员用户(密码: Admin123!, 实际生产环境必须使用BCrypt哈希)
-- 生成真实哈希示例: PHP的password_hash("Admin123!", PASSWORD_BCRYPT) 或 Python的bcrypt.hashpw
INSERT INTO users (username, email, password_hash, display_name, role, storage_quota_mb) 
VALUES 
('admin', 'admin@aixlab.org', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', '系统管理员', 'admin', 10240), -- 示例哈希值(密码: Admin123!)
('demo_user', 'demo@aixlab.org', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', '演示用户', 'researcher', 2048);

-- 插入数据集分类
INSERT INTO dataset_categories (category_name, category_slug, description, icon_class, display_order) 
VALUES 
('统计学', 'statistics', '统计学相关数据集, 包括各种统计分布、检验数据等', 'fas fa-chart-bar', 1),
('机器学习', 'machine-learning', '机器学习算法训练和测试数据集', 'fas fa-robot', 2),
('金融经济', 'finance-economics', '股票、汇率、宏观经济指标等金融经济数据', 'fas fa-chart-line', 3),
('社交网络', 'social-network', '社交网络关系、用户行为数据', 'fas fa-users', 4),
('医疗健康', 'healthcare', '医疗记录、生物特征、疾病统计等数据', 'fas fa-heartbeat', 5),
('自然科学', 'natural-science', '物理、化学、生物等自然科学实验数据', 'fas fa-flask', 6),
('时间序列', 'time-series', '时间序列分析相关数据集', 'fas fa-clock', 7),
('文本数据', 'text-data', '文本分类、情感分析等自然语言处理数据', 'fas fa-file-alt', 8),
('图像数据', 'image-data', '图像分类、目标检测等计算机视觉数据', 'fas fa-image', 9),
('地理空间', 'geospatial', '地图、GPS轨迹、地理信息数据', 'fas fa-globe', 10);

-- 插入内置数据集示例(修正: 用子查询获取分类ID, 指定创建者为admin用户)
INSERT INTO builtin_datasets (
    dataset_name, 
    dataset_slug, 
    description, 
    category_id,
    source_name,
    data_type,
    row_count,
    column_count,
    file_size_mb, -- 补充默认值, 避免空值
    file_path,
    column_schema,
    tags,
    created_by -- 指定创建者为admin(user_id=1)
) 
VALUES 
(
    '鸢尾花数据集', 
    'iris', 
    '经典的鸢尾花数据集, 包含三种鸢尾花的萼片和花瓣的长度和宽度测量数据。常用于分类算法演示。', 
    (SELECT category_id FROM dataset_categories WHERE category_slug = 'machine-learning'), -- 替换硬编码ID
    'UCI Machine Learning Repository',
    'tabular',
    150,
    5,
    0.01, -- 补充文件大小
    '/data/builtin/iris.csv',
    '[{"name":"sepal_length","type":"float","description":"萼片长度(cm)"},{"name":"sepal_width","type":"float","description":"萼片宽度(cm)"},{"name":"petal_length","type":"float","description":"花瓣长度(cm)"},{"name":"petal_width","type":"float","description":"花瓣宽度(cm)"},{"name":"species","type":"string","description":"鸢尾花种类"}]',
    '["分类","机器学习","经典","小数据集"]',
    1 -- admin用户ID
),
(
    '波士顿房价数据集', 
    'boston-housing', 
    '波士顿地区房价数据集, 包含房屋的各种特征和对应的房价。常用于回归分析。', 
    (SELECT category_id FROM dataset_categories WHERE category_slug = 'machine-learning'),
    'UCI Machine Learning Repository',
    'tabular',
    506,
    14,
    0.02,
    '/data/builtin/boston_housing.csv',
    '[{"name":"crim","type":"float","description":"城镇人均犯罪率"},{"name":"zn","type":"float","description":"占地面积超过25,000平方英尺的住宅用地比例"},{"name":"indus","type":"float","description":"非零售业务用地比例"},{"name":"chas","type":"int","description":"查尔斯河虚拟变量(1=河边, 0=其他)"},{"name":"nox","type":"float","description":"氮氧化物浓度"},{"name":"rm","type":"float","description":"每户平均房间数"},{"name":"age","type":"float","description":"1940年以前建造的自住房比例"},{"name":"dis","type":"float","description":"到波士顿五个就业中心的加权距离"},{"name":"rad","type":"int","description":"放射状公路可达性指数"},{"name":"tax","type":"float","description":"每万美元的全额财产税税率"},{"name":"ptratio","type":"float","description":"城镇师生比例"},{"name":"b","type":"float","description":"黑人比例"},{"name":"lstat","type":"float","description":"低收入人口比例"},{"name":"medv","type":"float","description":"自住房中位数价格(千美元)"}]',
    '["回归","房价预测","经典"]',
    1
),
(
    '泰坦尼克号乘客数据', 
    'titanic', 
    '泰坦尼克号乘客信息及生存状态数据集, 常用于生存分析和分类预测。', 
    (SELECT category_id FROM dataset_categories WHERE category_slug = 'statistics'),
    'Kaggle',
    'tabular',
    891,
    12,
    0.03,
    '/data/builtin/titanic.csv',
    '[{"name":"passenger_id","type":"int","description":"乘客ID"},{"name":"survived","type":"int","description":"是否幸存(0=否, 1=是)"},{"name":"pclass","type":"int","description":"船舱等级(1=头等舱, 2=二等舱, 3=三等舱)"},{"name":"name","type":"string","description":"乘客姓名"},{"name":"sex","type":"string","description":"性别"},{"name":"age","type":"float","description":"年龄"},{"name":"sibsp","type":"int","description":"同船兄弟姐妹/配偶数量"},{"name":"parch","type":"int","description":"同船父母/子女数量"},{"name":"ticket","type":"string","description":"船票编号"},{"name":"fare","type":"float","description":"船票价格"},{"name":"cabin","type":"string","description":"船舱号"},{"name":"embarked","type":"string","description":"登船港口"}]',
    '["生存分析","分类","数据挖掘"]',
    1
),
(
    '每日温度时间序列', 
    'daily-temperatures', 
    '某城市多年每日平均温度时间序列数据, 适合时间序列分析和预测。', 
    (SELECT category_id FROM dataset_categories WHERE category_slug = 'time-series'),
    'NOAA',
    'timeseries',
    3650,
    3,
    0.05,
    '/data/builtin/daily_temperatures.csv',
    '[{"name":"date","type":"date","description":"日期"},{"name":"temperature","type":"float","description":"平均温度(摄氏度)"},{"name":"precipitation","type":"float","description":"降水量(mm)"}]',
    '["时间序列","预测","天气数据"]',
    1
);

-- 插入数据集示例代码(修正: 转义特殊字符, 指定创建者)
INSERT INTO dataset_examples (
    dataset_id, 
    language, 
    title, 
    description, 
    code_content,
    analysis_type,
    difficulty,
    created_by -- 指定创建者为admin
) 
VALUES 
(
    (SELECT dataset_id FROM builtin_datasets WHERE dataset_slug = 'iris'), 
    'python', 
    '鸢尾花数据集分类分析', 
    '使用逻辑回归对鸢尾花数据集进行分类, 并评估模型性能。', 
    'import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
df = pd.read_csv("/data/builtin/iris.csv")

# 数据探索
print("数据形状:", df.shape)
print("\\n前5行数据:")
print(df.head())
print("\\n数据统计摘要:")
print(df.describe())

# 特征和目标变量
X = df.drop("species", axis=1)
y = df["species"]

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 创建并训练模型
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估模型
accuracy = accuracy_score(y_test, y_pred)
print(f"\\n模型准确率: {accuracy:.4f}")
print("\\n分类报告:")
print(classification_report(y_test, y_pred))

# 可视化
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="petal_length", y="petal_width", 
                hue="species", style="species", s=100)
plt.title("鸢尾花数据集 - 花瓣长度 vs 花瓣宽度")
plt.xlabel("花瓣长度 (cm)")
plt.ylabel("花瓣宽度 (cm)")
plt.legend(title="种类")
plt.grid(True, alpha=0.3)
plt.show()',
    '分类分析',
    'beginner',
    1
),
(
    (SELECT dataset_id FROM builtin_datasets WHERE dataset_slug = 'iris'), 
    'r', 
    '鸢尾花数据探索性分析', 
    '使用R语言对鸢尾花数据集进行探索性数据分析(EDA)。', 
    'library(ggplot2)
library(dplyr)
library(corrplot)

# 加载数据
data(iris)

# 基本数据信息
cat("数据维度:", dim(iris), "\\\\n")
cat("变量名:", names(iris), "\\\\n")
cat("\\n数据摘要:\\n")
print(summary(iris))

# 相关性分析
cor_matrix <- cor(iris[, 1:4])
cat("\\n特征相关性矩阵:\\n")
print(cor_matrix)

# 可视化相关性矩阵
corrplot(cor_matrix, method = "circle", type = "upper")

# 箱线图 - 按物种比较特征
ggplot(iris, aes(x = Species, y = Sepal.Length, fill = Species)) +
  geom_boxplot(alpha = 0.7) +
  labs(title = "按物种的萼片长度分布", 
       x = "物种", 
       y = "萼片长度") +
  theme_minimal()

# 散点图矩阵
pairs(iris[, 1:4], col = iris$Species, pch = 19,
      main = "鸢尾花数据集散点图矩阵")

# 密度图
ggplot(iris, aes(x = Petal.Length, fill = Species)) +
  geom_density(alpha = 0.5) +
  labs(title = "花瓣长度的密度分布", 
       x = "花瓣长度", 
       y = "密度") +
  theme_minimal()',
    '探索性数据分析',
    'beginner',
    1
);



