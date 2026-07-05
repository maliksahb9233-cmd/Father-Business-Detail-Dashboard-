import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database connection
conn = sqlite3.connect("farm_business.db")
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS farmers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    village TEXT,
    crop TEXT,
    amount REAL
)
""")

conn.commit()

# Functions
def add_farmer():
    name = name_entry.get()
    phone = phone_entry.get()
    village = village_entry.get()
    crop = crop_entry.get()
    amount = amount_entry.get()

    if name == "":
        messagebox.showerror("Error", "Enter farmer name")
        return

    cur.execute("""
    INSERT INTO farmers(name, phone, village, crop, amount)
    VALUES (?, ?, ?, ?, ?)
    """, (name, phone, village, crop, amount))

    conn.commit()
    load_data()
    clear_fields()

def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    village_entry.delete(0, tk.END)
    crop_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

def load_data():
    for row in tree.get_children():
        tree.delete(row)

    cur.execute("SELECT * FROM farmers")
    rows = cur.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

# GUI
root = tk.Tk()
root.title("Farmer Management System")
root.geometry("900x600")

tk.Label(root, text="Farmer Name").pack()
name_entry = tk.Entry(root, width=40)
name_entry.pack()

tk.Label(root, text="Phone").pack()
phone_entry = tk.Entry(root, width=40)
phone_entry.pack()

tk.Label(root, text="Village").pack()
village_entry = tk.Entry(root, width=40)
village_entry.pack()

tk.Label(root, text="Crop").pack()
crop_entry = tk.Entry(root, width=40)
crop_entry.pack()

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root, width=40)
amount_entry.pack()

tk.Button(root, text="Add Farmer", command=add_farmer).pack(pady=10)

tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Phone", "Village", "Crop", "Amount"),
    show="headings"
)

for col in ("ID", "Name", "Phone", "Village", "Crop", "Amount"):
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True)

load_data()

root.mainloop()

conn.close()