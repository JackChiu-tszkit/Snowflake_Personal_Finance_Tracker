# 💰 Personal Finance Tracker

An intelligent personal finance management system built with **Cursor AI** and **Snowflake**, designed to help you track expenses, manage budgets, monitor investments, and make smarter financial decisions.

## 🌟 Key Features

### 📈 Financial Overview
- Real-time overview of monthly income and expenses
- Income and expense trend analysis over the past 6 months
- Expense distribution visualization using pie charts
- Budget utilization tracking and monitoring

### 💳 Transaction Management
- Add and manage income and expense records
- Filter transactions by date, type, and category
- Search, query, and analyze transaction history
- Support for transaction tags and categorization

### 📋 Budget Management
- Set monthly budgets for different spending categories
- Monitor budget utilization in real time
- Receive alerts when spending exceeds budget limits
- Generate intelligent savings recommendations

### 📊 Investment Tracking
- Track investments in stocks, funds, cryptocurrencies, and other assets
- Calculate investment profits and losses
- Analyze investment portfolio performance
- Visualize asset allocation
- Generate AI-powered investment insights and recommendations

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Database:** Snowflake
- **Backend:** Python
- **Data Visualization:** Plotly
- **AI-Assisted Development:** Cursor AI

## 📦 Installation and Configuration

### 1. Clone the Repository

```bash
git clone <repository-url>
cd snowflake_v1
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Snowflake Connection

Copy the `.env.example` file to `.env` and enter your Snowflake connection credentials:

```bash
cp .env.example .env
```

Edit the `.env` file:

```env
SNOWFLAKE_ACCOUNT=your_account.snowflakecomputing.com
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=FINANCE_DB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ACCOUNTADMIN
```

**Security Note:** Keep your `.env` file private and exclude it from version control. For production environments, use a dedicated Snowflake role with minimum required permissions instead of `ACCOUNTADMIN`.

### 4. Initialize the Database

The application automatically creates the required database tables during its initial startup.

## 🚀 Running the Application

Start the Streamlit application using:

```bash
streamlit run src/dashboard.py
```

The application will automatically open in your default web browser.

**Default URL:** http://localhost:8501

## 📊 Database Schema

### 1. transactions (Transaction Records)

| Column | Description |
|---|---|
| `id` | Primary key |
| `date` | Transaction date |
| `type` | Transaction type (income/expense) |
| `category` | Transaction category |
| `amount` | Transaction amount |
| `description` | Transaction description |
| `tags` | Transaction tags |
| `created_at` | Record creation timestamp |

### 2. budgets (Budget Management)

| Column | Description |
|---|---|
| `id` | Primary key |
| `category` | Budget category |
| `monthly_budget` | Monthly budget amount |
| `current_spent` | Current spending amount |
| `month_year` | Budget month and year |
| `created_at` | Record creation timestamp |

### 3. investments (Investment Records)

| Column | Description |
|---|---|
| `id` | Primary key |
| `date` | Investment purchase date |
| `type` | Investment type (stock/fund/crypto/bond) |
| `symbol` | Asset ticker or symbol |
| `name` | Investment name |
| `quantity` | Number of units or shares |
| `price` | Purchase price per unit |
| `amount` | Total investment amount |
| `current_price` | Current market price |
| `current_value` | Current market value |
| `created_at` | Record creation timestamp |

## 🎯 User Guide

### 1. Getting Started

1. Configure your Snowflake connection credentials.
2. Launch the Streamlit application.
3. Navigate to the **Add Transaction** page.
4. Add sample income and expense records to explore the available features.

### 2. Daily Usage

1. **Record Transactions:** Track daily income and expenses through the Add Transaction page.
2. **Manage Budgets:** Set and monitor monthly spending limits for different categories.
3. **Track Investments:** Record investment purchases and periodically update market prices.
4. **Analyze Finances:** Use the Financial Overview dashboard to review financial performance, spending patterns, and budget utilization.

### 3. Data Import

You can import initial financial records using the sample CSV files provided in the `data/` directory.

## 🔧 Development Guide

### Project Structure

```text
snowflake_v1/
├── data/                       # Sample datasets
│   ├── sample_transactions.csv
│   ├── sample_budgets.csv
│   └── sample_investments.csv
├── src/                        # Application source code
│   ├── snowflake_connector.py   # Snowflake database connector
│   ├── transaction_manager.py  # Transaction management
│   ├── budget_analyzer.py      # Budget analysis
│   ├── investment_tracker.py   # Investment tracking
│   └── dashboard.py            # Streamlit dashboard
├── config.py                   # Application configuration
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

### Future Enhancements

The application can be extended with additional capabilities, including:

- Advanced financial analytics and interactive visualizations
- Data export to CSV, Excel, and JSON formats
- Financial goal setting and progress tracking
- Integration with additional financial market data providers
- AI-powered transaction categorization and expense analysis
- Automated financial reports and personalized recommendations
- Support for multiple currencies and exchange rate conversion
- Integration with AI agents for natural language financial queries

## 🤝 Contributing

Contributions are welcome!

Feel free to submit an **Issue** to report bugs or suggest new features, or open a **Pull Request** to improve the project.

## 📄 License

This project is licensed under the **MIT License**.
