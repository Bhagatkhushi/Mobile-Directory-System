import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

FILE_NAME = "contacts.csv"

# first time run pe file create ho jaye
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID","Name","Phone","Email","CUIN","Address"])


# -----------------------
# next id generate karne ke liye
# -----------------------
def get_next_id():
    with open(FILE_NAME, "r") as file:
        data = list(csv.reader(file))

        # agar file empty hai
        if len(data) <= 1:
            return 1
        else:
            last_id = int(data[-1][0])
            return last_id + 1


# -----------------------
# new contact add
# -----------------------
def add_contact():

    # input fields se data le rahe
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    cuin = cuin_entry.get()
    address = address_entry.get()

    # basic validation
    if name == "" or phone == "" or email == "" or cuin == "" or address == "":
        messagebox.showerror("Error", "All fields required")
        return

    # phone number check (simple wala)
    if not phone.isdigit():
        messagebox.showerror("Error", "Phone must be numeric")
        return

    contact_id = get_next_id()

    # file me save kar rahe
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([contact_id, name, phone, email, cuin, address])

    messagebox.showinfo("Success", "Contact Saved 👍")

    # fields clear kar dete hai
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    cuin_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

    # refresh list
    view_contacts()


# -----------------------
# contacts show karne ke liye
# -----------------------
def view_contacts():

    # pehle old data clear
    for row in tree.get_children():
        tree.delete(row)

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)  # header skip

        for row in reader:
            tree.insert("", tk.END, values=row)


# -----------------------
# search by name
# -----------------------
def search_contact():

    keyword = search_entry.get().lower()

    # table clear
    for row in tree.get_children():
        tree.delete(row)

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if keyword in row[1].lower():
                tree.insert("", tk.END, values=row)


# -----------------------
# delete selected contact
# -----------------------
def delete_contact():

    selected = tree.selection()

    if not selected:
        messagebox.showerror("Error", "Select contact first")
        return

    values = tree.item(selected)["values"]
    contact_id = values[0]

    # saara data read karte hai
    with open(FILE_NAME, "r") as file:
        rows = list(csv.reader(file))

    # overwrite file except deleted one
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)

        for row in rows:
            if row and row[0] != str(contact_id):
                writer.writerow(row)

    messagebox.showinfo("Deleted", "Contact removed")

    view_contacts()


# -----------------------
# pdf export (simple table)
# -----------------------
def export_pdf():

    with open(FILE_NAME, "r") as file:
        data = list(csv.reader(file))

    pdf = SimpleDocTemplate("contacts.pdf")
    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('GRID',(0,0),(-1,-1),1,colors.black)
    ]))

    pdf.build([table])

    messagebox.showinfo("Done", "PDF exported successfully")


# -----------------------
# GUI PART
# -----------------------
root = tk.Tk()
root.title("Mobile Directory Management System")
root.geometry("900x600")

title = tk.Label(root, text="Mobile Directory System", font=("Arial", 20, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

# input labels + fields
tk.Label(frame, text="Name").grid(row=0, column=0)
name_entry = tk.Entry(frame)
name_entry.grid(row=0, column=1)

tk.Label(frame, text="Phone").grid(row=1, column=0)
phone_entry = tk.Entry(frame)
phone_entry.grid(row=1, column=1)

tk.Label(frame, text="Email").grid(row=2, column=0)
email_entry = tk.Entry(frame)
email_entry.grid(row=2, column=1)

tk.Label(frame, text="CUIN").grid(row=3, column=0)
cuin_entry = tk.Entry(frame)
cuin_entry.grid(row=3, column=1)

tk.Label(frame, text="Address").grid(row=4, column=0)
address_entry = tk.Entry(frame)
address_entry.grid(row=4, column=1)

tk.Button(frame, text="Add Contact", command=add_contact).grid(row=5, column=1, pady=5)

# search section
tk.Label(root, text="Search Name").pack()
search_entry = tk.Entry(root)
search_entry.pack()

tk.Button(root, text="Search Contact", command=search_contact).pack(pady=5)

# -----------------------
# table + scrollbar
# -----------------------
table_frame = tk.Frame(root)
table_frame.pack()

scrollbar = tk.Scrollbar(table_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(
    table_frame,
    columns=("ID","Name","Phone","Email","CUIN","Address"),
    show="headings",
    yscrollcommand=scrollbar.set
)

scrollbar.config(command=tree.yview)

for col in ("ID","Name","Phone","Email","CUIN","Address"):
    tree.heading(col, text=col)

tree.pack()

# buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="View Contacts", command=view_contacts).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Delete Contact", command=delete_contact).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Export PDF", command=export_pdf).grid(row=0, column=2, padx=10)

root.mainloop()
