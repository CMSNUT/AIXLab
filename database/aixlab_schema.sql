-- 创建数据库和用户
CREATE DATABASE IF NOT EXISTS aixlab;
USE aixlab;

-- 用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 数据集表
CREATE TABLE datasets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    source_type ENUM('upload', 'builtin') DEFAULT 'builtin',
    builtin_name VARCHAR(50),  -- 内置数据集名称，如 'iris'
    columns JSON,  -- 存储列信息
    row_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 分析任务表
CREATE TABLE analysis_tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dataset_id INT NOT NULL,
    user_id INT NOT NULL,
    analysis_type VARCHAR(50) NOT NULL,  -- clustering, classification, etc
    backend_type ENUM('python', 'R') NOT NULL,
    parameters JSON,
    status ENUM('pending', 'running', 'completed', 'failed') DEFAULT 'pending',
    result JSON,  -- 存储分析结果
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 分析结果表
CREATE TABLE analysis_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    result_type VARCHAR(50),  -- plot, summary, model, etc
    content TEXT,  -- 可以是JSON、base64图片等
    file_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES analysis_tasks(id)
);

-- 插入示例用户
INSERT INTO users (username, email, hashed_password) VALUES
('demo', 'demo@aixlab.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW');

-- 插入Iris数据集信息
INSERT INTO datasets (name, description, source_type, builtin_name, columns, row_count, user_id) VALUES
('Iris Dataset', '经典鸢尾花数据集', 'builtin', 'iris', 
 '["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]', 
 150, 1);