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
from languages import get_text, get_language_list, LANGUAGES

# 语言选择
if 'language' not in st.session_state:
    st.session_state.language = 'en'

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

# 语言选择器
st.sidebar.title("🌍 Language / Språk")
language_options = get_language_list()
selected_lang = st.sidebar.selectbox(
    "Select Language / Velg Språk:",
    options=[code for code, _ in language_options],
    format_func=lambda x: next(display for code, display in language_options if code == x),
    index=[code for code, _ in language_options].index(st.session_state.language)
)

if selected_lang != st.session_state.language:
    st.session_state.language = selected_lang
    st.rerun()

# 获取当前语言
lang = st.session_state.language

# 主标题
st.title(get_text(lang, 'app_title', 'app_title'))
st.markdown("---")

# 侧边栏导航
st.sidebar.title("📊 " + get_text(lang, 'navigation', 'overview').split(' ', 1)[1])
page = st.sidebar.selectbox(
    get_text(lang, 'transactions', 'transaction_type'),
    [
        get_text(lang, 'navigation', 'overview'),
        get_text(lang, 'navigation', 'transactions'),
        get_text(lang, 'navigation', 'budgets'),
        get_text(lang, 'navigation', 'investments'),
        get_text(lang, 'navigation', 'add_record')
    ]
)

# 财务概览页面
if page == get_text(lang, 'navigation', 'overview'):
    st.header(get_text(lang, 'overview', 'title'))
    
    # 获取当前月份数据
    current_date = datetime.now()
    year, month = current_date.year, current_date.month
    
    # 月度摘要
    monthly_summary = transaction_manager.get_monthly_summary(year, month)
    
    if not monthly_summary.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            income = monthly_summary[monthly_summary['TYPE'] == 'income']['TOTAL_AMOUNT'].sum()
            st.metric(get_text(lang, 'overview', 'monthly_income'), f"¥{income:,.2f}")
        
        with col2:
            expense = monthly_summary[monthly_summary['TYPE'] == 'expense']['TOTAL_AMOUNT'].sum()
            st.metric(get_text(lang, 'overview', 'monthly_expense'), f"¥{expense:,.2f}")
        
        with col3:
            net_income = income - expense
            st.metric(get_text(lang, 'overview', 'net_income'), f"¥{net_income:,.2f}")
        
        with col4:
            # 投资价值
            investment_summary = investment_tracker.get_investment_summary()
            total_investment_value = investment_summary['CURRENT_VALUE'].sum() if not investment_summary.empty else 0
            st.metric(get_text(lang, 'overview', 'investment_value'), f"¥{total_investment_value:,.2f}")
    
    # 支出趋势图
    st.subheader(get_text(lang, 'overview', 'spending_trends'))
    trends = transaction_manager.get_spending_trends(6)
    
    if not trends.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trends['MONTH'], 
            y=trends['INCOME'], 
            mode='lines+markers',
            name=get_text(lang, 'overview', 'monthly_income'),
            line=dict(color='green')
        ))
        fig.add_trace(go.Scatter(
            x=trends['MONTH'], 
            y=trends['EXPENSE'], 
            mode='lines+markers',
            name=get_text(lang, 'overview', 'monthly_expense'),
            line=dict(color='red')
        ))
        fig.update_layout(title="6 months income/expense trends", xaxis_title="Month", yaxis_title="Amount")
        st.plotly_chart(fig, use_container_width=True)
    
    # 分类支出饼图
    st.subheader(get_text(lang, 'overview', 'expense_breakdown'))
    category_breakdown = transaction_manager.get_category_breakdown(year, month)
    
    if not category_breakdown.empty:
        fig = px.pie(
            category_breakdown, 
            values='TOTAL_AMOUNT', 
            names='CATEGORY',
            title="Monthly expense breakdown"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 预算状态
    st.subheader(get_text(lang, 'overview', 'budget_status'))
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
elif page == get_text(lang, 'navigation', 'transactions'):
    st.header(get_text(lang, 'transactions', 'title'))
    
    # 筛选选项
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        start_date = st.date_input(get_text(lang, 'transactions', 'start_date'), value=date.today() - timedelta(days=30))
    
    with col2:
        end_date = st.date_input(get_text(lang, 'transactions', 'end_date'), value=date.today())
    
    with col3:
        transaction_type = st.selectbox(get_text(lang, 'transactions', 'transaction_type'), 
                                      [get_text(lang, 'transactions', 'all'), 
                                       get_text(lang, 'transactions', 'income'), 
                                       get_text(lang, 'transactions', 'expense')])
    
    with col4:
        category = st.selectbox(get_text(lang, 'transactions', 'category'), 
                              [get_text(lang, 'transactions', 'all'), "food", "transport", "shopping", "entertainment", "health"])
    
    # 获取交易记录
    type_filter = None if transaction_type == get_text(lang, 'transactions', 'all') else "income" if transaction_type == get_text(lang, 'transactions', 'income') else "expense"
    category_filter = None if category == get_text(lang, 'transactions', 'all') else category
    
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
            st.metric(get_text(lang, 'transactions', 'total_transactions'), len(transactions))
        with col2:
            total_amount = transactions['AMOUNT'].sum()
            st.metric(get_text(lang, 'transactions', 'total_amount'), f"¥{total_amount:,.2f}")
        with col3:
            avg_amount = transactions['AMOUNT'].mean()
            st.metric(get_text(lang, 'transactions', 'average_amount'), f"¥{avg_amount:,.2f}")
    else:
        st.info(get_text(lang, 'transactions', 'no_records'))

# 预算管理页面
elif page == get_text(lang, 'navigation', 'budgets'):
    st.header(get_text(lang, 'budgets', 'title'))
    
    # 设置预算
    st.subheader(get_text(lang, 'budgets', 'set_budget'))
    with st.form("budget_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category = st.selectbox(get_text(lang, 'budgets', 'category'), 
                                  ["food", "transport", "shopping", "entertainment", "health", "education", "social"])
        
        with col2:
            monthly_budget = st.number_input(get_text(lang, 'budgets', 'monthly_budget'), 
                                           min_value=0.0, value=1000.0, step=100.0)
        
        with col3:
            month_year = st.text_input(get_text(lang, 'budgets', 'month_year'), 
                                     value=datetime.now().strftime('%Y-%m'))
        
        submitted = st.form_submit_button(get_text(lang, 'budgets', 'set_budget_btn'))
        
        if submitted:
            if budget_analyzer.set_budget(category, monthly_budget, month_year):
                st.success(f"{get_text(lang, 'messages', 'budget_set')}: {category} - ¥{monthly_budget}")
            else:
                st.error(get_text(lang, 'messages', 'budget_failed'))
    
    # 预算状态
    st.subheader(get_text(lang, 'budgets', 'budget_status'))
    budget_status = budget_analyzer.get_budget_status()
    
    if not budget_status.empty:
        st.dataframe(budget_status, use_container_width=True)
        
        # 预算警告
        alerts = budget_analyzer.get_budget_alerts()
        if alerts:
            st.subheader(get_text(lang, 'budgets', 'budget_alerts'))
            for alert in alerts:
                if alert['type'] == 'danger':
                    st.error(alert['message'])
                else:
                    st.warning(alert['message'])
        
        # 储蓄建议
        st.subheader(get_text(lang, 'budgets', 'savings_recommendations'))
        recommendations = budget_analyzer.get_savings_recommendation()
        for rec in recommendations:
            st.info(rec)
    else:
        st.info(get_text(lang, 'budgets', 'no_budget_data'))

# 投资跟踪页面
elif page == get_text(lang, 'navigation', 'investments'):
    st.header(get_text(lang, 'investments', 'title'))
    
    # 投资摘要
    investment_summary = investment_tracker.get_investment_summary()
    
    if not investment_summary.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_invested = investment_summary['TOTAL_INVESTED'].sum()
            st.metric(get_text(lang, 'investments', 'total_invested'), f"¥{total_invested:,.2f}")
        
        with col2:
            total_value = investment_summary['CURRENT_VALUE'].sum()
            st.metric(get_text(lang, 'investments', 'current_value'), f"¥{total_value:,.2f}")
        
        with col3:
            total_profit = investment_summary['PROFIT_LOSS'].sum()
            st.metric(get_text(lang, 'investments', 'profit_loss'), f"¥{total_profit:,.2f}")
        
        with col4:
            return_rate = (total_profit / total_invested * 100) if total_invested > 0 else 0
            st.metric(get_text(lang, 'investments', 'return_rate'), f"{return_rate:.2f}%")
    
    # 投资组合表现
    st.subheader(get_text(lang, 'investments', 'portfolio_performance'))
    portfolio = investment_tracker.get_portfolio_performance()
    
    if not portfolio.empty:
        st.dataframe(portfolio, use_container_width=True)
        
        # 资产配置饼图
        st.subheader(get_text(lang, 'investments', 'asset_allocation'))
        allocation = investment_tracker.get_asset_allocation()
        
        if not allocation.empty:
            fig = px.pie(
                allocation, 
                values='CURRENT_VALUE', 
                names='TYPE',
                title="Asset type distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 投资建议
        st.subheader(get_text(lang, 'investments', 'investment_recommendations'))
        recommendations = investment_tracker.get_investment_recommendations()
        for rec in recommendations:
            st.info(rec)
    else:
        st.info(get_text(lang, 'investments', 'no_investment_data'))

# 添加记录页面
elif page == get_text(lang, 'navigation', 'add_record'):
    st.header(get_text(lang, 'add_record', 'title'))
    
    # 添加交易记录
    st.subheader(get_text(lang, 'add_record', 'add_transaction'))
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            trans_date = st.date_input(get_text(lang, 'add_record', 'date'), value=date.today())
            trans_type = st.selectbox(get_text(lang, 'add_record', 'type'), 
                                    [get_text(lang, 'transactions', 'income'), 
                                     get_text(lang, 'transactions', 'expense')])
            category = st.selectbox(get_text(lang, 'add_record', 'category'), 
                                  ["food", "transport", "shopping", "entertainment", "health", "education", "social", "salary"])
        
        with col2:
            amount = st.number_input(get_text(lang, 'add_record', 'amount'), 
                                   min_value=0.01, value=100.0, step=0.01)
            description = st.text_input(get_text(lang, 'add_record', 'description'))
            tags = st.text_input(get_text(lang, 'add_record', 'tags'))
        
        submitted = st.form_submit_button(get_text(lang, 'add_record', 'add_transaction_btn'))
        
        if submitted:
            type_value = "income" if trans_type == get_text(lang, 'transactions', 'income') else "expense"
            if transaction_manager.add_transaction(trans_date, type_value, category, amount, description, tags):
                st.success(get_text(lang, 'messages', 'transaction_added'))
            else:
                st.error(get_text(lang, 'messages', 'transaction_failed'))
    
    # 添加投资记录
    st.subheader(get_text(lang, 'add_record', 'add_investment'))
    with st.form("investment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            inv_date = st.date_input(get_text(lang, 'add_record', 'investment_date'), 
                                   value=date.today(), key="inv_date")
            inv_type = st.selectbox(get_text(lang, 'add_record', 'investment_type'), 
                                  ["stock", "fund", "crypto", "bond"], key="inv_type")
            symbol = st.text_input(get_text(lang, 'add_record', 'symbol'), key="symbol")
            name = st.text_input(get_text(lang, 'add_record', 'name'), key="name")
        
        with col2:
            quantity = st.number_input(get_text(lang, 'add_record', 'quantity'), 
                                     min_value=0.0001, value=1.0, step=0.0001, key="quantity")
            price = st.number_input(get_text(lang, 'add_record', 'buy_price'), 
                                  min_value=0.01, value=100.0, step=0.01, key="price")
            current_price = st.number_input(get_text(lang, 'add_record', 'current_price'), 
                                          min_value=0.01, value=100.0, step=0.01, key="current_price")
        
        submitted = st.form_submit_button(get_text(lang, 'add_record', 'add_investment_btn'))
        
        if submitted:
            if investment_tracker.add_investment(inv_date, inv_type, symbol, name, quantity, price, current_price):
                st.success(get_text(lang, 'messages', 'investment_added'))
            else:
                st.error(get_text(lang, 'messages', 'investment_failed'))

# 页脚
st.markdown("---")
st.markdown("💡 " + ("Tip: Please configure Snowflake connection information first" if lang == 'en' else "Tips: Konfigurer Snowflake-tilkoblingsinformasjon først"))
