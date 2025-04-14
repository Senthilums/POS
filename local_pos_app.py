import tkinter as tk
from tkinter import ttk, messagebox
import pyqrcode
from PIL import Image, ImageTk
import os
import datetime
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
#from sync_to_sheets import sync_to_google_sheets



# === Predefined Product Rates ===
PRODUCT_RATES = {
    "Rice (per kg)": 50,
    "Husk (per kg)": 10,
    "Cattle Feed (per kg)": 25
}

# === Generate UPI QR Code ===
def generate_upi_qr(amount):
    upi_id = "yourupi@bank"  # Replace with your UPI ID
    name = "Kongu Modern Rice Mill"
    note = "POS Payment"
    url = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR&tn={note}"
    qr = pyqrcode.create(url)
    qr.png("upi_qr.png", scale=6)
    return "upi_qr.png"

# === Save to CSV (can later sync to Sheets) ===
def save_to_csv(product, weight, amount, phone):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("sales_data.csv", "a") as f:
        f.write(f"{timestamp},{product},{weight},{amount},{phone}\n")


# === Sync to google sheets ===
def sync_to_google_sheets(product, weight, amount, phone):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)

        spreadsheet_id = "1rNie02jspJlNTy-85JYkOkXMyEiXxDDQ0KsITL987RM"  # Replace this!
        sheet = client.open_by_key(spreadsheet_id).sheet1

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [timestamp, product, weight, amount, phone]

        # Optional: Add header if sheet is empty
        if not sheet.get_all_values():
            sheet.append_row(["Timestamp", "Product", "Weight", "Amount", "Phone"])

        sheet.append_row(row)
        print("✅ Synced to Google Sheets.")
    except Exception as e:
        print(f"❌ Google Sheets sync failed: {e}")


# === Main GUI ===
def run_app():
    def calculate_price():
        try:
            product = product_var.get()
            weight = float(weight_entry.get())
            phone = phone_entry.get()
            
            if not phone.isdigit() or len(phone) != 10:
                messagebox.showerror("Invalid Input", "Enter a valid 10-digit phone number")
                return

            rate = PRODUCT_RATES[product]
            amount = round(rate * weight, 2)
            amount_var.set(f"₹{amount}")
            save_to_csv(product, weight, amount, phone)
            print("🔄 Trying to sync data to Google Sheets...")
            sync_to_google_sheets(product, weight, amount, phone)
            
            # Show QR
            qr_path = generate_upi_qr(amount)
            qr_img = Image.open(qr_path)
            qr_img = qr_img.resize((200, 200))
            qr_tk = ImageTk.PhotoImage(qr_img)
            qr_label.configure(image=qr_tk)
            qr_label.image = qr_tk

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid weight")

    # GUI Window
    root = tk.Tk()
    root.title("Kongu POS - Rice Mill")
    root.geometry("400x550")

    ttk.Label(root, text="Select Product:").pack(pady=5)
    product_var = tk.StringVar(value=list(PRODUCT_RATES.keys())[0])
    product_menu = ttk.Combobox(root, textvariable=product_var, values=list(PRODUCT_RATES.keys()))
    product_menu.pack(pady=5)

    ttk.Label(root, text="Enter Weight (kg):").pack(pady=5)
    weight_entry = ttk.Entry(root)
    weight_entry.pack(pady=5)

    ttk.Label(root, text="Customer Phone Number:").pack(pady=5)
    phone_entry = ttk.Entry(root)
    phone_entry.pack(pady=5)

    ttk.Button(root, text="Generate Bill & QR", command=calculate_price).pack(pady=15)

    amount_var = tk.StringVar()
    ttk.Label(root, textvariable=amount_var, font=("Arial", 14)).pack(pady=10)

    qr_label = ttk.Label(root)
    qr_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_app()
