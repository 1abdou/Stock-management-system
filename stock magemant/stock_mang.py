import customtkinter as ctk
import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image

#Connect to mysql database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="your_db_name"
)
cursor = connection.cursor()

#Article class
class Article:
    def __init__(self, reference, name, price, quantity, date):
        self.reference = reference
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)
        self.date = date

#Stock calss
class Stock:
    def __init__(self):
        self.articles = []
    
#Clear all
def clear_all():
    ref_entry.delete(0,"end")
    name_entry.delete(0,"end")
    pri_entry.delete(0,"end")
    qnt_entry.delete(0,"end")

#Refresh table(treeview)
def show_all():
    #Delete all data from tree
    for data in my_tree.get_children():
        my_tree.delete(data)
    cursor.execute("SELECT reference, name, price, quantity, date FROM articles")
    results = cursor.fetchall()
    #Update tree data from database
    for result in results:
        my_tree.insert(parent="", index="end", text="", values=result)

#Add article to treeview
def add_to_tree():
    reference = ref_entry.get()
    name = name_entry.get()
    price = pri_entry.get()
    quantity = qnt_entry.get()
    #Check if all entries has been filled
    if not (reference and name and price and quantity):
        messagebox.showerror("Error!", "All failds must be filled!")
        return
    try:
        adding_date = datetime.now().strftime("%d-%m-%Y")
        new_article = Article(reference, name, price, quantity, adding_date)
        #Add article to db
        query = "INSERT INTO articles (reference, name, price, quantity, date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (new_article.reference, new_article.name, new_article.price, new_article.quantity, new_article.date))
        connection.commit()
        #Refresh data
        show_all()
        clear_all()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Eroor", f"Error: {err}")
    except ValueError as err:
        messagebox.showerror("Error!", f"Error: {err}")

#Delete article from treeview
def delete_from_tree():
    selected_item = my_tree.selection()
    if not selected_item:
        messagebox.showerror("Error!", "Select item to delete")
    else:
        #Confirmation
        response = messagebox.askyesno("Confirmation", "Are you sure to delete selected item?")
        if response:
            reference = my_tree.item(selected_item, "values")[0]
            #Delete from db
            query = "DELETE FROM articles WHERE reference = %s"
            cursor.execute(query, (reference,))
            connection.commit()
            #Refresh data
            show_all()
        else:
            my_tree.selection_remove(selected_item)
        
#Modify article in treeview
def modify_in_tree():
    selected_item = my_tree.selection()
    if not selected_item:
        messagebox.showerror("Error!", "Select item to modify")
        return
    try:
        reference = my_tree.item(selected_item, "values")[0]
        name = name_entry.get()
        price = pri_entry.get()
        quantity = qnt_entry.get()
        if not name and not price and not quantity:
            messagebox.showerror("Error!", "Enter you changes!")
            return
        old_name = my_tree.item(selected_item, "values")[1]
        old_price = my_tree.item(selected_item, "values")[2]
        old_qnt = my_tree.item(selected_item, "values")[3]
        if not name:
            name = old_name
        if not price:
            price = old_price
        if not quantity:
            quantity = old_qnt
        if not not ref_entry.get():
            messagebox.showerror("Error!", "Can not modify references")
            return
        #Confirmation
        response = messagebox.askyesno("Confirmation",f"Current data:\n   Ref: {reference}\n   name: {old_name}\n   price {old_price}\n   qnt: {old_qnt}\nAfter changes:\n   Ref: {reference}\n   name: {name}\n   price: {price}\n   qnt: {quantity}\nDo you want to implement changes?")
        if response:
            if name:
                mod_data = datetime.now().strftime("%d/%m/%Y")
                query = "UPDATE articles SET name = %s, date = %s WHERE reference = %s"
                cursor.execute(query, (name, mod_data, reference))
                connection.commit()
            if price:
                query = "UPDATE articles SET price = %s, date = %s WHERE reference = %s"
                cursor.execute(query, (float(price), mod_data, reference))
                connection.commit()
            if quantity:
                query = "UPDATE articles SET quantity = %s, date = %s WHERE reference = %s"
                cursor.execute(query, (int(quantity), mod_data, reference))
                connection.commit()
            show_all()
            clear_all()
        else:
            my_tree.selection_remove(selected_item)
            clear_all()
    except ValueError as err:
        messagebox.showerror("Error!", f"Error: {err}")

#Clear search entries
def clear_search():
    search_by_ref_entry.delete(0,"end")
    search_by_name_entry.delete(0,"end")
    min_pri_serach.delete(0,"end")
    max_pri_serach.delete(0,"end")

#Refrence search
def search_by_ref():
    found = False
    ref = search_by_ref_entry.get()
    if ref:
        for item in my_tree.get_children():
            item_values = my_tree.item(item, "values")
            if ref in item_values[0]:
                found = True
                my_tree.selection_set(item)
                for delete_others in my_tree.get_children():
                    delete_others_values = my_tree.item(delete_others, "values")
                    if delete_others_values[0] != ref:
                        my_tree.delete(delete_others)
                break
        if not found:
            messagebox.showinfo("Not found", f"No match found for the ref: {ref}")
        else:
            clear_search()
    else:
        messagebox.showerror("Error!", "Enter reference to make a search")

#Name search
def search_by_name():
    found = False
    name = search_by_name_entry.get()
    if name:
        for item in my_tree.get_children():
            item_values = my_tree.item(item, "values")
            if name in item_values[1]:
                found = True
                my_tree.selection_set(item)
                for delete_others in my_tree.get_children():
                    delete_others_values = my_tree.item(delete_others, "values")
                    if delete_others_values[1] != name:
                        my_tree.delete(delete_others)
                break
        if not found:
            messagebox.showeinfo("Not found", f"No match found for the name: {name}")
        else:
            clear_search()
    else:
        messagebox.showerror("Error!", "Enter name to make a search")

#Price search
def search_by_price():
    found = False
    try:
        min_price = float(min_pri_serach.get())
        max_price = float(max_pri_serach.get())
        if min_price and max_price:
            for item in my_tree.get_children():
                item_values = my_tree.item(item, "values")
                if float(item_values[2]) >= min_price and float(item_values[2]) <= max_price:
                    found = True
                    my_tree.selection_set(item)
                    for delete_others in my_tree.get_children():
                        delete_others_values = my_tree.item(delete_others, "values")
                        if float(delete_others_values[2]) < min_price or float(delete_others_values[2]) > max_price:
                            my_tree.delete(delete_others)
                    break
            if not found:
                messagebox.showinfo("Not found", f"No match found for min price {min_price} and max price {max_price}")
            else:
                clear_search()
        else:
            messagebox.showerror("Error!", "Missing min/max values")
    except ValueError:
        messagebox.showerror("Error!","Values error: min price/max price")

"""
####################################
##############--Main--##############
####################################
"""
#Background color
my_bg_color = "#F7F1F1"

#GUI setup
ctk.set_appearance_mode("light")
window = ctk.CTk()
window.title("Stock Management System")
window.geometry("820x640")
window.iconbitmap("E:/python/Projects/stock magemant/assets/tools_pic.ico")
window.configure(bg=my_bg_color)
window.resizable(False, True)

#Styles
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    background="white",
    foreground="black",
    fieldbackground="white"
)
style.configure(
    "Treeview.Heading",
    background="white",
    foreground="black"
)
style.map(
    "Custom.Treeview",
    background=[("selected", "#92E3A9")],
    foreground=[("selected", "black")]
)

#Treeview setup
my_tree = ttk.Treeview(window, show="headings", height=2, style="Custom.Treeview")
my_tree["columns"] = ("Reference", "Name", "Price", "Quantity", "Date")
my_tree.column("#0", width=0, stretch="NO")
my_tree.column("Reference", anchor="w", width=160, minwidth=60)
my_tree.column("Name", anchor="w", width=160, minwidth=60)
my_tree.column("Price", anchor="center", width=160, minwidth=60)
my_tree.column("Quantity", anchor="center", width=160, minwidth=60)
my_tree.column("Date", anchor="center", width=160, minwidth=60)
#set column names
my_tree.heading("Reference", text="Reference", anchor="w")
my_tree.heading("Name", text="Name", anchor="w")
my_tree.heading("Price", text="Price", anchor="center")
my_tree.heading("Quantity", text="Quantity", anchor="center")
my_tree.heading("Date", text="Date", anchor="center")
my_tree.pack(side="bottom", expand=True, fill="y")

#Button/Label font
btn_font = ("Alexanderia Medium", 14)
lab_font = ("Alixandria Medium", 10)

#Refresh frame
refresh_frame = tk.Frame(window, height=30, bg=my_bg_color)
refresh_frame.pack(side="bottom", fill="x", pady=5)

#Refresh button
refresh_btn = ctk.CTkButton(refresh_frame,text="Show all", width=80, font=btn_font, text_color="black", fg_color="#92E3A9", hover_color="#31C15A", command=show_all)
refresh_btn.place(x=370,y=0)

#Manage frame
manage_frame = tk.LabelFrame(window, text=" Manage ", width=400, height=205, bg=my_bg_color, font=lab_font)
manage_frame.pack(side="left", anchor="nw", padx=5, pady=0)

#labels
ref_label = tk.Label(manage_frame, text="Referece",font=lab_font, bg=my_bg_color, anchor="w", width=10)
ref_label.place(x=3,y=10)
name_label = tk.Label(manage_frame, text="Name",font=lab_font, bg=my_bg_color, anchor="w", width=10)
name_label.place(x=3, y=40)
pri_label = tk.Label(manage_frame, text="Price",font=lab_font, bg=my_bg_color, anchor="w", width=10)
pri_label.place(x=3, y=70)
qnt_label = tk.Label(manage_frame, text="Quantity",font=lab_font, bg=my_bg_color, anchor="w", width=10)
qnt_label.place(x=3, y=100)

#Designing entries focus in/out
def focus_in_entry(event):
    ref_entry.configure(border_width = 2, border_color="#92E3A9")

def focus_out_entry(event):
    ref_entry.configure(border_width = 1, border_color="gray")

#entries
ref_entry = ctk.CTkEntry(manage_frame, width=300, height=5, corner_radius=5, border_width=1, border_color="gray")
ref_entry.place(x=70, y=10)
ref_entry.bind("<FocusIn>", focus_in_entry)
ref_entry.bind("<FocusOut>", focus_out_entry)

#Designing entries focus in/out
def focus_in_entry(event):
    name_entry.configure(border_width = 2, border_color="#92E3A9")

def focus_out_entry(event):
    name_entry.configure(border_width = 1, border_color="gray")

name_entry = ctk.CTkEntry(manage_frame, width=300, height=5, corner_radius=5, border_width=1, border_color="gray")
name_entry.place(x=70, y=40)
name_entry.bind("<FocusIn>", focus_in_entry)
name_entry.bind("<FocusOut>", focus_out_entry)

#Designing entries focus in/out
def focus_in_entry(event):
    pri_entry.configure(border_width = 2, border_color="#92E3A9")

def focus_out_entry(event):
    pri_entry.configure(border_width = 1, border_color="gray")

pri_entry = ctk.CTkEntry(manage_frame, width=300, height=5, corner_radius=5, border_width=1, border_color="gray")
pri_entry.place(x=70, y=70)
pri_entry.bind("<FocusIn>", focus_in_entry)
pri_entry.bind("<FocusOut>", focus_out_entry)

#Designing entries focus in/out
def focus_in_entry(event):
    qnt_entry.configure(border_width = 2, border_color="#92E3A9")

def focus_out_entry(event):
    qnt_entry.configure(border_width = 1, border_color="gray")

qnt_entry = ctk.CTkEntry(manage_frame, width=300, height=5, corner_radius=5, border_width=1, border_color="gray")
qnt_entry.place(x=70, y=100)
qnt_entry.bind("<FocusIn>", focus_in_entry)
qnt_entry.bind("<FocusOut>", focus_out_entry)

#Create a stock
stock = Stock()

#buttons
add_btn = ctk.CTkButton(manage_frame,text="Add", width=90, font=btn_font, text_color="black", fg_color="#92E3A9", hover_color="#31C15A", command=add_to_tree)
add_btn.place(x=70, y=140)
edit_btn = ctk.CTkButton(manage_frame,text="Edit", width=90, font=btn_font, text_color="black", fg_color="#92E3A9", hover_color="#31C15A", command=modify_in_tree)
edit_btn.place(x=175, y=140)
delete_btn = ctk.CTkButton(manage_frame,text="Delete", width=90, font=btn_font, text_color="black", fg_color="#92E3A9", hover_color="#31C15A", command=delete_from_tree)
delete_btn.place(x=280, y=140)

#Search frame
search_frame = tk.LabelFrame(window, text=" Search ", width=400, height=205, bg=my_bg_color, font=lab_font)
search_frame.pack(side="right", anchor="ne", padx=5, pady=0)

#Labels
search_by_ref_lab = tk.Label(search_frame, text="Reference", font=lab_font, bg=my_bg_color, width=10, anchor="w").place(x=0, y=10)
search_by_name_lab = tk.Label(search_frame, text="Name", font=lab_font, bg=my_bg_color, width=10, anchor="w").place(x=0, y=60)
pri_search = tk.Label(search_frame, text="Price", font=lab_font, bg=my_bg_color, width=10, anchor="w").place(x=0, y=120)
line = tk.Label(search_frame, bg=my_bg_color, text="_").place(x=200, y=115)
min_label = tk.Label(search_frame, text="Min price", font=lab_font, bg=my_bg_color, width=10, anchor="center").place(x=90, y=98)
max_label = tk.Label(search_frame, text="Max price", font=lab_font, bg=my_bg_color, width=10, anchor="center").place(x=235, y=98)

#Designing entries focus in/out
def focus_in_entry(event):
    search_by_ref_entry.configure(border_width = 2, border_color="#92E3A9")

def focus_out_entry(event):
    search_by_ref_entry.configure(border_width = 1, border_color="gray")

#entries
search_by_ref_entry = ctk.CTkEntry(search_frame, width=270, height=5, corner_radius=5, border_width=1, border_color="gray")
search_by_ref_entry.place(x=70, y=10)
search_by_ref_entry.bind("<FocusIn>", focus_in_entry)
search_by_ref_entry.bind("<FocusOut>", focus_out_entry)

#Designing entries focus in/out
def focus_in_entry(event):
    search_by_name_entry.configure(border_width = 2, border_color="#92E3A9")

def focus_out_entry(event):
    search_by_name_entry.configure(border_width = 1, border_color="gray")

search_by_name_entry = ctk.CTkEntry(search_frame, width=270, height=5, corner_radius=5, border_width=1, border_color="gray")
search_by_name_entry.place(x=70, y=60)
search_by_name_entry.bind("<FocusIn>", focus_in_entry)
search_by_name_entry.bind("<FocusOut>", focus_out_entry)

#Designing entries focus in/out
def focus_in_entry(event):
    min_pri_serach.configure(border_width = 2, border_color="#92E3A9")

def focus_out_entry(event):
    min_pri_serach.configure(border_width = 1, border_color="gray")

min_pri_serach = ctk.CTkEntry(search_frame, width=125, height=5, corner_radius=5, border_width=1, border_color="gray")
min_pri_serach.place(x=70, y=120)
min_pri_serach.bind("<FocusIn>", focus_in_entry)
min_pri_serach.bind("<FocusOut>", focus_out_entry)

#Designing entries focus in/out
def focus_in_entry(event):
    max_pri_serach.configure(border_width = 2, border_color="#92E3A9")

def focus_out_entry(event):
    max_pri_serach.configure(border_width = 1, border_color="gray")

max_pri_serach = ctk.CTkEntry(search_frame, width=125, height=5, corner_radius=5, border_width=1, border_color="gray")
max_pri_serach.place(x=215, y=120)
max_pri_serach.bind("<FocusIn>", focus_in_entry)
max_pri_serach.bind("<FocusOut>", focus_out_entry)

#Searsh image
org_img = Image.open("E:/python/Projects/stock magemant/assets/search.png")
search_img = ctk.CTkImage(org_img,size=(25,25))

#Buttons
search_by_ref_btn = ctk.CTkButton(search_frame, text="", image=search_img, width=25, fg_color=my_bg_color, hover_color="#92E3A9", command= search_by_ref)
search_by_ref_btn.place(x=343, y=5)
search_by_name_btn = ctk.CTkButton(search_frame, text="", image=search_img, width=25, fg_color=my_bg_color, hover_color="#92E3A9", command= search_by_name)
search_by_name_btn.place(x=343, y=55)
pri_search_btn = ctk.CTkButton(search_frame, text="", image=search_img, width=25, fg_color=my_bg_color, hover_color="#92E3A9", command= search_by_price)
pri_search_btn.place(x=343, y=115)

#Initial data refresh
show_all()

#Run the application
try:
    window.mainloop()
finally:
    cursor.close()
    connection.close()