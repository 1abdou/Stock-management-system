import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import subprocess

#Connect to MYSQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "benyahya123sql",
    database="stock_mang"
)
cursor = connection.cursor()

#log in function
def login_f(root):
    s_user = user.get()
    s_pass = pass_w.get()
    if s_user=="Username" or s_pass=="Password":
        messagebox.showerror("Error!", "username or password are empty!")
        return
    
    #mysql db operations
    query = "SELECT password FROM admin WHERE username = %s"
    cursor.execute(query,(s_user,))
    result = cursor.fetchone()
    if result:
        stored_password = result[0]
        if stored_password == s_pass:
            root.destroy()
            subprocess.run(["python", "E:/python/Projects/stock magemant/stock_mang.py"])
            return
        else:
            messagebox.showerror("Error!", "Invalid password!")
            return
    else:
        messagebox.showerror("Error!", "username not found, please sign up!")

#run sign up file
def sifn_up_f():
    subprocess.run(["python", "E:/python/Projects/stock magemant/signup.py"])

#Show/hide password
def showhide():
    global show_hide_stat
    if show_hide_stat:
        pass_w.configure(show="")
        show_hide_btn.configure(image=open_eye)
        show_hide_stat = 0
    else:
        pass_w.configure(show="●")
        show_hide_btn.configure(image=close_eye)
        show_hide_stat = 1

"""
####################
#-------main-------#
####################
"""
#GUI setup
ctk.set_appearance_mode("light")
window = ctk.CTk()
window.title("Login")
window.geometry("700x500")
window.configure(bg="#ffffff")
window.resizable(False,False)
window.iconbitmap("E:/python/Projects/stock magemant/assets/login_pic.ico")

#Create frame for image
img_frame = tk.Frame(window, bg="white")
img_frame.pack(side="left", fill="y")

#Insert image
org_img = Image.open("E:/python/Projects/stock magemant/assets/login_pic2.png")
resized_img = org_img.resize((300,302))
img = ImageTk.PhotoImage(resized_img)
label = tk.Label(img_frame, image= img, border=0)
label.pack(side="left", padx=5)

#Create frame for labels, entries and buttons
my_frame = tk.Frame(window, width=350, height=500, bg="white")
my_frame.pack(side="right", ipadx=30, fill="y")

#title label
title = ctk.CTkLabel(my_frame, text="Stock Management", text_color="#92E3A9", font=("Alexandria Medium",26, "bold"))
title.place(x=80, y=80)

#Subtitle label
subtitle = ctk.CTkLabel(my_frame, text="Login to your account", text_color="black", font=("Alexandria Medium",16))
subtitle.place(x=120, y=130)

#focus in/out functions
def in_user_entry(event):
    user.configure(border_color="#92E3A9")
def out_user_entry(event):
    if(user.get()):
        user.configure(border_color="gray")
    else:
        user.configure(border_color="red")

#user entry
user = ctk.CTkEntry(my_frame, width=300, placeholder_text="Username", font=("Alexandria Medium", 14), corner_radius=50)
user.place(x=60, y=180)

#bind events
user.bind("<FocusIn>", in_user_entry)
user.bind("<FocusOut>", out_user_entry)

#focus in/out functions
def in_pass_w_entry(event):
    pass_w.configure(border_color="#92E3A9")
def out_pass_w_entry(event):
    if(pass_w.get()):
        pass_w.configure(border_color="gray")
    else:
        pass_w.configure(border_color="red")

#password entry
pass_w = ctk.CTkEntry(my_frame, width=300, placeholder_text="Password", show="●", font=("Alexandria Medium", 14), corner_radius=50,)
pass_w.place(x=60, y=240)

#bind events
pass_w.bind("<FocusIn>", in_pass_w_entry)
pass_w.bind("<FocusOut>", out_pass_w_entry)

#1 for hiding password
show_hide_stat = 1

#Resize images
org_img = Image.open("E:/python/Projects/stock magemant/assets/open_eye.png")
resized_img = org_img.resize((35,15))
open_eye = ImageTk.PhotoImage(resized_img)
org_img = Image.open("E:/python/Projects/stock magemant/assets/close_eye.png")
resized_img = org_img.resize((35,15))
close_eye = ImageTk.PhotoImage(resized_img)

#Show/hide password button
show_hide_btn = tk.Button(my_frame, image=close_eye, borderwidth=0, cursor="hand2", command=showhide)
show_hide_btn.place(x=320, y=247)

#login button
my_btn = ctk.CTkButton(my_frame, text="Login", width=300, font=("Alexandria Medium",16), text_color="black", fg_color="#92E3A9", hover_color="#31C15A", cursor="hand2", command=lambda: login_f(window))
my_btn.place(x=60, y=310)

#sign up label
sign_up_label = ctk.CTkLabel(my_frame, text="Create a new acount:", text_color="black", font=("Alexandria Medium",14))
sign_up_label.place(x=100, y=360)

#sign up button
sign_up_btn = ctk.CTkButton(my_frame, text="Sign Up", font=("Alexandria Medium",14), text_color="blue", fg_color="transparent", hover_color="white", width=80, cursor="hand2", command= sifn_up_f)
sign_up_btn.place(x=247, y=359)

#Run the application
try:
    window.mainloop()
finally:
    cursor.close()
    connection.close()