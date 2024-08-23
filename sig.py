from curses import window
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mbox
from PIL import Image, ImageTk
from fpdf import FPDF
from pymongo import MongoClient
from customtkinter import *


# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['calculatorpy']
collection = db['emidata']

# Function to launch EMI Calculator
def launch_emi_calculator():
    # Main window created
    window = Tk()
    window.geometry("1000x700")
    window.title("EMI Calculator")

    # Variables defined
    firstclick1 = True
    firstclick2 = True
    firstclick3 = True
    firstclick4 = True
    firstclick5 = True
    firstclick6 = True
    cal_emi = 0

    def def_emi():
        mbox.showinfo("EMI INFO", "EMI, which stands for Equated Monthly Installment, is the monthly amount payments we make towards a loan we opted for.\n\nEMI payments include contributions towards both principal and interest on the loan amount.\n\nThe mathematical formula to calculate EMI is: EMI = P × r × (1 + r)n/((1 + r)n - 1) where P= Loan amount, r= interest rate, n=tenure in number of months.")
    # Defined function for start button
    def def_start():
        def on_e1_click(event):
            """function that gets called whenever entry1 is clicked"""
            nonlocal firstclick1
            if firstclick1:  # if this is the first time they clicked it
                firstclick1 = False
                e1.delete(0, "end")  # delete all the text in the entry

        def on_e2_click(event):
            """function that gets called whenever entry2 is clicked"""
            nonlocal firstclick2
            if firstclick2:  # if this is the first time they clicked it
                firstclick2 = False
                e2.delete(0, "end")  # delete all the text in the entry

        def on_e3_click(event):
            """function that gets called whenever entry3 is clicked"""
            nonlocal firstclick3
            if firstclick3:  # if this is the first time they clicked it
                firstclick3 = False
                e3.delete(0, "end")  # delete all the text in the entry

        def on_e4_click(event):
            """function that gets called whenever entry4 is clicked"""
            nonlocal firstclick4
            if firstclick4:  # if this is the first time they clicked it
                firstclick4 = False
                e4.delete(0, "end")  # delete all the text in the entry

        def on_e5_click(event):
            """function that gets called whenever entry5 is clicked"""
            nonlocal firstclick5
            if firstclick5:  # if this is the first time they clicked it
                firstclick5 = False
                e5.delete(0, "end")  # delete all the text in the entry

        def on_e6_click(event):
            """function that gets called whenever entry6 is clicked"""
            nonlocal firstclick6
            if firstclick6:  # if this is the first time they clicked it
                firstclick6 = False
                e6.delete(0, "end")  # delete all the text in the entry

        # Function for generating and saving the PDF
        def def_PDF():
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()

            pdf.set_font("helvetica", "", 20)
            pdf.set_text_color(0, 0, 0)

            pdf.image('Images', x=0, y=0, w=210, h=297)

            pdf.text(55, 129, e1.get())
            pdf.text(70, 142, e2.get())
            pdf.text(60, 155, e3.get())

            pdf.text(78, 197, str(e4.get()))
            pdf.text(96, 210, str(e5.get()))
            pdf.text(93, 223, str(e6.get()))

            pdf.text(91, 264, str(cal_emi))

            pdf.output('EMI_Calculated.pdf')
            mbox.showinfo("PDF Status", "PDF Generated and Saved Successfully.")

        # Function for calculating the EMI
        def def_cal():
            nonlocal cal_emi
            p = int(e4.get())
            r = int(e5.get())
            n = int(e6.get())
            cal_emi = p * (r / 1200) * ((1 + r / 1200) ** n) / (((1 + r / 1200) ** n) - 1)
            mbox.showinfo("EMI DETAILS", "Your Monthly Payment  :  " + str(cal_emi))
            store_data(e1.get(), e4.get(), e5.get(), e6.get(), cal_emi)

        # Function for storing data in MongoDB
        def store_data(Name, Principal, Rate, Time, emi):
            data = {
                "name": Name,
                "principal": Principal,
                "rate": Rate,
                "time": Time,
                "emi": emi
            }
            collection.insert_one(data)
            print("Data stored in MongoDB successfully!")

        # Function for getting user details
        def def_details():
            mbox.showinfo("User Details", "Name  :  " + str(e1.get()) + "\n\nMobile No.  :  " + str(e2.get()) + "\n\nEmail ID  :  " + str(e3.get()))

        # New frame created
        f1 = Frame(window, width=1000, height=700)
        f1.propagate(0)
        f1.pack(side='top')

        # Created entry for Name
        l1 = Label(f1, text='Name', font=("Poppins", 25), fg="brown")
        l1.place(x=100, y=140)
        e1 = Entry(f1, width=30, border=2, font=("Poppins", 22), bg="light yellow")
        e1.insert(0, 'Enter Your Name...')
        e1.bind('<FocusIn>', on_e1_click)
        e1.place(x=300, y=143)

        # Created entry for Mobile No
        l2 = Label(f1, text='Mobile No.', font=("Poppins", 25), fg="brown")
        l2.place(x=100, y=200)
        e2 = Entry(f1, width=30, border=2, font=("Poppins", 22), bg="light yellow")
        e2.insert(0, 'Enter Your Contact...')
        e2.bind('<FocusIn>', on_e2_click)
        e2.place(x=300, y=203)

        # Created entry for Email ID
        l3 = Label(f1, text='Email Id', font=("Poppins", 25), fg="brown")
        l3.place(x=100, y=260)
        e3 = Entry(f1, width=30, border=2, font=("Poppins", 22), bg="light yellow")
        e3.insert(0, 'Enter Your Email Id...')
        e3.bind('<FocusIn>', on_e3_click)
        e3.place(x=300, y=263)

        # Created entry for Loan Amount
        l4 = Label(f1, text='Loan Amount', font=("Poppins", 25), fg="brown")
        l4.place(x=100, y=380)
        e4 = Entry(f1, width=30, border=2, font=("Poppins", 22), bg="light yellow")
        e4.insert(0, 'Enter Your Loan Amount...')
        e4.bind('<FocusIn>', on_e4_click)
        e4.place(x=430, y=383)

        # Created entry for Interest Per Annum
        l5 = Label(f1, text='Interest Per Annum', font=("Poppins", 25), fg="brown")
        l5.place(x=100, y=440)
        e5 = Entry(f1, width=30, border=2, font=("Poppins", 22), bg="light yellow")
        e5.insert(0, 'Enter Your Interest Per Annum...')
        e5.bind('<FocusIn>', on_e5_click)
        e5.place(x=430, y=443)

        # Created entry for Period In Months
        l6 = Label(f1, text='Period In Months', font=("Poppins", 25), fg="brown")
        l6.place(x=100, y=500)
        e6 = Entry(f1, width=30, border=2, font=("Poppins", 22), bg="light yellow")
        e6.insert(0, 'Enter Your Period In Months...')
        e6.bind('<FocusIn>', on_e6_click)
        e6.place(x=430, y=503)

        # Created button for calculating EMI
        calb = Button(window, text="CALCULATE EMI", command=def_cal, font=("Poppins", 20), bg="light green", fg="blue", borderwidth=3, relief="raised")
        calb.place(x=80, y=590)

        # Created button for user details
        userb = Button(window, text="USER DETAILS", command=def_details, font=("Poppins", 20), bg="orange", fg="blue", borderwidth=3, relief="raised")
        userb.place(x=380, y=590)

        # Created button for generating PDF
        pdfb = Button(window, text="GENERATE PDF", command=def_PDF, font=("Poppins", 20), bg="orange", fg="blue", borderwidth=3, relief="raised")
        pdfb.place(x=680, y=590)

        # Created button for exit
        exitb = Button(window, text="EXIT", command=window.quit, font=("Poppins", 20), bg="red", fg="blue", borderwidth=3, relief="raised")
        exitb.place(x=830, y=680)


    # top label
    start1 = tk.Label(text = "EMI  CALCULATOR", font=("Poppins", 50), fg="Black") # same way bg
    start1.place(x = 180, y = 10)

# image on the main window
    path = "./emi_front.jpg"
# Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    img1 = ImageTk.PhotoImage(Image.open(path))
    # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    panel = tk.Label(window, image = img1)
    panel.place(x = 100, y = 140)

    # Created start button
    btn = Button(window, text="START", command=def_start, font=("Poppins", 20, "bold"), bg="yellow", fg="red",
             borderwidth=10, relief="raised", activeforeground="green", activebackground="light green", padx=50)
    btn.place(x=730, y=190)

    # Created EMI Info button
    btn2 = Button(window, text="EMI INFO", command=def_emi, font=("Poppins", 20 , "bold"), bg="light blue", fg="black",
              borderwidth=3, relief="raised", activeforeground="blue", activebackground="light green", padx=20)
    btn2.place(x=730, y=300)

    def exit_win():
        if mbox.askokcancel("Exit", "Do you want to exit?"):
            window.destroy()

    exitb = Button(window, text="EXIT", command=exit_win, font=("Arial", 30), bg="red", fg="blue",
               borderwidth=3, relief="raised")
    exitb.place(x=730, y=410) 

    window.mainloop()


# Function to handle login
def login():
    main = CTk()
    main.title("Login Page")
    main.config(bg="white")

    # Background Image
    bg_img = CTkImage(Image.open("./sign.jpg"), size=(500, 500))
    bg_lab = CTkLabel(main, image=bg_img, text="")
    bg_lab.grid(row=0, column=0)

    # Login Frame
    frame1 = CTkFrame(main, fg_color="#D9D9D9", bg_color="white", height=1050, width=3000, corner_radius=20)
    frame1.grid(row=0, column=1, padx=40)

    # Title
    title = CTkLabel(frame1, text="Welcome Back! \nLogin to Account", text_color="black", font=("", 35, "bold"))
    title.grid(row=0, column=0, sticky="nw", pady=30, padx=10)

    # Username Entry
    usrname_entry = CTkEntry(frame1, text_color="white", placeholder_text="Username", fg_color="black", placeholder_text_color="white",
                             font=("", 16, "bold"), width=200, corner_radius=15, height=45)
    usrname_entry.grid(row=1, column=0, sticky="nwe", padx=30)

    # Password Entry
    passwd_entry = CTkEntry(frame1, text_color="white", placeholder_text="Password", fg_color="black", placeholder_text_color="white",
                            font=("", 16, "bold"), width=200, corner_radius=15, height=45, show="*")
    passwd_entry.grid(row=2, column=0, sticky="nwe", padx=30, pady=20)

    # Create Account Label
    cr_acc = CTkLabel(frame1, text="Create Account!", text_color="black", cursor="hand2", font=("", 15))
    cr_acc.grid(row=3, column=0, sticky="w", pady=20, padx=40)

    # Function to save user data to MongoDB
    def save_login_details():
        username = usrname_entry.get()
        password = passwd_entry.get()

        # You can add additional checks for username/password validity here
        if username and password:
            user_data = {
                "username": username,
                "password": password  # Note: In a real application, store hashed passwords!
            }
            # Store the data in the 'user' collection
            user_collection = db['user']  # New collection for user logins
            user_collection.insert_one(user_data)
            print("User login data stored successfully!")
        else:
            mbox.showwarning("Input Error", "Please enter both username and password.")

    # Login Button
    l_btn = CTkButton(frame1, text="Login", font=("", 15, "bold"), height=40, width=60, fg_color="#0085FF", cursor="hand2",
                      corner_radius=15, command=lambda: [save_login_details(), main.quit(), main.destroy(), launch_emi_calculator()])
    l_btn.grid(row=3, column=0, sticky="ne", pady=20, padx=35)

    main.mainloop()



# Start the login function
login()
