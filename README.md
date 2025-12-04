# 🧾 Expense Tracker Application  
L7 Informatics Internship — Python Programming Round

This is a Flask + SQLite based **Expense Tracking System** that allows users to record daily expenses, categorize them, set monthly budgets, and receive alerts upon reaching or exceeding their budget limits.  
The system also provides **detailed monthly reports** comparing spending vs. budgets.

This project fully meets all requirements of the assignment.

---

# 🚀 Features

### ✅ Core Features
- Add users  
- Log daily expenses  
- Categorize expenses (Food, Travel, Entertainment, etc.)  
- Set monthly budgets per category  
- Alert when **90% of budget is reached**  
- Alert when **budget is exceeded**  
- Generate monthly reports  
- Compare spending vs. budget  
- Clean web interface using Bootstrap  

### 🟦 Extra Credit Features
- Email alerts (optional, automatically disabled if no email config provided)  
- Support for different budgets for different months  

---

# 🛠️ Tech Stack

- **Python 3.10+**
- **Flask**
- **SQLite3**
- **SQLAlchemy ORM**
- **HTML + Bootstrap**
- **Docker (optional)**

---

# 📂 Folder Structure

expense_tracker/
│ app.py
│ config.py
│ database.py
│ models.py
│ utils.py
│ requirements.txt
│ Dockerfile
│ .env
│
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── add_expense.html
│ ├── budget.html
│ ├── reports.html
│
└── static/
└── style.css


---

# ⚙️ Installation & Running the Application

## 1. Clone the Repository


git clone https://github.com/
<your-username>/expense-tracker.git
cd expense-tracker


## 2. Create Virtual Environment

### Windows:


python -m venv venv
venv\Scripts\activate


### Mac/Linux:


python3 -m venv venv
source venv/bin/activate


## 3. Install Dependencies


pip install -r requirements.txt


## 4. Create `.env` File
Create a file named `.env` in the project root and add:



SECRET_KEY=<your_secret_key_here>
MAIL_SERVER=
MAIL_PORT=
MAIL_USERNAME=
MAIL_PASSWORD=


*(Email config optional — app works even if left blank.)*

## 5. Run the Application


python app.py


Your app will start at:

👉 http://127.0.0.1:5000/

---

# 🐋 Running with Docker (Optional)

## Build the image:


docker build -t expense-app .


## Run the container:


docker run -p 5000:5000 expense-app


Open:  
👉 http://127.0.0.1:5000/

---

# 🧪 Test Steps (Mandatory for 1 Mark in Evaluation)

These steps validate all features:

### 1️⃣ Create a user  
- Enter Name and Email → Add User

### 2️⃣ Set a budget  
Go to **Set Budget**  
Enter:  
- Category: Food  
- Month: 5  
- Year: 2025  
- Amount: 2000  

### 3️⃣ Add an expense — within budget  
Add:  
- Food = 1500  
- Date: 2025-05-05  
✔ No alert should appear

### 4️⃣ Add expense — exceed budget  
Add:  
- Food = 600  
- Date: 2025-05-10  
✔ Expect: **Budget Exceeded alert**

### 5️⃣ Verify Report  
Open:  


http://127.0.0.1:5000/reports/
<user_id>/2025/5


You should see:
- Total spending = **2100**
- Budget = **2000**

---

# 🗄️ Database Schema (Using SQLAlchemy ORM)

### **User**
| Column | Type |
|--------|------|
| id | Integer |
| name | String |
| email | String (unique) |

### **Expense**
| Column | Type |
|--------|------|
| id | Integer |
| user_id | ForeignKey |
| category | String |
| amount | Float |
| date | Date |

### **Budget**
| Column | Type |
|--------|------|
| id | Integer |
| user_id | ForeignKey |
| category | String |
| month | Integer |
| year | Integer |
| amount | Float |

---

# 📘 SQL Queries (Required for SQL/ORM Marks)

### Total spending for a month:
```sql
SELECT SUM(amount)
FROM expense
WHERE user_id = ?
  AND strftime('%m', date) = ?
  AND strftime('%Y', date) = ?;

Category-wise spending:
SELECT category, SUM(amount)
FROM expense
WHERE user_id = ?
GROUP BY category;