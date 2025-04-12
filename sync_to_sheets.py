import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === Setup Google Sheets Credentials ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# === Open your Google Sheet ===
spreadsheet_id = "1rNie02jspJlNTy-85JYkOkXMyEiXxDDQ0KsITL987RM"  # Replace with your real ID
sheet = client.open_by_key(spreadsheet_id).sheet1  # Access the first sheet (Sales)

# === Optional: Add headers if sheet is empty ===
if not sheet.get_all_values():
    sheet.append_row(["Timestamp", "Product", "Weight", "Amount", "Phone"])

# === Read local sales CSV and append to Google Sheet ===
with open("sales_data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        sheet.append_row(row)

print("✅ Sales data synced to Google Sheets successfully!")
