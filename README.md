# 💰 个人理财助手 (Personal Finance Tracker)

一个基于 **Cursor AI** 和 **Snowflake** 的智能个人理财管理系统，帮助你更好地管理个人财务。

## 🌟 功能特性

### 📈 财务概览
- 实时显示月度收支情况
- 6个月收支趋势分析
- 支出分类饼图展示
- 预算使用状态监控

### 💳 交易记录管理
- 添加收入/支出记录
- 按日期、类型、分类筛选
- 交易记录查询和统计
- 支持标签分类

### 📋 预算管理
- 设置各类别月度预算
- 实时预算使用监控
- 超支警告提醒
- 智能储蓄建议

### 📊 投资跟踪
- 记录股票、基金、加密货币等投资
- 实时计算投资盈亏
- 投资组合表现分析
- 资产配置可视化
- 投资建议生成

## 🛠️ 技术栈

- **前端界面**: Streamlit
- **数据库**: Snowflake
- **后端语言**: Python
- **数据可视化**: Plotly
- **AI辅助开发**: Cursor

## 📦 安装和配置

### 1. 克隆项目
```bash
git clone <repository-url>
cd snowflake_v1
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置Snowflake连接
复制 `.env.example` 文件为 `.env` 并填入你的Snowflake连接信息：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
SNOWFLAKE_ACCOUNT=your_account.snowflakecomputing.com
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=FINANCE_DB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ACCOUNTADMIN
```

### 4. 初始化数据库
首次运行时，系统会自动创建所需的数据表。

## 🚀 运行应用

```bash
streamlit run src/dashboard.py
```

应用将在浏览器中打开，默认地址为 `http://localhost:8501`

## 📊 数据表结构

### transactions (交易记录表)
- `id`: 主键
- `date`: 交易日期
- `type`: 交易类型 (income/expense)
- `category`: 分类
- `amount`: 金额
- `description`: 描述
- `tags`: 标签
- `created_at`: 创建时间

### budgets (预算表)
- `id`: 主键
- `category`: 分类
- `monthly_budget`: 月度预算
- `current_spent`: 当前支出
- `month_year`: 年月
- `created_at`: 创建时间

### investments (投资表)
- `id`: 主键
- `date`: 投资日期
- `type`: 投资类型 (stock/fund/crypto/bond)
- `symbol`: 代码/符号
- `name`: 名称
- `quantity`: 数量
- `price`: 买入价格
- `amount`: 投资金额
- `current_price`: 当前价格
- `current_value`: 当前价值
- `created_at`: 创建时间

## 🎯 使用指南

### 1. 首次使用
1. 配置Snowflake连接信息
2. 运行应用
3. 在"添加记录"页面添加一些示例数据

### 2. 日常使用
1. **记录交易**: 在"添加记录"页面记录日常收支
2. **设置预算**: 在"预算管理"页面设置各类别预算
3. **跟踪投资**: 记录投资并定期更新价格
4. **查看分析**: 在"财务概览"页面查看整体财务状况

### 3. 数据导入
可以使用 `data/` 目录下的示例CSV文件导入初始数据。

## 🔧 开发说明

### 项目结构
```
snowflake_v1/
├── data/                    # 示例数据文件
│   ├── sample_transactions.csv
│   ├── sample_budgets.csv
│   └── sample_investments.csv
├── src/                     # 源代码
│   ├── snowflake_connector.py    # Snowflake连接器
│   ├── transaction_manager.py    # 交易管理
│   ├── budget_analyzer.py        # 预算分析
│   ├── investment_tracker.py     # 投资跟踪
│   └── dashboard.py              # Streamlit界面
├── config.py                # 配置文件
├── requirements.txt         # 依赖包
└── README.md               # 项目说明
```

### 扩展功能
- 可以添加更多数据可视化图表
- 支持数据导出功能
- 添加财务目标设定和跟踪
- 集成更多投资数据源

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License

## 🙏 致谢

- 感谢 **Cursor AI** 提供的智能编程辅助
- 感谢 **Snowflake** 提供的数据存储服务
- 感谢 **Streamlit** 提供的Web界面框架

---

💡 **提示**: 这是一个演示项目，展示了如何结合Cursor AI和Snowflake来构建实用的数据应用。你可以根据自己的需求进行定制和扩展。
