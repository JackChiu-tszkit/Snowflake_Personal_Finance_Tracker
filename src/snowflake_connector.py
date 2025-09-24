import snowflake.connector
import pandas as pd
from config import SNOWFLAKE_CONFIG, TABLE_CONFIG
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SnowflakeConnector:
    """Snowflake数据库连接器"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """建立Snowflake连接"""
        try:
            self.connection = snowflake.connector.connect(
                account=SNOWFLAKE_CONFIG['account'],
                user=SNOWFLAKE_CONFIG['user'],
                password=SNOWFLAKE_CONFIG['password'],
                warehouse=SNOWFLAKE_CONFIG['warehouse'],
                database=SNOWFLAKE_CONFIG['database'],
                schema=SNOWFLAKE_CONFIG['schema'],
                role=SNOWFLAKE_CONFIG['role']
            )
            self.cursor = self.connection.cursor()
            logger.info("成功连接到Snowflake数据库")
            return True
        except Exception as e:
            logger.error(f"连接Snowflake失败: {e}")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("已断开Snowflake连接")
    
    def execute_query(self, query, params=None):
        """执行SQL查询"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"查询执行失败: {e}")
            return None
    
    def execute_query_df(self, query, params=None):
        """执行查询并返回DataFrame"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            # 获取列名
            columns = [desc[0] for desc in self.cursor.description]
            # 获取数据
            data = self.cursor.fetchall()
            
            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            logger.error(f"查询执行失败: {e}")
            return pd.DataFrame()
    
    def create_tables(self):
        """创建数据表"""
        tables = {
            'transactions': """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER AUTOINCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
                    category VARCHAR(50) NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    description VARCHAR(255),
                    tags VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            'budgets': """
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER AUTOINCREMENT PRIMARY KEY,
                    category VARCHAR(50) NOT NULL,
                    monthly_budget DECIMAL(10,2) NOT NULL,
                    current_spent DECIMAL(10,2) DEFAULT 0,
                    month_year VARCHAR(7) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            'investments': """
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
                )
            """,
            'categories': """
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER AUTOINCREMENT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL UNIQUE,
                    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
                    description VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
        }
        
        for table_name, create_sql in tables.items():
            try:
                self.cursor.execute(create_sql)
                logger.info(f"表 {table_name} 创建成功")
            except Exception as e:
                logger.error(f"创建表 {table_name} 失败: {e}")
    
    def insert_data(self, table_name, data):
        """插入数据"""
        try:
            if table_name == 'transactions':
                query = """
                    INSERT INTO transactions (date, type, category, amount, description, tags)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
            elif table_name == 'budgets':
                query = """
                    INSERT INTO budgets (category, monthly_budget, current_spent, month_year)
                    VALUES (%s, %s, %s, %s)
                """
            elif table_name == 'investments':
                query = """
                    INSERT INTO investments (date, type, symbol, name, quantity, price, amount, current_price, current_value)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            else:
                logger.error(f"不支持的表名: {table_name}")
                return False
            
            if isinstance(data, list):
                self.cursor.executemany(query, data)
            else:
                self.cursor.execute(query, data)
            
            self.connection.commit()
            logger.info(f"数据插入到 {table_name} 成功")
            return True
        except Exception as e:
            logger.error(f"插入数据到 {table_name} 失败: {e}")
            return False
    
    def get_monthly_summary(self, year, month):
        """获取月度财务摘要"""
        query = """
            SELECT 
                type,
                SUM(amount) as total_amount,
                COUNT(*) as transaction_count
            FROM transactions 
            WHERE YEAR(date) = %s AND MONTH(date) = %s
            GROUP BY type
        """
        return self.execute_query_df(query, (year, month))
    
    def get_category_breakdown(self, year, month):
        """获取分类支出明细"""
        query = """
            SELECT 
                category,
                SUM(amount) as total_amount,
                COUNT(*) as transaction_count
            FROM transactions 
            WHERE type = 'expense' AND YEAR(date) = %s AND MONTH(date) = %s
            GROUP BY category
            ORDER BY total_amount DESC
        """
        return self.execute_query_df(query, (year, month))
    
    def get_investment_summary(self):
        """获取投资摘要"""
        query = """
            SELECT 
                type,
                COUNT(*) as count,
                SUM(amount) as total_invested,
                SUM(current_value) as current_value,
                SUM(current_value) - SUM(amount) as profit_loss
            FROM investments
            GROUP BY type
        """
        return self.execute_query_df(query)
