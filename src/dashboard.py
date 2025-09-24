import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import sys
import os

# 添加src目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transaction_manager import TransactionManager
from budget_analyzer import BudgetAnalyzer
from investment_tracker import InvestmentTracker
from config import APP_CONFIG

# 页面配置
st.set_page_config(
    page_title=APP_CONFIG['page_title'],
    page_icon=APP_CONFIG['page_icon'],
    layout=APP_CONFIG['layout'],
    initial_sidebar_state=APP_CONFIG['initial_sidebar_state']
)

# 初始化管理器
@st.cache_resource
def init_managers():
    return TransactionManager(), BudgetAnalyzer(), InvestmentTracker()

transaction_manager, budget_analyzer, investment_tracker = init_managers()

# 主标题
st.title("💰 个人理财助手")
st.markdown("---")

# 侧边栏导航
st.sidebar.title("📊 导航菜单")
page = st.sidebar.selectbox(
    "选择功能",
    ["📈 财务概览", "💳 交易记录", "📋 预算管理", "📊 投资跟踪", "📝 添加记录"]
)

# 财务概览页面
if page == "📈 财务概览":
    st.header("📈 财务概览")
    
    # 获取当前月份数据
    current_date = datetime.now()
    year, month = current_date.year, current_date.month
    
    # 月度摘要
    monthly_summary = transaction_manager.get_monthly_summary(year, month)
    
    if not monthly_summary.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            income = monthly_summary[monthly_summary['TYPE'] == 'income']['TOTAL_AMOUNT'].sum()
            st.metric("本月收入", f"¥{income:,.2f}")
        
        with col2:
            expense = monthly_summary[monthly_summary['TYPE'] == 'expense']['TOTAL_AMOUNT'].sum()
            st.metric("本月支出", f"¥{expense:,.2f}")
        
        with col3:
            net_income = income - expense
            st.metric("净收入", f"¥{net_income:,.2f}")
        
        with col4:
            # 投资价值
            investment_summary = investment_tracker.get_investment_summary()
            total_investment_value = investment_summary['CURRENT_VALUE'].sum() if not investment_summary.empty else 0
            st.metric("投资价值", f"¥{total_investment_value:,.2f}")
    
    # 支出趋势图
    st.subheader("📊 支出趋势")
    trends = transaction_manager.get_spending_trends(6)
    
    if not trends.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trends['MONTH'], 
            y=trends['INCOME'], 
            mode='lines+markers',
            name='收入',
            line=dict(color='green')
        ))
        fig.add_trace(go.Scatter(
            x=trends['MONTH'], 
            y=trends['EXPENSE'], 
            mode='lines+markers',
            name='支出',
            line=dict(color='red')
        ))
        fig.update_layout(title="6个月收支趋势", xaxis_title="月份", yaxis_title="金额")
        st.plotly_chart(fig, use_container_width=True)
    
    # 分类支出饼图
    st.subheader("🥧 支出分类")
    category_breakdown = transaction_manager.get_category_breakdown(year, month)
    
    if not category_breakdown.empty:
        fig = px.pie(
            category_breakdown, 
            values='TOTAL_AMOUNT', 
            names='CATEGORY',
            title="本月支出分类分布"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 预算状态
    st.subheader("📋 预算状态")
    budget_status = budget_analyzer.get_budget_status()
    
    if not budget_status.empty:
        for _, row in budget_status.iterrows():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{row['CATEGORY']}**")
            with col2:
                progress = min(row['USAGE_PERCENTAGE'] / 100, 1.0)
                st.progress(progress)
            with col3:
                status_color = "🔴" if row['STATUS'] == '超支' else "🟡" if row['STATUS'] == '接近预算' else "🟢"
                st.write(f"{status_color} {row['USAGE_PERCENTAGE']:.1f}%")

# 交易记录页面
elif page == "💳 交易记录":
    st.header("💳 交易记录")
    
    # 筛选选项
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        start_date = st.date_input("开始日期", value=date.today() - timedelta(days=30))
    
    with col2:
        end_date = st.date_input("结束日期", value=date.today())
    
    with col3:
        transaction_type = st.selectbox("交易类型", ["全部", "收入", "支出"])
    
    with col4:
        category = st.selectbox("分类", ["全部", "food", "transport", "shopping", "entertainment", "health"])
    
    # 获取交易记录
    type_filter = None if transaction_type == "全部" else "income" if transaction_type == "收入" else "expense"
    category_filter = None if category == "全部" else category
    
    transactions = transaction_manager.get_transactions(
        start_date=start_date,
        end_date=end_date,
        category=category_filter,
        transaction_type=type_filter
    )
    
    if not transactions.empty:
        st.dataframe(transactions, use_container_width=True)
        
        # 统计信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总交易数", len(transactions))
        with col2:
            total_amount = transactions['AMOUNT'].sum()
            st.metric("总金额", f"¥{total_amount:,.2f}")
        with col3:
            avg_amount = transactions['AMOUNT'].mean()
            st.metric("平均金额", f"¥{avg_amount:,.2f}")
    else:
        st.info("暂无交易记录")

# 预算管理页面
elif page == "📋 预算管理":
    st.header("📋 预算管理")
    
    # 设置预算
    st.subheader("设置预算")
    with st.form("budget_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category = st.selectbox("分类", ["food", "transport", "shopping", "entertainment", "health", "education", "social"])
        
        with col2:
            monthly_budget = st.number_input("月度预算", min_value=0.0, value=1000.0, step=100.0)
        
        with col3:
            month_year = st.text_input("月份 (YYYY-MM)", value=datetime.now().strftime('%Y-%m'))
        
        submitted = st.form_submit_button("设置预算")
        
        if submitted:
            if budget_analyzer.set_budget(category, monthly_budget, month_year):
                st.success(f"预算设置成功: {category} - ¥{monthly_budget}")
            else:
                st.error("预算设置失败")
    
    # 预算状态
    st.subheader("预算状态")
    budget_status = budget_analyzer.get_budget_status()
    
    if not budget_status.empty:
        st.dataframe(budget_status, use_container_width=True)
        
        # 预算警告
        alerts = budget_analyzer.get_budget_alerts()
        if alerts:
            st.subheader("⚠️ 预算警告")
            for alert in alerts:
                if alert['type'] == 'danger':
                    st.error(alert['message'])
                else:
                    st.warning(alert['message'])
        
        # 储蓄建议
        st.subheader("💡 储蓄建议")
        recommendations = budget_analyzer.get_savings_recommendation()
        for rec in recommendations:
            st.info(rec)
    else:
        st.info("暂无预算数据")

# 投资跟踪页面
elif page == "📊 投资跟踪":
    st.header("📊 投资跟踪")
    
    # 投资摘要
    investment_summary = investment_tracker.get_investment_summary()
    
    if not investment_summary.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_invested = investment_summary['TOTAL_INVESTED'].sum()
            st.metric("总投资", f"¥{total_invested:,.2f}")
        
        with col2:
            total_value = investment_summary['CURRENT_VALUE'].sum()
            st.metric("当前价值", f"¥{total_value:,.2f}")
        
        with col3:
            total_profit = investment_summary['PROFIT_LOSS'].sum()
            st.metric("盈亏", f"¥{total_profit:,.2f}")
        
        with col4:
            return_rate = (total_profit / total_invested * 100) if total_invested > 0 else 0
            st.metric("收益率", f"{return_rate:.2f}%")
    
    # 投资组合表现
    st.subheader("📈 投资组合表现")
    portfolio = investment_tracker.get_portfolio_performance()
    
    if not portfolio.empty:
        st.dataframe(portfolio, use_container_width=True)
        
        # 资产配置饼图
        st.subheader("🥧 资产配置")
        allocation = investment_tracker.get_asset_allocation()
        
        if not allocation.empty:
            fig = px.pie(
                allocation, 
                values='CURRENT_VALUE', 
                names='TYPE',
                title="资产类型分布"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 投资建议
        st.subheader("💡 投资建议")
        recommendations = investment_tracker.get_investment_recommendations()
        for rec in recommendations:
            st.info(rec)
    else:
        st.info("暂无投资数据")

# 添加记录页面
elif page == "📝 添加记录":
    st.header("📝 添加记录")
    
    # 添加交易记录
    st.subheader("添加交易记录")
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            trans_date = st.date_input("日期", value=date.today())
            trans_type = st.selectbox("类型", ["收入", "支出"])
            category = st.selectbox("分类", ["food", "transport", "shopping", "entertainment", "health", "education", "social", "salary"])
        
        with col2:
            amount = st.number_input("金额", min_value=0.01, value=100.0, step=0.01)
            description = st.text_input("描述")
            tags = st.text_input("标签")
        
        submitted = st.form_submit_button("添加交易")
        
        if submitted:
            type_value = "income" if trans_type == "收入" else "expense"
            if transaction_manager.add_transaction(trans_date, type_value, category, amount, description, tags):
                st.success("交易记录添加成功！")
            else:
                st.error("交易记录添加失败！")
    
    # 添加投资记录
    st.subheader("添加投资记录")
    with st.form("investment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            inv_date = st.date_input("投资日期", value=date.today(), key="inv_date")
            inv_type = st.selectbox("投资类型", ["stock", "fund", "crypto", "bond"], key="inv_type")
            symbol = st.text_input("代码/符号", key="symbol")
            name = st.text_input("名称", key="name")
        
        with col2:
            quantity = st.number_input("数量", min_value=0.0001, value=1.0, step=0.0001, key="quantity")
            price = st.number_input("买入价格", min_value=0.01, value=100.0, step=0.01, key="price")
            current_price = st.number_input("当前价格", min_value=0.01, value=100.0, step=0.01, key="current_price")
        
        submitted = st.form_submit_button("添加投资")
        
        if submitted:
            if investment_tracker.add_investment(inv_date, inv_type, symbol, name, quantity, price, current_price):
                st.success("投资记录添加成功！")
            else:
                st.error("投资记录添加失败！")

# 页脚
st.markdown("---")
st.markdown("💡 提示：首次使用请先配置Snowflake连接信息")
