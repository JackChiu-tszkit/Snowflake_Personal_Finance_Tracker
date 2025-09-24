import pandas as pd
from datetime import datetime, date
from snowflake_connector import SnowflakeConnector
import logging

logger = logging.getLogger(__name__)

class BudgetAnalyzer:
    """预算分析类"""
    
    def __init__(self):
        self.db = SnowflakeConnector()
    
    def set_budget(self, category, monthly_budget, month_year=None):
        """设置月度预算"""
        try:
            if month_year is None:
                month_year = datetime.now().strftime('%Y-%m')
            
            if not self.db.connect():
                return False
            
            # 检查是否已存在该月的预算
            check_query = """
                SELECT id FROM budgets 
                WHERE category = %s AND month_year = %s
            """
            existing = self.db.execute_query(check_query, (category, month_year))
            
            if existing:
                # 更新现有预算
                update_query = """
                    UPDATE budgets 
                    SET monthly_budget = %s 
                    WHERE category = %s AND month_year = %s
                """
                self.db.cursor.execute(update_query, (monthly_budget, category, month_year))
            else:
                # 插入新预算
                data = (category, monthly_budget, 0, month_year)
                self.db.insert_data('budgets', data)
            
            self.db.connection.commit()
            self.db.disconnect()
            logger.info(f"预算设置成功: {category} - {monthly_budget}")
            return True
            
        except Exception as e:
            logger.error(f"设置预算失败: {e}")
            return False
    
    def update_budget_spending(self, month_year=None):
        """更新预算支出统计"""
        try:
            if month_year is None:
                month_year = datetime.now().strftime('%Y-%m')
            
            if not self.db.connect():
                return False
            
            # 获取当月各分类的实际支出
            spending_query = """
                SELECT 
                    category,
                    SUM(amount) as total_spent
                FROM transactions 
                WHERE type = 'expense' 
                AND DATE_FORMAT(date, '%%Y-%%m') = %s
                GROUP BY category
            """
            
            spending_data = self.db.execute_query_df(spending_query, (month_year,))
            
            # 更新预算表中的实际支出
            for _, row in spending_data.iterrows():
                update_query = """
                    UPDATE budgets 
                    SET current_spent = %s 
                    WHERE category = %s AND month_year = %s
                """
                self.db.cursor.execute(update_query, (row['total_spent'], row['category'], month_year))
            
            self.db.connection.commit()
            self.db.disconnect()
            logger.info(f"预算支出统计更新成功: {month_year}")
            return True
            
        except Exception as e:
            logger.error(f"更新预算支出失败: {e}")
            return False
    
    def get_budget_status(self, month_year=None):
        """获取预算状态"""
        try:
            if month_year is None:
                month_year = datetime.now().strftime('%Y-%m')
            
            if not self.db.connect():
                return pd.DataFrame()
            
            # 先更新支出统计
            self.update_budget_spending(month_year)
            
            # 获取预算状态
            query = """
                SELECT 
                    category,
                    monthly_budget,
                    current_spent,
                    monthly_budget - current_spent as remaining,
                    CASE 
                        WHEN current_spent > monthly_budget THEN '超支'
                        WHEN current_spent > monthly_budget * 0.8 THEN '接近预算'
                        ELSE '正常'
                    END as status,
                    ROUND((current_spent / monthly_budget) * 100, 2) as usage_percentage
                FROM budgets 
                WHERE month_year = %s
                ORDER BY usage_percentage DESC
            """
            
            result = self.db.execute_query_df(query, (month_year,))
            self.db.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"获取预算状态失败: {e}")
            return pd.DataFrame()
    
    def get_budget_alerts(self, month_year=None):
        """获取预算警告"""
        try:
            if month_year is None:
                month_year = datetime.now().strftime('%Y-%m')
            
            budget_status = self.get_budget_status(month_year)
            
            alerts = []
            for _, row in budget_status.iterrows():
                if row['status'] == '超支':
                    alerts.append({
                        'type': 'danger',
                        'category': row['category'],
                        'message': f"{row['category']} 已超支 {abs(row['remaining']):.2f} 元",
                        'amount': abs(row['remaining'])
                    })
                elif row['status'] == '接近预算':
                    alerts.append({
                        'type': 'warning',
                        'category': row['category'],
                        'message': f"{row['category']} 已使用 {row['usage_percentage']:.1f}% 预算",
                        'amount': row['remaining']
                    })
            
            return alerts
            
        except Exception as e:
            logger.error(f"获取预算警告失败: {e}")
            return []
    
    def get_budget_trends(self, months=6):
        """获取预算趋势分析"""
        try:
            if not self.db.connect():
                return pd.DataFrame()
            
            query = """
                SELECT 
                    month_year,
                    category,
                    monthly_budget,
                    current_spent,
                    monthly_budget - current_spent as remaining
                FROM budgets 
                WHERE month_year >= DATE_FORMAT(DATEADD(month, -%s, CURRENT_DATE()), '%%Y-%%m')
                ORDER BY month_year DESC, category
            """
            
            result = self.db.execute_query_df(query, (months,))
            self.db.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"获取预算趋势失败: {e}")
            return pd.DataFrame()
    
    def get_savings_recommendation(self, month_year=None):
        """获取储蓄建议"""
        try:
            if month_year is None:
                month_year = datetime.now().strftime('%Y-%m')
            
            budget_status = self.get_budget_status(month_year)
            
            if budget_status.empty:
                return "暂无预算数据"
            
            # 计算总预算和总支出
            total_budget = budget_status['monthly_budget'].sum()
            total_spent = budget_status['current_spent'].sum()
            total_remaining = total_budget - total_spent
            
            # 找出超支最多的分类
            overspent = budget_status[budget_status['remaining'] < 0]
            
            recommendations = []
            
            if total_remaining < 0:
                recommendations.append(f"本月超支 {abs(total_remaining):.2f} 元，建议减少不必要的支出")
            
            if not overspent.empty:
                top_overspent = overspent.iloc[0]
                recommendations.append(f"建议控制 {top_overspent['category']} 支出，已超支 {abs(top_overspent['remaining']):.2f} 元")
            
            # 找出可以优化的分类
            high_usage = budget_status[
                (budget_status['usage_percentage'] > 80) & 
                (budget_status['usage_percentage'] < 100)
            ]
            
            if not high_usage.empty:
                recommendations.append(f"注意 {high_usage.iloc[0]['category']} 支出，已使用 {high_usage.iloc[0]['usage_percentage']:.1f}% 预算")
            
            if total_remaining > 0:
                recommendations.append(f"本月还有 {total_remaining:.2f} 元预算余额，可以考虑储蓄或投资")
            
            return recommendations if recommendations else ["预算使用情况良好"]
            
        except Exception as e:
            logger.error(f"获取储蓄建议失败: {e}")
            return ["无法生成建议"]
