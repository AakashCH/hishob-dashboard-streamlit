import streamlit as st
import json
import datetime
from app.drive import get_monthly_transactions
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === Streamlit app for Hishob Dashboard ===
st.write("Loading credentials...")
try:
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["credentials_json"], scope)
    client = gspread.authorize(creds)
    st.success("Credentials loaded and authorized.")

    spreadsheet_name = st.secrets["spreadsheet_name"]
    sheet = client.open(spreadsheet_name)
    st.success(f"Sheet '{spreadsheet_name}' opened successfully.")
except Exception as e:
    st.error(f"Error loading Google Sheet: {e}")

st.set_page_config(page_title="Hishob Dashboard", layout="wide")

st.title("📊 Hishob - Personal Finance Dashboard")

# === Load secrets ===
creds_str = st.secrets["credentials_json"]
spreadsheet_name = st.secrets["spreadsheet_name"]

try:
    credentials = json.loads(creds_str)
except Exception as e:
    st.error("Error parsing credentials.")
    st.stop()

# === Current month ===
now = datetime.datetime.now()
month_tab = now.strftime("%b-%Y")

# === Load transactions ===
try:
    df = get_monthly_transactions(spreadsheet_name, credentials, month_tab)
    if df.empty:
        st.info("No active transactions for this month.")
    else:
        st.success(f"{len(df)} active transactions loaded.")
        st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Error fetching data: {str(e)}")
