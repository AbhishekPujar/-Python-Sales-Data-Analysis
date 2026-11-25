import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📊", layout="wide")

st.title("📊 Python Sales Data Analysis Dashboard")
st.write("Explore sales performance, products, categories and regions.")

DATA_FILE = Path(__file__).parent / "data" / "sales.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.dropna(subset=["date", "product", "category", "quantity", "unit_price", "region"])
    df = df[(df["quantity"] >= 0) & (df["unit_price"] >= 0)].copy()
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df

df = load_data()

with st.sidebar:
    st.header("Filter sales")
    regions = st.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
    categories = st.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

filtered = df[df["region"].isin(regions) & df["category"].isin(categories)].copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered = filtered[filtered["date"].between(start, end)]

if filtered.empty:
    st.warning("No sales match the selected filters. Change the filters in the sidebar.")
    st.stop()

total_revenue = filtered["revenue"].sum()
units_sold = int(filtered["quantity"].sum())
orders = len(filtered)
average_order = total_revenue / orders if orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("Units Sold", f"{units_sold:,}")
c3.metric("Sales Records", f"{orders:,}")
c4.metric("Average Revenue / Record", f"₹{average_order:,.0f}")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Revenue by product")
    product_sales = filtered.groupby("product", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=product_sales, x="revenue", y="product", ax=ax)
    ax.set_xlabel("Revenue (₹)")
    ax.set_ylabel("")
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Revenue by region")
    region_sales = filtered.groupby("region", as_index=False)["revenue"].sum()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.pie(region_sales["revenue"], labels=region_sales["region"], autopct="%1.1f%%", startangle=90)
    ax.set_title("Regional revenue share")
    st.pyplot(fig)
    plt.close(fig)

st.subheader("Revenue over time")
daily = filtered.groupby("date", as_index=False)["revenue"].sum().sort_values("date")
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(daily["date"], daily["revenue"], marker="o")
ax.set_xlabel("Date")
ax.set_ylabel("Revenue (₹)")
ax.grid(True, alpha=0.3)
fig.autofmt_xdate()
st.pyplot(fig)
plt.close(fig)

st.subheader("Sales data")
display_df = filtered.sort_values("date", ascending=False).copy()
st.dataframe(display_df, use_container_width=True)

csv = display_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered sales as CSV", csv, "filtered_sales.csv", "text/csv")

st.caption("Built with Python, Streamlit, Pandas, NumPy, Matplotlib and Seaborn.")
