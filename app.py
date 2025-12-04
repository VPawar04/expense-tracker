from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from database import db
from models import User, Expense, Budget
from datetime import datetime
from sqlalchemy import func
from utils import send_email

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create DB tables
with app.app_context():
    db.create_all()

# ==================== ROUTES ====================

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/create_user', methods=['POST'])
def create_user():
    name = request.form['name']
    email = request.form['email']
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    flash("User created successfully!", "success")
    return redirect(url_for('index'))


@app.route('/add_expense_form/<int:user_id>')
def add_expense_form(user_id):
    return render_template('add_expense.html', user_id=user_id)


@app.route('/add_expense', methods=['POST'])
def add_expense():
    user_id = int(request.form['user_id'])
    category = request.form['category']
    amount = float(request.form['amount'])
    date = datetime.strptime(request.form['date'], '%Y-%m-%d')

    # Save expense
    exp = Expense(
        user_id=user_id,
        category=category,
        amount=amount,
        date=date
    )
    db.session.add(exp)
    db.session.commit()

    # Budget alert logic
    month = date.month
    year = date.year

    spent = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user_id,
        Expense.category == category,
        func.strftime('%m', Expense.date) == f"{month:02d}",
        func.strftime('%Y', Expense.date) == str(year)
    ).scalar() or 0.0

    budget = Budget.query.filter_by(
        user_id=user_id,
        category=category,
        month=month,
        year=year
    ).first()

    if budget:
        if spent > budget.amount:
            flash(f"⚠️ Exceeded budget for {category}!", "danger")
            send_email("test@gmail.com", "Budget Exceeded", f"Budget exceeded for {category}")
        elif spent >= 0.9 * budget.amount:
            flash(f"⚠️ 90% budget used for {category}", "warning")

    return redirect(url_for('index'))


@app.route('/budget_form/<int:user_id>')
def budget_form(user_id):
    return render_template('budget.html', user_id=user_id)


@app.route('/set_budget', methods=['POST'])
def set_budget():
    user_id = int(request.form['user_id'])
    category = request.form['category']
    month = int(request.form['month'])
    year = int(request.form['year'])
    amount = float(request.form['amount'])

    budget = Budget.query.filter_by(
        user_id=user_id,
        category=category,
        month=month,
        year=year
    ).first()

    if budget:
        budget.amount = amount
    else:
        budget = Budget(
            user_id=user_id,
            category=category,
            month=month,
            year=year,
            amount=amount
        )
        db.session.add(budget)

    db.session.commit()
    flash("Budget saved!", "success")
    return redirect(url_for('index'))


@app.route('/reports/<int:user_id>/<int:year>/<int:month>')
def reports(user_id, year, month):
    total = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user_id,
        func.strftime('%m', Expense.date) == f"{month:02d}",
        func.strftime('%Y', Expense.date) == str(year)
    ).scalar() or 0.0

    breakdown = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == user_id,
        func.strftime('%m', Expense.date) == f"{month:02d}",
        func.strftime('%Y', Expense.date) == str(year)
    ).group_by(Expense.category).all()

    budgets = Budget.query.filter_by(user_id=user_id, month=month, year=year).all()

    return render_template(
        'reports.html',
        total=total,
        breakdown=breakdown,
        budgets=budgets,
        month=month,
        year=year
    )


# ==================== NEW ROUTE: Overall Report ====================
@app.route('/overall_report/<int:user_id>')
def overall_report(user_id):
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        flash("User not found!", "danger")
        return redirect(url_for('index'))

    # Total spending (all time)
    total_spent = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user_id
    ).scalar() or 0.0

    # Category-wise total spending (all time)
    category_spending = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == user_id
    ).group_by(Expense.category).all()

    # All budgets set by user
    budgets = Budget.query.filter_by(user_id=user_id).all()

    # Check months where budget was exceeded
    exceeded_months = []
    for b in budgets:
        spent = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == user_id,
            Expense.category == b.category,
            func.strftime('%m', Expense.date) == f"{b.month:02d}",
            func.strftime('%Y', Expense.date) == str(b.year)
        ).scalar() or 0.0

        if spent > b.amount:
            exceeded_months.append({
                "category": b.category,
                "month": b.month,
                "year": b.year,
                "spent": spent,
                "budget": b.amount
            })

    return render_template(
        'overall_report.html',
        user=user,
        total_spent=total_spent,
        category_spending=category_spending,
        exceeded_months=exceeded_months
    )


if __name__ == "__main__":
    app.run(debug=True)
