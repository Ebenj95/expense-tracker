import matplotlib.pyplot as plt
import pandas as pd

def category_chart(df):

    category_total = df.groupby("category")["amount"].sum()

    fig, ax = plt.subplots()

    ax.pie(
        category_total,
        labels=category_total.index,
        autopct='%1.1f%%'
    )

    return fig

def monthly_chart(df):

    df["date"] = pd.to_datetime(df["date"])

    monthly = df.groupby(
        df["date"].dt.month
    )["amount"].sum()

    fig, ax = plt.subplots()

    ax.plot(monthly.index, monthly.values)

    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")

    return fig