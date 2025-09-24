import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Snowflake 连接配置
SNOWFLAKE_CONFIG = {
    'account': os.getenv('SNOWFLAKE_ACCOUNT', 'your_account'),
    'user': os.getenv('SNOWFLAKE_USER', 'your_username'),
    'password': os.getenv('SNOWFLAKE_PASSWORD', 'your_password'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
    'database': os.getenv('SNOWFLAKE_DATABASE', 'FINANCE_DB'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC'),
    'role': os.getenv('SNOWFLAKE_ROLE', 'ACCOUNTADMIN')
}

# 应用配置
APP_CONFIG = {
    'page_title': '个人理财助手',
    'page_icon': '💰',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# 数据表配置
TABLE_CONFIG = {
    'transactions': 'transactions',
    'budgets': 'budgets', 
    'investments': 'investments',
    'categories': 'categories'
}
