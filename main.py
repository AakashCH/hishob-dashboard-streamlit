import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === AUTH & GOOGLE SHEETS SETUP ===
@st.cache_resource
def load_gsheet():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            st.secrets["credentials_json"], scope
        )
        client = gspread.authorize(creds)
        sheet = client.open(st.secrets["spreadsheet_name"])
        return sheet
    except Exception as e:
        st.error("❌ Failed to connect to Google Sheets.")
        st.stop()

# === LOAD DATA FOR CURRENT MONTH ===
def load_current_month_data(sheet):
    tab = datetime.datetime.now().strftime("%b-%Y")
    try:
        worksheet = sheet.worksheet(tab)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception:
        st.warning(f"No data found for tab: {tab}")
        return pd.DataFrame()

# === DASHBOARD ===
def show_summary(df):
    st.subheader("📊 Hishob - Personal Finance Dashboard")

    if df.empty:
        st.info("No transactions found.")
        return

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    # Filter active entries only
    df = df[df["active"] == "Y"]

    total_spent = df[df["entry_type"] == "debit"]["amount"].sum()
    total_income = df[df["entry_type"] == "credit"]["amount"].sum()

    st.metric("Total Spent", f"₹{total_spent:,.2f}")
    st.metric("Total Income", f"₹{total_income:,.2f}")

    # Category-wise summary
    category_summary = df.groupby("category", dropna=False)["amount"].sum().sort_values(ascending=False)
    st.bar_chart(category_summary)

    # Show latest transactions
    st.subheader("🧾 Latest Transactions")
    st.dataframe(df.sort_values("datetime", ascending=False).head(10), use_container_width=True)

# === MAIN ===
def main():
    st.title("💸 Hishob Dashboard")

    sheet = load_gsheet()
    df = load_current_month_data(sheet)

    show_summary(df)

if __name__ == "__main__":
    main()
