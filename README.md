# Python Sales Data Analysis Dashboard

An interactive sales analytics web application built with Python, Streamlit, Pandas, NumPy, Matplotlib and Seaborn.

## Features
- Revenue, units sold, record count and average revenue KPIs
- Filters for region, category and date range
- Product-wise and region-wise revenue charts
- Revenue trend chart
- Interactive sales table and CSV download
- Basic data cleaning and revenue calculation

## Project structure
```text
Python_Sales_Data_Analysis_Dashboard/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── sales.csv
```

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (optional but recommended).
4. Install dependencies:
   `pip install -r requirements.txt`
5. Start the app:
   `streamlit run app.py`
6. Open the local URL shown in the terminal (usually http://localhost:8501).

## Deploy free with Streamlit Community Cloud
1. Push this entire project folder to a public GitHub repository.
2. Sign in to Streamlit Community Cloud with GitHub.
3. Choose **Create app**.
4. Select your repository, branch `main`, and file path `app.py`.
5. Click **Deploy** and wait for the app to build.
6. Copy the public app URL.

## Dataset
`data/sales.csv` is a small sample dataset included so the project runs immediately. Replace it with your own sales data only if the column names remain: `date, product, category, quantity, unit_price, region`.
