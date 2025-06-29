import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def get_gsheet_client(credentials: dict):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope) # type: ignore
    if not creds or creds.invalid:
        raise ValueError("Invalid credentials provided.")
    return gspread.authorize(creds) # type: ignore

def get_monthly_transactions(sheet_name, credentials, month_tab):
    client = get_gsheet_client(credentials)
    sheet = client.open(sheet_name)
    worksheet = sheet.worksheet(month_tab)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    df = df[df["active"] == "Y"]
    return df
