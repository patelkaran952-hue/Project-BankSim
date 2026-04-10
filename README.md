🏦 BankSim Fraud Detection & Analytics Dashboard

📌 Project Overview

This project analyzes synthetic banking transaction data to detect fraudulent activities and generate actionable insights. 
The dataset is based on the BankSim simulator, which mimics real-world banking transactions while preserving privacy .

The project combines:

Python (Data Analysis & Visualization)
MySQL (Data Storage & Querying)
Streamlit (Interactive Dashboard)

🎯 Objectives

Analyze transaction patterns across customers, categories, and age groups
Identify high-risk fraud segments
Build an interactive dashboard for real-time insights
Practice end-to-end data pipeline (SQL → Python → Visualization)
📂 Dataset
Source: BankSim Synthetic Dataset
~594,000 transactions
Includes:
Customer demographics (age, gender)
Transaction details (amount, category, step)
Fraud label (0 = normal, 1 = fraud)

👉 The dataset simulates real banking behavior with injected fraud scenarios

⚙️ Tech Stack

Python (Pandas, NumPy, Matplotlib, Seaborn)
MySQL (Data querying & aggregation)
Streamlit (Dashboard UI)
Jupyter Notebook (EDA & experimentation)

🔍 Key Features

📊 1. Data Analysis
Fraud vs non-fraud distribution
Transaction amount analysis (log scale)
Category-wise fraud trends
Age-based fraud behavior

📈 2. Visualizations
Bar charts (fraud amount by category)
Heatmap (fraud transactions by category and age)
Bar and Line combo chart (fraud amount vs fraud count by category)
Annotated charts for better insights

🖥️ 3. Streamlit Dashboard

Interactive tabs:
Category Analysis
Age Analysis
Distribution Insights
Clean UI with multiple plots
Real-time filtering and exploration

🗄️ Database Integration (MySQL)

Data stored in MySQL table (transactions)
SQL queries used for:
Aggregation (SUM, COUNT)
Grouping (category, age)
Filtering (fraud = 1)

Example:

SELECT category, 
       SUM(amount) AS total_fraud_amount
FROM transactions
WHERE fraud = 1
GROUP BY category;


🚀 How to Run the Project

1️⃣ Clone the Repository
   git clone https://github.com/patelkaran952-hue/Project-BankSim.git
   cd Project-BankSim

2️⃣ Install Dependencies
   pip install -r requirements.txt

3️⃣ Run Streamlit App
   streamlit run app.py

👉 You will see:

📊 Sample Insights

Certain categories contribute disproportionately to fraud
Fraud transactions tend to occur in specific age groups
High-value transactions are more likely to be fraudulent
Fraud distribution is highly imbalanced (very few fraud cases)

📌 Project Structure (Typical)

Project-BankSim/
│
├── app.py                 # Streamlit dashboard
├── notebooks/             # Jupyter notebooks (EDA)
├── data/                  # Dataset files
├── sql/                   # SQL queries
├── images/                # Visualizations/screenshots
├── requirements.txt
└── README.md

🧠 Learnings
End-to-end data analytics workflow
SQL + Python integration
Data visualization best practices
Dashboard development using Streamlit
Understanding fraud detection patterns

👤 Author
Karan Patel
