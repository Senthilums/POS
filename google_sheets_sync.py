import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

# === Google Sheet Setup ===
SHEET_NAME = "Kongu POS Sales"
WORKSHEET_NAME = "Daily Sales"

def sync_csv_to_gsheet():
    # Auth
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # Open Sheet
    sheet = client.open(SHEET_NAME)
    worksheet = sheet.worksheet(WORKSHEET_NAME)

    # Read CSV
    with open("sales_data.csv", "r") as f:
        reader = csv.reader(f)
        data = list(reader)

    # Clear existing and update
    worksheet.clear()
    worksheet.update("A1", data)
    print("✅ Synced sales_data.csv to Google Sheet")

if __name__ == "__main__":
    sync_csv_to_gsheet()
