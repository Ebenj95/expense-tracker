import streamlit as st
import pandas as pd
from analytics import category_chart, monthly_chart

st.title("Expense Tracker 📊")

st.write("Welcome to your expense tracker!")
import streamlit as st
import sqlite3
from datetime import datetime


# Input fields
amount = st.number_input("Amount", min_value=0.0)

category = st.selectbox(
    "Category",
    ["Food", "Travel", "Shopping", "Bills", "Entertainment"]
)

description = st.text_input("Description")

date = st.date_input("Date")

# Button
if st.button("Add Expense"):

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses (amount, category, description, date)
    VALUES (?, ?, ?, ?)
    """, (amount, category, description, str(date)))

    conn.commit()
    conn.close()

    st.success("Expense Added Successfully!")

import pandas as pd

st.subheader("Saved Expenses")

conn = sqlite3.connect("expenses.db")

df = pd.read_sql_query(
    "SELECT * FROM expenses",
    conn
)

conn.close()

st.dataframe(df)
st.subheader("Remove Expense")

# Create readable options
expense_options = df.apply(
    lambda row: f"ID {row['id']} | ₹{row['amount']} | {row['category']} | {row['description']}",
    axis=1
)

selected_expense = st.selectbox(
    "Select Expense to Remove",
    expense_options
)

if st.button("Delete Expense", type="primary"):

    # Extract ID from selected text
    expense_id = int(selected_expense.split("|")[0].replace("ID", "").strip())

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    st.success("Expense Deleted Successfully!")

    st.rerun()
st.subheader("Expense Breakdown")

fig = category_chart(df)

st.pyplot(fig)

st.subheader("Monthly Spending Trend")

fig2 = monthly_chart(df)

st.pyplot(fig2)

total = df["amount"].sum()

st.metric("Total Spending", f"₹{total}")