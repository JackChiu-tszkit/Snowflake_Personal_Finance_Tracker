#!/usr/bin/env python3
"""
导入示例数据到Snowflake
"""

import pandas as pd
import sys
import os
from datetime import datetime

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from snowflake_connector import SnowflakeConnector

def import_sample_data():
    """导入示例数据"""
    print("🚀 开始导入示例数据到Snowflake...")
    
    # 初始化连接器
    db = SnowflakeConnector()
    
    try:
        # 连接数据库
        if not db.connect():
            print("❌ 无法连接到Snowflake数据库")
            print("请检查你的连接配置：")
            print("1. 确保.env文件中的Snowflake连接信息正确")
            print("2. 确保Snowflake账户有足够的权限")
            print("3. 确保网络连接正常")
            return False
        
        print("✅ 成功连接到Snowflake数据库")
        
        # 创建表结构
        print("📋 创建数据表...")
        db.create_tables()
        
        # 导入交易数据
        print("💳 导入交易数据...")
        transactions_df = pd.read_csv('data/sample_transactions.csv')
        
        # 转换数据格式
        transactions_data = []
        for _, row in transactions_df.iterrows():
            transactions_data.append((
                row['date'],
                row['type'],
                row['category'],
                row['amount'],
                row['description'],
                row['tags']
            ))
        
        if db.insert_data('transactions', transactions_data):
            print(f"✅ 成功导入 {len(transactions_data)} 条交易记录")
        else:
            print("❌ 交易数据导入失败")
        
        # 导入预算数据
        print("📋 导入预算数据...")
        budgets_df = pd.read_csv('data/sample_budgets.csv')
        
        budgets_data = []
        for _, row in budgets_df.iterrows():
            budgets_data.append((
                row['category'],
                row['monthly_budget'],
                row['current_spent'],
                '2024-01'  # 默认月份
            ))
        
        if db.insert_data('budgets', budgets_data):
            print(f"✅ 成功导入 {len(budgets_data)} 条预算记录")
        else:
            print("❌ 预算数据导入失败")
        
        # 导入投资数据
        print("📊 导入投资数据...")
        investments_df = pd.read_csv('data/sample_investments.csv')
        
        investments_data = []
        for _, row in investments_df.iterrows():
            investments_data.append((
                row['date'],
                row['type'],
                row['symbol'],
                row['name'],
                row['quantity'],
                row['price'],
                row['amount'],
                row['current_price'],
                row['current_value']
            ))
        
        if db.insert_data('investments', investments_data):
            print(f"✅ 成功导入 {len(investments_data)} 条投资记录")
        else:
            print("❌ 投资数据导入失败")
        
        print("🎉 示例数据导入完成！")
        return True
        
    except Exception as e:
        print(f"❌ 导入过程中出现错误: {e}")
        return False
    
    finally:
        # 断开连接
        db.disconnect()

def main():
    """主函数"""
    print("=" * 50)
    print("💰 个人理财助手 - 数据导入工具")
    print("=" * 50)
    
    # 检查环境变量文件
    if not os.path.exists('.env'):
        print("❌ 未找到.env文件")
        print("请先创建.env文件并配置Snowflake连接信息")
        print("参考.env.example文件")
        return
    
    # 检查示例数据文件
    required_files = [
        'data/sample_transactions.csv',
        'data/sample_budgets.csv', 
        'data/sample_investments.csv'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ 未找到文件: {file_path}")
            return
    
    # 开始导入
    success = import_sample_data()
    
    if success:
        print("\n🎉 数据导入成功！现在可以运行应用了：")
        print("python run.py")
    else:
        print("\n❌ 数据导入失败，请检查配置和网络连接")

if __name__ == "__main__":
    main()
