from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# In-memory financial ledger state
FINANCE_STATE = {
    "balance": 2500.0,
    "transactions": [
        {"id": 1, "title": "Freelance Micro-task", "type": "Income", "amount": 3000.0, "category": "Work"},
        {"id": 2, "title": "Mobile Internet Bundle", "type": "Expense", "amount": 500.0, "category": "Utilities"}
    ]
}

@app.route('/')
def budget_home():
    # Calculate totals
    total_income = sum(t['amount'] for t in FINANCE_STATE['transactions'] if t['type'] == 'Income')
    total_expense = sum(t['amount'] for t in FINANCE_STATE['transactions'] if t['type'] == 'Expense')
    net_balance = total_income - total_expense

    tx_html = ""
    for t in FINANCE_STATE['transactions']:
        is_income = t['type'] == 'Income'
        color = "#10b981" if is_income else "#f43f5e"
        sign = "+" if is_income else "-"
        tx_html += f'''
        <div style="background: #1b2230; border-radius: 8px; padding: 12px; margin-bottom: 10px; border: 1px solid #2a3447; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-size: 14px; font-weight: bold; color: #fff;">{t['title']}</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">{t['category']} • <span style="color: {color};">{t['type']}</span></div>
            </div>
            <div style="font-size: 15px; font-weight: bold; color: {color};">{sign}KES {t['amount']:.2f}</div>
        </div>
        '''
    
    if not tx_html:
        tx_html = "<p style='color:#64748b; text-align:center;'>No transactions recorded yet.</p>"

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Budget & Finance Tracker</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; background: #121824; color: #fff; margin: 0; padding: 12px; }}
            h2 {{ color: #38bdf8; border-bottom: 2px solid #38bdf8; padding-bottom: 6px; }}
            .card {{ background: #1b2230; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #2a3447; }}
            .metric-box {{ display: flex; gap: 10px; margin-bottom: 15px; }}
            .metric {{ flex: 1; background: #1b2230; padding: 12px; border-radius: 8px; border: 1px solid #2a3447; text-align: center; }}
            input, select {{ width: 100%; padding: 10px; margin: 6px 0 12px 0; background: #121824; border: 1px solid #334155; color: #fff; border-radius: 6px; box-sizing: border-box; font-family: sans-serif; }}
            button {{ width: 100%; padding: 12px; background: #3b82f6; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }}
        </style>
    </head>
    <body>
        <h2>Personal Budget Tracker</h2>
        
        <!-- Balance Summary Cards -->
        <div class="metric-box">
            <div class="metric">
                <div style="font-size: 11px; color: #94a3b8;">Net Balance</div>
                <div style="font-size: 16px; font-weight: bold; color: #38bdf8; margin-top: 4px;">KES {net_balance:.2f}</div>
            </div>
            <div class="metric">
                <div style="font-size: 11px; color: #94a3b8;">Income</div>
                <div style="font-size: 15px; font-weight: bold; color: #10b981; margin-top: 4px;">+KES {total_income:.2f}</div>
            </div>
            <div class="metric">
                <div style="font-size: 11px; color: #94a3b8;">Expenses</div>
                <div style="font-size: 15px; font-weight: bold; color: #f43f5e; margin-top: 4px;">-KES {total_expense:.2f}</div>
            </div>
        </div>

        <div class="card">
            <h3 style="margin-top:0; color:#38bdf8; font-size:15px;">Add Transaction</h3>
            <form action="/add_tx" method="POST">
                <label style="font-size:12px; color:#94a3b8;">Description</label>
                <input type="text" name="title" placeholder="e.g., Grocery Shopping" required>
                
                <div style="display:flex; gap:10px;">
                    <div style="flex:1;">
                        <label style="font-size:12px; color:#94a3b8;">Type</label>
                        <select name="tx_type">
                            <option value="Income">Income</option>
                            <option value="Expense">Expense</option>
                        </select>
                    </div>
                    <div style="flex:1;">
                        <label style="font-size:12px; color:#94a3b8;">Amount (KES)</label>
                        <input type="number" step="0.01" name="amount" placeholder="0.00" required>
                    </div>
                </div>

                <label style="font-size:12px; color:#94a3b8;">Category</label>
                <select name="category">
                    <option value="Work">Work / Freelance</option>
                    <option value="Utilities">Utilities & Data</option>
                    <option value="Food">Food & Groceries</option>
                    <option value="Other">Other</option>
                </select>
                
                <button type="submit">+ Record Transaction</button>
            </form>
        </div>

        <h3 style="color: #38bdf8; margin-top: 20px;">Transaction Ledger</h3>
        {tx_html}
    </body>
    </html>
    '''

@app.route('/add_tx', methods=['POST'])
def add_transaction():
    title = request.form.get('title')
    tx_type = request.form.get('tx_type')
    amount = float(request.form.get('amount', 0))
    category = request.form.get('category')
    
    if title and amount > 0:
        new_id = len(FINANCE_STATE['transactions']) + 1
        FINANCE_STATE['transactions'].insert(0, {
            "id": new_id,
            "title": title,
            "type": tx_type,
            "amount": amount,
            "category": category
        })
    return redirect(url_for('budget_home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
