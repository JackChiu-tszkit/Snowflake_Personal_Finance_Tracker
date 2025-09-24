import pandas as pd
from datetime import datetime, date
from snowflake_connector import SnowflakeConnector
import logging

logger = logging.getLogger(__name__)

class TransactionManager:
    """交易管理类"""
    
    def __init__(self):
        self.db = SnowflakeConnector()
        
    def add_transaction(self, date, transaction_type, category, amount, description="", tags=""):
        """添加新交易记录"""
        try:
            # 验证数据类型
            if transaction_type not in ['income', 'expense']:
                raise ValueError("交易类型必须是 'income' 或 'expense'")
            
            if amount <= 0:
                raise ValueError("金额必须大于0")
            
            # 连接数据库
            if not self.db.connect():
                return False
            
            # 插入数据
            data = (date, transaction_type, category, amount, description, tags)
            success = self.db.insert_data('transactions', data)
            
            self.db.disconnect()
            return success
            
        except Exception as e:
            logger.error(f"添加交易记录失败: {e}")
            return False
    
    def get_transactions(self, start_date=None, end_date=None, category=None, transaction_type=None):
        """获取交易记录"""
        try:
            if not self.db.connect():
                return pd.DataFrame()
            
            # 构建查询条件
            where_conditions = []
            params = []
            
            if start_date:
                where_conditions.append("date >= %s")
                params.append(start_date)
            
            if end_date:
                where_conditions.append("date <= %s")
                params.append(end_date)
            
            if category:
                where_conditions.append("category = %s")
                params.append(category)
            
            if transaction_type:
                where_conditions.append("type = %s")
                params.append(transaction_type)
            
            # 构建查询语句
            query = "SELECT * FROM transactions"
            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)
            query += " ORDER BY date DESC"
            
            result = self.db.execute_query_df(query, params)
            self.db.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"获取交易记录失败: {e}")
            return pd.DataFrame()
    
    def get_monthly_summary(self, year, month):
        """获取月度财务摘要"""
        try:
            if not self.db.connect():
                return pd.DataFrame()
            
            result = self.db.get_monthly_summary(year, month)
            self.db.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"获取月度摘要失败: {e}")
            return pd.DataFrame()
    
    def get_category_breakdown(self, year, month):
        """获取分类支出明细"""
        try:
            if not self.db.connect():
                return pd.DataFrame()
            
            result = self.db.get_category_breakdown(year, month)
            self.db.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"获取分类明细失败: {e}")
            return pd.DataFrame()
    
    def get_spending_trends(self, months=6):
        """获取支出趋势"""
        try:
            if not self.db.connect():
                return pd.DataFrame()
            
            query = """
                SELECT 
                    YEAR(date) as year,
                    MONTH(date) as month,
                    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expense,
                    SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) as net_income
                FROM transactions 
                WHERE date >= DATEADD(month, -%s, CURRENT_DATE())
                GROUP BY YEAR(date), MONTH(date)
                ORDER BY year, month
            """
            
            result = self.db.execute_query_df(query, (months,))
            self.db.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"获取支出趋势失败: {e}")
            return pd.DataFrame()
    
    def get_top_categories(self, limit=10, transaction_type='expense'):
        """获取支出最多的分类"""
        try:
            if not self.db.connect():
                return pd.DataFrame()
            
            query = """
                SELECT 
                    category,
                    SUM(amount) as total_amount,
                    COUNT(*) as transaction_count,
                    AVG(amount) as avg_amount
                FROM transactions 
                WHERE type = %s
                GROUP BY category
                ORDER BY total_amount DESC
                LIMIT %s
            """
            
            result = self.db.execute_query_df(query, (transaction_type, limit))
            self.db.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"获取分类排行失败: {e}")
            return pd.DataFrame()
    
    def delete_transaction(self, transaction_id):
        """删除交易记录"""
        try:
            if not self.db.connect():
                return False
            
            query = "DELETE FROM transactions WHERE id = %s"
            self.db.cursor.execute(query, (transaction_id,))
            self.db.connection.commit()
            
            self.db.disconnect()
            logger.info(f"交易记录 {transaction_id} 删除成功")
            return True
            
        except Exception as e:
            logger.error(f"删除交易记录失败: {e}")
            return False
    
    def update_transaction(self, transaction_id, **kwargs):
        """更新交易记录"""
        try:
            if not self.db.connect():
                return False
            
            # 构建更新语句
            set_clauses = []
            params = []
            
            allowed_fields = ['date', 'type', 'category', 'amount', 'description', 'tags']
            for field, value in kwargs.items():
                if field in allowed_fields:
                    set_clauses.append(f"{field} = %s")
                    params.append(value)
            
            if not set_clauses:
                logger.error("没有有效的更新字段")
                return False
            
            params.append(transaction_id)
            query = f"UPDATE transactions SET {', '.join(set_clauses)} WHERE id = %s"
            
            self.db.cursor.execute(query, params)
            self.db.connection.commit()
            
            self.db.disconnect()
            logger.info(f"交易记录 {transaction_id} 更新成功")
            return True
            
        except Exception as e:
            logger.error(f"更新交易记录失败: {e}")
            return False
