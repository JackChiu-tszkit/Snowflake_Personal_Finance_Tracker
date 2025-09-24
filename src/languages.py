"""
Multi-language support for Personal Finance Tracker
支持多语言的个人理财助手
"""

# Language configurations
LANGUAGES = {
    'en': {
        'name': 'English',
        'flag': '🇺🇸',
        'app_title': '💰 Personal Finance Tracker',
        'navigation': {
            'overview': '📈 Financial Overview',
            'transactions': '💳 Transaction Records',
            'budgets': '📋 Budget Management',
            'investments': '📊 Investment Tracking',
            'add_record': '📝 Add Records'
        },
        'overview': {
            'title': '📈 Financial Overview',
            'monthly_income': 'Monthly Income',
            'monthly_expense': 'Monthly Expense',
            'net_income': 'Net Income',
            'investment_value': 'Investment Value',
            'spending_trends': '📊 Spending Trends',
            'expense_breakdown': '🥧 Expense Breakdown',
            'budget_status': '📋 Budget Status',
            'overspent': 'Overspent',
            'near_budget': 'Near Budget',
            'normal': 'Normal'
        },
        'transactions': {
            'title': '💳 Transaction Records',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'transaction_type': 'Transaction Type',
            'category': 'Category',
            'all': 'All',
            'income': 'Income',
            'expense': 'Expense',
            'total_transactions': 'Total Transactions',
            'total_amount': 'Total Amount',
            'average_amount': 'Average Amount',
            'no_records': 'No transaction records'
        },
        'budgets': {
            'title': '📋 Budget Management',
            'set_budget': 'Set Budget',
            'category': 'Category',
            'monthly_budget': 'Monthly Budget',
            'month_year': 'Month (YYYY-MM)',
            'set_budget_btn': 'Set Budget',
            'budget_status': 'Budget Status',
            'budget_alerts': '⚠️ Budget Alerts',
            'savings_recommendations': '💡 Savings Recommendations',
            'no_budget_data': 'No budget data'
        },
        'investments': {
            'title': '📊 Investment Tracking',
            'total_invested': 'Total Invested',
            'current_value': 'Current Value',
            'profit_loss': 'Profit/Loss',
            'return_rate': 'Return Rate',
            'portfolio_performance': '📈 Portfolio Performance',
            'asset_allocation': '🥧 Asset Allocation',
            'investment_recommendations': '💡 Investment Recommendations',
            'no_investment_data': 'No investment data'
        },
        'add_record': {
            'title': '📝 Add Records',
            'add_transaction': 'Add Transaction Record',
            'date': 'Date',
            'type': 'Type',
            'category': 'Category',
            'amount': 'Amount',
            'description': 'Description',
            'tags': 'Tags',
            'add_transaction_btn': 'Add Transaction',
            'add_investment': 'Add Investment Record',
            'investment_date': 'Investment Date',
            'investment_type': 'Investment Type',
            'symbol': 'Symbol/Code',
            'name': 'Name',
            'quantity': 'Quantity',
            'buy_price': 'Buy Price',
            'current_price': 'Current Price',
            'add_investment_btn': 'Add Investment'
        },
        'categories': {
            'food': 'Food',
            'transport': 'Transport',
            'shopping': 'Shopping',
            'entertainment': 'Entertainment',
            'health': 'Health',
            'education': 'Education',
            'social': 'Social',
            'salary': 'Salary'
        },
        'investment_types': {
            'stock': 'Stock',
            'fund': 'Fund',
            'crypto': 'Cryptocurrency',
            'bond': 'Bond'
        },
        'messages': {
            'success': 'Success',
            'error': 'Error',
            'transaction_added': 'Transaction record added successfully!',
            'transaction_failed': 'Failed to add transaction record!',
            'investment_added': 'Investment record added successfully!',
            'investment_failed': 'Failed to add investment record!',
            'budget_set': 'Budget set successfully',
            'budget_failed': 'Failed to set budget'
        }
    },
    
    'no': {
        'name': 'Norsk',
        'flag': '🇳🇴',
        'app_title': '💰 Personlig Finans Tracker',
        'navigation': {
            'overview': '📈 Finansiell Oversikt',
            'transactions': '💳 Transaksjonsposter',
            'budgets': '📋 Budsjettstyring',
            'investments': '📊 Investeringssporing',
            'add_record': '📝 Legg til Poster'
        },
        'overview': {
            'title': '📈 Finansiell Oversikt',
            'monthly_income': 'Månedlig Inntekt',
            'monthly_expense': 'Månedlig Utgift',
            'net_income': 'Netto Inntekt',
            'investment_value': 'Investeringsverdi',
            'spending_trends': '📊 Utgiftstrender',
            'expense_breakdown': '🥧 Utgiftsfordeling',
            'budget_status': '📋 Budsjettstatus',
            'overspent': 'Overskredet',
            'near_budget': 'Nær Budsjett',
            'normal': 'Normal'
        },
        'transactions': {
            'title': '💳 Transaksjonsposter',
            'start_date': 'Startdato',
            'end_date': 'Sluttdato',
            'transaction_type': 'Transaksjonstype',
            'category': 'Kategori',
            'all': 'Alle',
            'income': 'Inntekt',
            'expense': 'Utgift',
            'total_transactions': 'Totalt Antall Transaksjoner',
            'total_amount': 'Total Beløp',
            'average_amount': 'Gjennomsnittlig Beløp',
            'no_records': 'Ingen transaksjonsposter'
        },
        'budgets': {
            'title': '📋 Budsjettstyring',
            'set_budget': 'Sett Budsjett',
            'category': 'Kategori',
            'monthly_budget': 'Månedlig Budsjett',
            'month_year': 'Måned (YYYY-MM)',
            'set_budget_btn': 'Sett Budsjett',
            'budget_status': 'Budsjettstatus',
            'budget_alerts': '⚠️ Budsjettvarsler',
            'savings_recommendations': '💡 Sparingsanbefalinger',
            'no_budget_data': 'Ingen budsjettdata'
        },
        'investments': {
            'title': '📊 Investeringssporing',
            'total_invested': 'Totalt Investert',
            'current_value': 'Nåværende Verdi',
            'profit_loss': 'Gevinst/Tap',
            'return_rate': 'Avkastning',
            'portfolio_performance': '📈 Porteføljeytelse',
            'asset_allocation': '🥧 Aktivafordeling',
            'investment_recommendations': '💡 Investeringsanbefalinger',
            'no_investment_data': 'Ingen investeringsdata'
        },
        'add_record': {
            'title': '📝 Legg til Poster',
            'add_transaction': 'Legg til Transaksjonspost',
            'date': 'Dato',
            'type': 'Type',
            'category': 'Kategori',
            'amount': 'Beløp',
            'description': 'Beskrivelse',
            'tags': 'Etiketter',
            'add_transaction_btn': 'Legg til Transaksjon',
            'add_investment': 'Legg til Investeringspost',
            'investment_date': 'Investeringsdato',
            'investment_type': 'Investerings type',
            'symbol': 'Symbol/Kode',
            'name': 'Navn',
            'quantity': 'Antall',
            'buy_price': 'Kjøpspris',
            'current_price': 'Nåværende Pris',
            'add_investment_btn': 'Legg til Investering'
        },
        'categories': {
            'food': 'Mat',
            'transport': 'Transport',
            'shopping': 'Shopping',
            'entertainment': 'Underholdning',
            'health': 'Helse',
            'education': 'Utdanning',
            'social': 'Sosialt',
            'salary': 'Lønn'
        },
        'investment_types': {
            'stock': 'Aksje',
            'fund': 'Fond',
            'crypto': 'Kryptovaluta',
            'bond': 'Obligasjon'
        },
        'messages': {
            'success': 'Suksess',
            'error': 'Feil',
            'transaction_added': 'Transaksjonspost lagt til!',
            'transaction_failed': 'Kunne ikke legge til transaksjonspost!',
            'investment_added': 'Investeringspost lagt til!',
            'investment_failed': 'Kunne ikke legge til investeringspost!',
            'budget_set': 'Budsjett satt',
            'budget_failed': 'Kunne ikke sette budsjett'
        }
    }
}

def get_text(lang, section, key):
    """Get localized text"""
    if lang in LANGUAGES and section in LANGUAGES[lang] and key in LANGUAGES[lang][section]:
        return LANGUAGES[lang][section][key]
    # Fallback to English
    if 'en' in LANGUAGES and section in LANGUAGES['en'] and key in LANGUAGES['en'][section]:
        return LANGUAGES['en'][section][key]
    return key

def get_language_list():
    """Get list of available languages"""
    return [(code, f"{LANGUAGES[code]['flag']} {LANGUAGES[code]['name']}") for code in LANGUAGES.keys()]
