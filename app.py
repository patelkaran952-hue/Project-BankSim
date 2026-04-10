# Creating DASHBOARD

from sqlalchemy import create_engine
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

engine = create_engine("mysql+mysqlconnector://root:theoutrun123@localhost/banksim")

df_banksim = pd.read_sql("SELECT * FROM transactions", engine)

st.title("💳 Fraud Detection Dashboard")


# KPIs

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Fraud Amount", int(df_banksim[df_banksim["fraud"] == 1]["amount"].sum())
)
col2.metric("Fraud Transactions", df_banksim[df_banksim["fraud"] == 1].shape[0])
col3.metric(
    "Avg Fraud Amount", int(df_banksim[df_banksim["fraud"] == 1]["amount"].mean())
)


## Chart 1

fraud_df = df_banksim[df_banksim["fraud"] == 1]
top_fraud_categories = fraud_df["category"].value_counts().nlargest(10).index
plot_data = fraud_df[fraud_df["category"].isin(top_fraud_categories)]

fig1 = plt.figure(figsize=(14, 7))
sns.set_style("darkgrid")
sns.set_palette("Reds_r")

ax = sns.countplot(x="category", data=plot_data, order=top_fraud_categories)

plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

total = len(plot_data)
for p in ax.patches:
    height = p.get_height()
    ax.annotate(
        f"{height} ({height / total:.1%})",
        (p.get_x() + p.get_width() / 2.0, height),
        ha="center",
        va="bottom",
        fontsize=11,
    )

plt.title("Fraud Count by Top 10 Categories", fontsize=16, weight="bold")
plt.xlabel("Transaction Category", fontsize=14)
plt.ylabel("Number of Fraudulent Transactions", fontsize=14)

plt.tight_layout()

st.pyplot(fig1)


# Chart 2

fig2 = plt.figure(figsize=(6, 4))
sns.set_style("whitegrid")
sns.set_palette("Reds_r")
ax2 = sns.countplot(x="gender", hue="fraud", data=fraud_df)

for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(
            f"{int(height)}",
            (p.get_x() + p.get_width() / 2.0, height),
            ha="center",
            va="bottom",
        )
plt.title("Fraud Distribution by Gender")
st.pyplot(fig2)


# Chart 3

query = """
select age, count(fraud) from transactions
where fraud = 1
group by age
order by count(fraud) desc; 
"""

fraud_age_df = pd.read_sql(query, engine)

top_frauds = fraud_age_df.head(6)

fig3 = plt.figure(figsize=(12, 6))
ax3 = sns.barplot(x="age", y="count(fraud)", data=top_frauds)

for p in ax.patches:
    height = p.get_height()
    ax.text(
        p.get_x() + p.get_width() / 2, height, f"{height:.0f}", ha="center", va="bottom"
    )

plt.title("Top frauds by age group")
plt.xticks(rotation=45)

st.pyplot(fig3)


# Chart 4
query = """
select category, count(fraud) as fraud_transactions, age from transactions
where fraud = 1
group by category, age
order by fraud_transactions desc;   
"""
fraud_cat_age_df = pd.read_sql(query, engine)

pivot_df = fraud_cat_age_df.pivot(
    index="category", columns="age", values="fraud_transactions"
)


fig4 = plt.figure(figsize=(12, 6))
sns.heatmap(pivot_df, annot=True, fmt=".0f", cmap="Reds")
plt.title("Fraud Transactions by Category and Age")

st.pyplot(fig4)


# Chart 5

query = """
select category, sum(amount) from transactions
where fraud = 1
group by category
order by sum(amount) desc;
"""

category_df = pd.read_sql(query, engine)

fig5 = plt.figure(figsize=(16, 6))
ax5 = sns.barplot(x="sum(amount)", y="category", data=category_df, palette="Reds_r")

for p in ax5.patches:
    width = p.get_width()
    ax5.annotate(
        f"{width:,.0f}",
        (width, p.get_y() + p.get_height() / 2),
        ha="left",
        va="center",
        xytext=(5, 0),
        textcoords="offset points",
    )

plt.title("Total Fraud Amount by Category")
plt.xlabel("Fraud Amount")
plt.ylabel("Category")

st.pyplot(fig5)


# Chart 6

query = """
SELECT category, 
       SUM(amount) AS total_fraud_amount, 
       COUNT(fraud) AS fraud_count
FROM transactions
WHERE fraud = 1
GROUP BY category
ORDER BY total_fraud_amount DESC;
"""

catfraud_df = pd.read_sql(query, engine)

sns.set_style("darkgrid")
plt.rcParams["font.size"] = 11

df_cat = pd.read_sql(query, engine)

df_cat = df_cat.sort_values(by="total_fraud_amount", ascending=False)

fig6, ax1 = plt.subplots(figsize=(14, 7))

bars = sns.barplot(
    x="category", y="total_fraud_amount", data=df_cat, palette="Reds_r", ax=ax1
)

ax1.set_title("Fraud Amount vs Fraud Count by Category", fontsize=16, weight="bold")
ax1.set_xlabel("Category", fontsize=12)
ax1.set_ylabel("Total Fraud Amount", fontsize=12)

ax1.set_xticklabels(ax1.get_xticklabels(), rotation=40, ha="right")

for i, v in enumerate(df_cat["total_fraud_amount"]):
    ax1.text(i, v, f"{v:,.0f}", ha="center", va="bottom", fontsize=9)

ax2 = ax1.twinx()
line = ax2.plot(df_cat["category"], df_cat["fraud_count"], marker="o", linewidth=2)

ax2.set_ylabel("Fraud Count", fontsize=12)

for i, v in enumerate(df_cat["fraud_count"]):
    ax2.text(i, v, str(v), ha="center", va="bottom", fontsize=9)

ax1.grid(axis="y", linestyle="--", alpha=0.6)
ax1.grid(axis="x", visible=False)

sns.despine(left=False, bottom=False)

plt.tight_layout()

st.pyplot(fig6)


# Chart 7

top = (
    df_banksim[df_banksim["fraud"] == 1]
    .groupby(["age", "category"])["amount"]
    .max()
    .reset_index()
)

top = top.sort_values(by="amount", ascending=False).head(10)

fig7 = plt.figure(figsize=(12, 6))

ax7 = sns.barplot(
    data=top,
    y=top["age"].astype(str) + " | " + top["category"],
    x="amount",
    palette="Reds_r",
)

for i, v in enumerate(top["amount"]):
    ax7.text(v + (v * 0.01), i, f"{v:,.0f}", va="center", fontsize=11)

plt.title("Top 10 Highest Fraud Amounts (Age + Category)", fontsize=15, weight="bold")
plt.xlabel("Max Fraud Amount")
plt.ylabel("Age | Category")

plt.tight_layout()

st.pyplot(fig7)


# Creating tabs

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    ["One", "Two", "Three", "Four", "Five", "Six", "Seven"]
)

with tab1:
    st.pyplot(fig1)

with tab2:
    st.pyplot(fig2)

with tab3:
    st.pyplot(fig3)

with tab4:
    st.pyplot(fig4)

with tab5:
    st.pyplot(fig5)

with tab6:
    st.pyplot(fig6)

with tab7:
    st.pyplot(fig7)
