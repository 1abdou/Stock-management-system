import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import re

#Admin class
class admin:
    def __init__(self, usernam, password, email):
        self.username = usernam
        self.password = password
        self.email = email

#Connect to MYSQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "benyahya123sql",
    database="stock_mang"
)
cursor = connection.cursor()

#Save to database
def save_db(new_dmin):
    query = "INSERT INTO admin (username, password, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (new_dmin.username, new_dmin.password, new_dmin.email))
    connection.commit()

#Checkin the email syntax
def validate_email(email):
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]+.[a-zA-Z]{2,}$"
    return re.match(email_regex, email)

#Checkin the password validate
def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number."
    if not any(char.isalpha() for char in password):
        return "Password must contain at least one letter."
    if not any(char in "!@#$%^&*()-_=+?" for char in password):
        return "Password must contain at least one special character (!@#$%^&*()-_=+)."
    return None

#Sign up function
def sign_up(root):
    username = create_user.get().strip()
    password = create_passw.get()
    confirm_password = confirm_passw.get()
    email = u_email.get().strip()

    # Check all fields are filled
    if username=="Enter your name" or password=="Enter a password" or confirm_password=="Confirm the password" or email=="Enter your email":
        messagebox.showerror("Error", "All fields must be filled out.")
        return
    
     # Validate password strength
    if validate_password(password):
        messagebox.showerror("Error", validate_password(password))
        return
    
    # Check passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return
    
    # Validate email
    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format.")
        return
    
    # If all validations pass
    messagebox.showinfo("Success", "Sign-Up Successful!")
    
    #create new admin
    new_admin = admin(username,password,email)

    #svae admin info to database
    save_db(new_admin)

    #Close sign up windo
    root.destroy()

"""
#########################
#----------main---------#
#########################
"""

#GUI setup
signup = tk.Tk()
signup.title("Sign up")
signup.geometry("800x500")
signup.resizable(False, False)
signup.iconbitmap("E:/python/Projects/stock magemant/assets/login_pic.ico")

#------------image frame------------#
img_frame = tk.Frame(signup, bg="#F0F0F0", width=400)
img_frame.pack(side="left", fill="y")

#resize image
org_img = Image.open("E:/python/Projects/stock magemant/assets/signup.png")
resize = org_img.resize((330,330))
img = ImageTk.PhotoImage(resize)
label = tk.Label(img_frame, border=0, image= img)
label.place(x=50, y=80)

#------------button, labels, entries frame------------#"
my_frame = tk.Frame(signup, bg="white", width=400)
my_frame.pack(side="right", fill="y", ipadx=5)

#Title
title = tk.Label(my_frame, text="Welcome!", fg="#4f75ff", bg="white", font=("Alexandria Black",24))
title.place(x=110, y=50)

#Designing entries when focusin and focusout
def in_use(event):
        if create_user.get() == "Enter your name":
            create_user.delete(0,"end")
            line_1.configure(bg="#4f75ff")
def out_use(event):
    if create_user.get() == "":
        create_user.insert(0,"Enter your name")
        line_1.configure(bg="black")
create_user = tk.Entry(my_frame, width=25, border=0, font=("Alexandria Medium", 11))
create_user.place(x=60, y=130)
create_user.insert(0,"Enter your name")
create_user.bind("<FocusIn>", in_use)
create_user.bind("<FocusOut>", out_use)
line_1 = tk.Frame(my_frame, width=270, height=2, bg="black")
line_1.place(x=60, y=155)
#Designing entries when focusin and focusout
def in_use(event):
    if create_passw.get() == "Enter a password":
        create_passw.delete(0,"end")
        line_2.configure(bg="#4f75ff")
def out_use(event):
    if create_passw.get() == "":
        create_passw.insert(0,"Enter a password")
        line_2.configure(bg="black")
create_passw = tk.Entry(my_frame, width=25, border=0, font=("Alexandria Medium", 11))
create_passw.place(x=60, y=195)
create_passw.insert(0,"Enter a password")
create_passw.bind("<FocusIn>", in_use)
create_passw.bind("<FocusOut>", out_use)
line_2 = tk.Frame(my_frame, width=270, height=2, bg="black")
line_2.place(x=60, y=220)

#Designing entries when focusin and focusout
def in_use(event):
    if confirm_passw.get() == "Confirm the password":
        confirm_passw.delete(0,"end")
        line_3.configure(bg="#4f75ff")
def out_use(event):
    if confirm_passw.get() == "":
        confirm_passw.insert(0,"Confirm the password")
        line_3.configure(bg="black")
confirm_passw = tk.Entry(my_frame, width=25, border=0, font=("Alexandria Medium", 11))
confirm_passw.place(x=60, y=255)
confirm_passw.insert(0,"Confirm the password")
confirm_passw.bind("<FocusIn>", in_use)
confirm_passw.bind("<FocusOut>", out_use)
line_3 = tk.Frame(my_frame, width=270, height=2, bg="black")
line_3.place(x=60, y=280)

#Designing entries when focusin and focusout
def in_use(event):
    if u_email.get() == "Enter your email":
        u_email.delete(0,"end")
        line_4.configure(bg="#4f75ff")
def out_use(event):
    if u_email.get() == "":
        u_email.insert(0,"Enter your email")
        line_4.configure(bg="black")
u_email = tk.Entry(my_frame, width=25, border=0, font=("Alexandria Medium", 11))
u_email.place(x=60, y=320)
u_email.insert(0,"Enter your email")
u_email.bind("<FocusIn>", in_use)
u_email.bind("<FocusOut>", out_use)
line_4 = tk.Frame(my_frame, width=270, height=2, bg="black")
line_4.place(x=60, y=345)

#sign up button
s_btn = ctk.CTkButton(my_frame, text="Sign up", width=270, font=("Alexandria Medium", 16), text_color="black", fg_color="#4f75ff", hover_color="#9FB4FF", cursor="hand2", command=lambda: sign_up(signup))
s_btn.place(x=60, y=390)

#Run the app
try:
    #Display loop
    signup.mainloop()
finally:
    #Close db connection
    cursor.close()
    connection.close()