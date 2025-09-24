import pandas as pd
from datetime import datetime, date
from snowflake_connector import SnowflakeConnector
import logging

logger = logging.getLogger(__name__)

class InvestmentTracker:
    """投资跟踪类"""
    
    def __init__(self):
        self.db = SnowflakeConnector()
    
    def add_investment(self, date, investment_type, symbol, name, quantity, price, current_price=None):
        """添加投资记录"""
        try:
            # 验证数据类型
            if investment_type not in ['stock', 'fund', 'crypto', 'bond']:
                raise ValueError("投资类型必须是 'stock', 'fund', 'crypto' 或 'bond'")
            
            if quantity <= 0 or price <= 0:
                raise ValueError("数量和价格必须大于0")
            
            amount = quantity * price
            current_value = quantity * current_price if current_price else amount
            
            if not self.db.connect():
                return False
            
            data = (date, investment_type, symbol, name, quantity, price, amount, current_price, current_value)
            success = self.db.insert_data('investments', data)
            
            self.db.disconnect()
            return success
            
        except Exception as e:
            logger.error(f"添加投资记录失败: {e}")
            return False
    
    def update_investment_prices(self, symbol, current_price):
        """更新投资当前价格"""
        try:
            if not self.db.connect():
                return False
            
            # 获取该投资的数量
            query = "SELECT quantity FROM investments WHERE symbol = %s"
            result = self.db.execute_query(query, (symbol,))
            
            if not result:
                logger.error(f"未找到投资记录: {symbol}")
                return False
            
            quantity = result[0][0]
            current_value = quantity * current_price
            
            # 更新价格和当前价值
            update_query = """
                UPDATE investments 
                SET current_price = %s, current_value = %s 
                WHERE symbol = %s
            """
            self.db.cursor.execute(update_query, (current_price, current_value, symbol))
            self.db.connection.commit()
            
            self.db.disconnect()
            logger.info(f"投资价格更新成功: {symbol} - {current_price}")
            return True
            
        except Exception as e:
            logger.error(f"更新投资价格失败: {e}")
            return False
    
    def get_investments(self, investment_type=None):
        """获取投资记录"""
        try:
            if not self.db.connect():
                return pd.DataFrame()
            
            query = "SELECT * FROM investments"
            params = []
            
            if investment_type:
                query += " WHERE type = %s"
                params.append(investment_type)
            
            query += " ORDER BY date DESC"
            
            result = self.db.execute_query_df(query, params)
            self.db.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"获取投资记录失败: {e}")
            return pd.DataFrame()
    
    def get_investment_summary(self):
        """获取投资摘要"""
        try:
            if not self.db.connect():
                return pd.DataFrame()
            
            result = self.db.get_investment_summary()
            self.db.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"获取投资摘要失败: {e}")
            return pd.DataFrame()
    
    def get_portfolio_performance(self):
        """获取投资组合表现"""
        try:
            if not self.db.connect():
                return pd.DataFrame()
            
            query = """
                SELECT 
                    symbol,
                    name,
                    type,
                    quantity,
                    price as buy_price,
                    current_price,
                    amount as total_invested,
                    current_value,
                    current_value - amount as profit_loss,
                    ROUND(((current_value - amount) / amount) * 100, 2) as return_percentage
                FROM investments
                ORDER BY profit_loss DESC
            """
            
            result = self.db.execute_query_df(query)
            self.db.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"获取投资组合表现失败: {e}")
            return pd.DataFrame()
    
    def get_asset_allocation(self):
        """获取资产配置"""
        try:
            if not self.db.connect():
                return pd.DataFrame()
            
            query = """
                SELECT 
                    type,
                    COUNT(*) as count,
                    SUM(amount) as total_invested,
                    SUM(current_value) as current_value,
                    ROUND((SUM(current_value) / (SELECT SUM(current_value) FROM investments)) * 100, 2) as percentage
                FROM investments
                GROUP BY type
                ORDER BY current_value DESC
            """
            
            result = self.db.execute_query_df(query)
            self.db.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"获取资产配置失败: {e}")
            return pd.DataFrame()
    
    def get_monthly_performance(self, months=12):
        """获取月度投资表现"""
        try:
            if not self.db.connect():
                return pd.DataFrame()
            
            # 这里简化处理，实际应用中需要更复杂的逻辑来计算月度表现
            query = """
                SELECT 
                    DATE_FORMAT(date, '%%Y-%%m') as month,
                    type,
                    SUM(amount) as invested_amount,
                    SUM(current_value) as current_value,
                    SUM(current_value) - SUM(amount) as profit_loss
                FROM investments
                WHERE date >= DATEADD(month, -%s, CURRENT_DATE())
                GROUP BY DATE_FORMAT(date, '%%Y-%%m'), type
                ORDER BY month DESC
            """
            
            result = self.db.execute_query_df(query, (months,))
            self.db.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"获取月度表现失败: {e}")
            return pd.DataFrame()
    
    def get_investment_recommendations(self):
        """获取投资建议"""
        try:
            portfolio = self.get_portfolio_performance()
            
            if portfolio.empty:
                return ["暂无投资数据"]
            
            recommendations = []
            
            # 分析表现最好的投资
            best_performer = portfolio.iloc[0]
            if best_performer['return_percentage'] > 0:
                recommendations.append(f"表现最佳: {best_performer['name']} 收益率 {best_performer['return_percentage']:.2f}%")
            
            # 分析表现最差的投资
            worst_performer = portfolio.iloc[-1]
            if worst_performer['return_percentage'] < -10:
                recommendations.append(f"注意风险: {worst_performer['name']} 亏损 {abs(worst_performer['return_percentage']):.2f}%")
            
            # 分析资产配置
            allocation = self.get_asset_allocation()
            if not allocation.empty:
                # 检查是否过度集中在某个资产类型
                max_percentage = allocation['percentage'].max()
                if max_percentage > 70:
                    max_type = allocation.iloc[0]['type']
                    recommendations.append(f"建议分散投资，{max_type} 占比过高 ({max_percentage:.1f}%)")
            
            # 总体建议
            total_invested = portfolio['total_invested'].sum()
            total_value = portfolio['current_value'].sum()
            total_return = ((total_value - total_invested) / total_invested) * 100
            
            if total_return > 10:
                recommendations.append("投资表现良好，可考虑继续持有")
            elif total_return < -5:
                recommendations.append("投资表现不佳，建议重新评估投资策略")
            else:
                recommendations.append("投资表现平稳，建议定期调整投资组合")
            
            return recommendations if recommendations else ["暂无特殊建议"]
            
        except Exception as e:
            logger.error(f"获取投资建议失败: {e}")
            return ["无法生成投资建议"]
    
    def delete_investment(self, investment_id):
        """删除投资记录"""
        try:
            if not self.db.connect():
                return False
            
            query = "DELETE FROM investments WHERE id = %s"
            self.db.cursor.execute(query, (investment_id,))
            self.db.connection.commit()
            
            self.db.disconnect()
            logger.info(f"投资记录 {investment_id} 删除成功")
            return True
            
        except Exception as e:
            logger.error(f"删除投资记录失败: {e}")
            return False
