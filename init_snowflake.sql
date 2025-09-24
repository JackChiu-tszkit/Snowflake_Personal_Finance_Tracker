-- 个人理财助手 - Snowflake 初始化脚本
-- 请在Snowflake中执行以下SQL语句

-- 1. 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS FINANCE_DB;

-- 2. 使用数据库
USE DATABASE FINANCE_DB;

-- 3. 创建Schema（如果不存在）
CREATE SCHEMA IF NOT EXISTS PUBLIC;

-- 4. 使用Schema
USE SCHEMA PUBLIC;

-- 5. 创建交易记录表
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255),
    tags VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. 创建预算表
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    monthly_budget DECIMAL(10,2) NOT NULL,
    current_spent DECIMAL(10,2) DEFAULT 0,
    month_year VARCHAR(7) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. 创建投资表
CREATE TABLE IF NOT EXISTS investments (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('stock', 'fund', 'crypto', 'bond')),
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    quantity DECIMAL(10,4) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    current_price DECIMAL(10,2),
    current_value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. 创建分类表
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. 插入默认分类数据
INSERT INTO categories (name, type, description) VALUES
('salary', 'income', '工资收入'),
('bonus', 'income', '奖金收入'),
('investment', 'income', '投资收益'),
('other_income', 'income', '其他收入'),
('food', 'expense', '餐饮支出'),
('transport', 'expense', '交通支出'),
('shopping', 'expense', '购物支出'),
('entertainment', 'expense', '娱乐支出'),
('health', 'expense', '健康支出'),
('education', 'expense', '教育支出'),
('social', 'expense', '社交支出'),
('housing', 'expense', '住房支出'),
('utilities', 'expense', '水电费'),
('other_expense', 'expense', '其他支出')
ON CONFLICT (name) DO NOTHING;

-- 10. 创建一些示例预算数据
INSERT INTO budgets (category, monthly_budget, current_spent, month_year) VALUES
('food', 800, 0, '2024-01'),
('transport', 200, 0, '2024-01'),
('shopping', 1000, 0, '2024-01'),
('entertainment', 300, 0, '2024-01'),
('health', 500, 0, '2024-01'),
('education', 200, 0, '2024-01'),
('social', 300, 0, '2024-01')
ON CONFLICT DO NOTHING;

-- 11. 验证表创建
SELECT 'Tables created successfully' as status;
SELECT table_name FROM information_schema.tables WHERE table_schema = 'PUBLIC';
