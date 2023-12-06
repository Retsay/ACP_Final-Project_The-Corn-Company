from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from BackEnd import mysqlconnect, insert_data, update_tree_1, update_tree_2, search_id, sorting_data, delete_item, update_data, fetch_data, insert_data1, update_customer_purchase, insert_customer_purchase, fetch_data1, update_info, remove_receipt, fetch_all_receipts, userupdate
from BackEnd import remove_admin_data, is_field_id_existing, deletebusiness, update_business, fetch_purchase_history_data, delete_purchase_history, mysql_change_password,get_total_stock, get_total_field_size, get_total_Profit, get_total_Expenses
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from BackEnd import insert_databusiness, fetch_databusiness
from datetime import datetime
from time import strftime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import re
from tkinter.simpledialog import askstring

def toggle_show_password1():
    if show_password_var1.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

def hide_and_show(window_to_hide, window_to_show):
    window_to_hide.withdraw()
    window_to_show.deiconify()

def logout(current_window, main_window):
    current_window.destroy()
    main_window.deiconify()

def show_user_window(window, username):
    tree_purchase_history = None
    user_window = tk.Tk()
    user_width = 1100
    user_height = 650
    user_window.resizable(width=False, height=False)
    screen_width = user_window.winfo_screenwidth()
    screen_height = user_window.winfo_screenheight()
    x_axis = (screen_width / 2) - (user_width / 2)
    y_axis = (screen_height / 2) - (user_height / 2)
    user_window.geometry("{}x{}+{}+{}".format(user_width, user_height, int(x_axis), int(y_axis)))
    user_window.title("THE CORN COMPANY")
    user_window.config(background="#E8D350")
    style = ttk.Style(user_window)
    style.theme_use('alt')
    style.configure('Treeview', background='yellowgreen')

    BUY_HERE_label_frame = tk.Frame(user_window, bg='#9fe649', width=260, height=40, bd=3, relief=tk.SUNKEN)
    BUY_HERE_label_frame.place(x=358, y=10)

    label = tk.Label(BUY_HERE_label_frame, text="BUY HERE",font=("Arial", 15, "bold"), background='#9fe649')
    label.place(x=80,y=5)

    label = tk.Label(user_window,text="Date:", font=('calibri', 15, 'bold'), background='green', foreground='yellow')
    label.place(x=20, y=608)

    label = tk.Label(user_window, text="Time:", font=('calibri', 15, 'bold'), background='green', foreground='yellow')
    label.place(x=167, y=608)

    time_label = tk.Label(user_window, font=('calibri', 15, 'bold'), background='green', foreground='yellow')
    time_label.place(x=220, y=608)

    date_label = tk.Label(user_window, font=('calibri', 15, 'bold'), background='green', foreground='yellow')
    date_label.place(x=70, y=608)

    def update_time():
        string_time = strftime('%I:%M:%S %p')
        time_label.config(text=string_time)
        time_label.after(1000, update_time)

    def update_date():
        current_date = datetime.now().strftime('%Y-%m-%d')
        date_label.config(text=current_date)
        date_label.after(86400000, update_date)

    update_date()
    update_time()

    purchase_trees = {}

    def search_purchase_history(search_term, window):
        tree = purchase_trees.get(window)

        if tree:
            for item in tree.get_children():
                tree.delete(item)

            all_receipts = fetch_purchase_history_data(search_term)

            if all_receipts:
                for receipt in all_receipts:
                    tree.insert("", "end", values=receipt)
            else:
                messagebox.showinfo("Information", "No matching records found.")
        else:
            messagebox.showerror("Error", "Treeview not found for the window.")

    def reset_purchase_history(tree, original_data):
        for item in tree.get_children():
            tree.delete(item)

        for data in original_data:
            tree.insert("", "end", values=data)

    def open_purchase_history_window():
        purchase_history_window = tk.Toplevel(user_window)
        purchase_history_window.title("Purchase History")

        window_width = purchase_history_window.winfo_reqwidth()
        window_height = purchase_history_window.winfo_reqheight()
        screen_width = purchase_history_window.winfo_screenwidth()
        screen_height = purchase_history_window.winfo_screenheight()

        x_coordinate = int((screen_width - window_width) / 5)
        y_coordinate = int((screen_height - window_height) / 2)

        purchase_history_window.geometry(f"+{x_coordinate}+{y_coordinate}")


        purchase_history_window.resizable(False, False)
        purchase_history_window.config(background="#E8D350")

        all_receipts = fetch_purchase_history_data()


        header_labels = [
            "Purchase ID", "Field ID", "Field Size", "Planted Date", "Harvest Date",
            "Stock", "Address", "Phone Number", "Recipient Name", "Purchase Date"
        ]

        Purchase_label = tk.Label(purchase_history_window, text="CUSTOMER PURCHASE HISTORY", background="#E8D350",font=("Aharoni", 20, 'bold'))
        Purchase_label.place(x=400, y=10)

        search_label = tk.Label(purchase_history_window, text="Search:", background="#E8D350", font=("Arial", 9, 'bold'))
        search_label.place(x=10, y=10)

        search_entry = tk.Entry(purchase_history_window)
        search_entry.place(x=60, y=11)

        search_button = tk.Button(purchase_history_window, text="Search",background="yellowgreen",font=("Arial", 9, 'bold'),
                                  command=lambda: search_purchase_history(search_entry.get(), purchase_history_window))
        search_button.place(x=190, y=9)

        Back_button = tk.Button(purchase_history_window, text="Back",background="yellowgreen",font=("Arial", 9, 'bold'),
                                  command=purchase_history_window.destroy)
        Back_button.place(x=930, y=11)

        reset_button = tk.Button(purchase_history_window, text="Reset",background="yellowgreen",font=("Arial", 9, 'bold'),
                                 command=lambda: reset_purchase_history(purchase_tree, original_data))
        reset_button.grid(row=0, column=1, pady=9, padx=18, sticky=tk.W)


        purchase_tree = ttk.Treeview(purchase_history_window, columns=header_labels, show="headings")

        column_widths = [100, 80, 80, 90, 90, 60, 150, 100, 120, 90]

        for header, width in zip(header_labels, column_widths):
            purchase_tree.heading(header, text=header)
            purchase_tree.column(header, width=width)

        for receipt in all_receipts:
            purchase_tree.insert("", "end", values=receipt)

        purchase_tree.grid(row=1, column=0, columnspan=4, pady=10, padx=10, sticky=tk.W)

        purchase_trees[purchase_history_window] = purchase_tree

        original_data = all_receipts

        if not all_receipts:
            label = tk.Label(purchase_history_window, text="No purchase history found.")
            label.grid(row=2, column=0, columnspan=4, pady=10, padx=10, sticky=tk.W)

    def show_instructions():
        message = "Welcome to the Help section!\n\n"
        message += "1. Input an field ID, Address, Phone No., Recipient Name, Purchase Date. \n"
        message += "2. Press submit\n"
        message += "3. Double Check your order before pressing the buy button.\n"
        message += "4. Receipts provide evidence that a transaction took place and indicate what was bought, making it easier to return or exchange items if necessary.\n"
        message += "\n•You can edit your order by pressing the edit button\n"
        message += "•You can also press the ascending/descending buttons\n"

        messagebox.showinfo("Help", message)

    Email_label = tk.Label(user_window, text="Email: Thecorn_company01@gmail.com", font=('Times new roman', 17, 'bold'), bg="#E8D350")
    Email_label.place(x=330, y=608)

    Contacts_label = tk.Label(user_window, text="Contacts: 09217593335 ", font=('Times new roman', 17, 'bold'),
                           bg="#E8D350")
    Contacts_label.place(x=750, y=608)

    welcome_label = Label(user_window, text=f"Welcome {username}",bd=4, relief="raised", width=25, fg="black", bg="yellowgreen", font=("Times new Roman", 13, "bold"))
    welcome_label.place(x=20, y=12)

    the_label = tk.Label(user_window, text="The", font=("times new roman", 25, "bold"), bg="#E8D350")
    the_label.place(x=15, y=60)

    help_button = tk.Button(user_window, text="HELP", font=("Arial", 9, 'bold'), bg='#9fe649',
                            command=show_instructions)
    help_button.place(x=1038, y=18)

    corn_label = tk.Label(user_window, text="CORN", font=("times new roman", 77, "bold"), fg="yellow", bg="green")
    corn_label.place(x=20, y=105)

    company_label = tk.Label(user_window, text="         COMPANY", font=("times new roman", 30, "bold"),
                             bg="#E8D350")
    company_label.place(x=20, y=240)

    frame = Frame(user_window)
    frame.pack(pady=10)

    tree_frame_2 = tk.Frame(user_window)
    tree_frame_2.place(x=20, y=365, width=1060, height=230)

    tree_2 = ttk.Treeview(tree_frame_2, columns=('FieldID', 'Field_Size', 'PlantedDate', 'HarvestDate', 'Stock'),
                          show='headings')
    tree_2.heading('FieldID', text='Field ID')
    tree_2.heading('Field_Size', text='Field Size')
    tree_2.heading('PlantedDate', text='Planted Date')
    tree_2.heading('HarvestDate', text='Harvest Date')
    tree_2.heading('Stock', text='Stock')
    tree_2.pack()

    tree_2.place(x=0, y=0, width=1060, height=230)

    scrollbar_2 = ttk.Scrollbar(tree_frame_2, orient="vertical", command=tree_2.yview)
    scrollbar_2.pack(side=tk.RIGHT, fill=tk.Y)

    tree_2.config(yscrollcommand=scrollbar_2.set)

    update_tree_2(tree_2)

    def sort_size_ascending():
        sorted_data = sorting_data("ASC", "Field_Size")
        if sorted_data:
            for row in tree_2.get_children():
                tree_2.delete(row)
            for data in sorted_data:
                tree_2.insert("", "end", values=data)

    def sort_size_descending():
        sorted_data = sorting_data("DESC", "Field_Size")
        if sorted_data:
            for row in tree_2.get_children():
                tree_2.delete(row)
            for data in sorted_data:
                tree_2.insert("", "end", values=data)

    SortSizeAscending_button = tk.Button(user_window, text="FieldSize Ascending", font=("Arial", 12, 'bold'),
                                         bg='#9fe649', command=sort_size_ascending)
    SortSizeAscending_button.place(x=15, y=320)

    SortSizeDescending_button = tk.Button(user_window, text="FieldSize Descending", font=("Arial", 12, 'bold'),
                                          bg='#9fe649', command=sort_size_descending)
    SortSizeDescending_button.place(x=185, y=320)

    def sort_harvest_ascending():
        sorted_data = sorting_data("ASC", "HarvestDate")
        if sorted_data:
            for row in tree_2.get_children():
                tree_2.delete(row)
            for data in sorted_data:
                tree_2.insert("", "end", values=data)

    def sort_harvest_descending():
        sorted_data = sorting_data("DESC", "HarvestDate")
        if sorted_data:
            for row in tree_2.get_children():
                tree_2.delete(row)
            for data in sorted_data:
                tree_2.insert("", "end", values=data)

    HarvestAscending_button = Button(user_window, text="HarvestDate Ascending", font=("Arial", 12, 'bold'), bg='#9fe649',
                                     command=sort_harvest_ascending)
    HarvestAscending_button.place(x=365, y=320)

    HarvestDescending_button = Button(user_window, text="HarvestDate Descending", font=("Arial", 12, 'bold'),
                                      bg='#9fe649', command=sort_harvest_descending)
    HarvestDescending_button.place(x=559, y=320)

    def sort_stocks_ascending():
        sorted_data = sorting_data("ASC", "Stock")
        if sorted_data:
            for row in tree_2.get_children():
                tree_2.delete(row)
            for data in sorted_data:
                tree_2.insert("", "end", values=data)

    def sort_stocks_descending():
        sorted_data = sorting_data("DESC", "Stock")
        if sorted_data:
            for row in tree_2.get_children():
                tree_2.delete(row)
            for data in sorted_data:
                tree_2.insert("", "end", values=data)

    stockSortAscending_button = Button(user_window, text="Stocks Ascending", font=("Arial", 12, 'bold'), bg='#9fe649',
                                       command=sort_stocks_ascending)
    stockSortAscending_button.place(x=763, y=320)

    stockSortDescending_button = Button(user_window, text="Stocks Descending", font=("Arial", 12, 'bold'), bg='#9fe649',
                                        command=sort_stocks_descending)
    stockSortDescending_button.place(x=916, y=320)

    LogOut_button = Button(user_window, text="LogOut", command=lambda: logout(user_window, window), font=("Arial", 8, 'bold'), bg='#9fe649')
    LogOut_button.place(x=1030, y=610)

    def search():
        search_id(search_entry, tree_2)

    search_label = tk.Label(user_window, text="Search:", font=('ARIAL', 11, 'bold'), fg="black", bg="#E8D350")
    search_label.place(x=650, y=20)
    search_entry = tk.Entry(user_window, font=("Arial", 11), bg='white', width=17)
    search_entry.place(x=710, y=22 )
    search_button = tk.Button(user_window, text="Search", font=("Arial", 8, 'bold'), bg='#9fe649', command=search)
    search_button.place(x=855, y=20)

    back_button = tk.Button(user_window, text="Reset", font=("Arial", 8, 'bold'), bg='#9fe649',command=lambda: update_tree_2(tree_2))
    back_button.place(x=908, y=20)


    def clear_entries():
        field_id_entry.delete(0, 'end')
        field_id_entry.insert(0, default_field_id)
        field_id_entry.config(fg='grey')

        address_entry.delete(0, 'end')
        address_entry.insert(0, default_address)
        address_entry.config(fg='grey')

        phone_number_entry.delete(0, 'end')
        phone_number_entry.insert(0, default_phone_number)
        phone_number_entry.config(fg='grey')

        recipient_name_entry.delete(0, 'end')
        recipient_name_entry.insert(0, default_recipient_name)
        recipient_name_entry.config(fg='grey')

        purchase_date_entry.delete(0, 'end')
        purchase_date_entry.insert(0, default_purchase_date)
        purchase_date_entry.config(fg='grey')

    def submit():
        try:
            field_id = field_id_entry.get()
            address = address_entry.get()
            phone_number = phone_number_entry.get()
            recipient_name = recipient_name_entry.get()
            purchase_date = purchase_date_entry.get()


            if field_id == default_field_id or address == default_address or \
                    phone_number == default_phone_number or recipient_name == default_recipient_name or \
                    purchase_date == default_purchase_date:
                messagebox.showerror("Invalid Input", "Please fill in all the required fields with valid information.")
                return

            if not all([address, phone_number, recipient_name, purchase_date]):
                messagebox.showerror("Missing Information", "Please fill in all the required fields.")
            else: 
                confirm = messagebox.askquestion("Confirm Submission",
                                                 f"Are you sure you want to submit Field ID: {field_id}?")
                if confirm == 'yes':

                    all_receipts = fetch_purchase_history_data(tree_purchase_history)
                    field_ids = [receipt[1] for receipt in all_receipts]

                    if field_id in field_ids:
                        messagebox.showinfo("Field ID Already Picked", "This field ID has already been picked.")
                    else:

                        insert_data1(field_id, address, phone_number, recipient_name, purchase_date)

                        admin_data = fetch_data(field_id)

                        if admin_data is not None:

                            receipt_label_field_id.config(text=f"Field ID: {field_id}")
                            receipt_label_field_size.config(text=f"Field Size: {admin_data[1]}")
                            receipt_label_planted_date.config(text=f"Planted Date: {admin_data[2]}")
                            receipt_label_harvest_date.config(text=f"Harvest Date: {admin_data[3]}")
                            receipt_label_stock.config(text=f"Stock: {admin_data[4]}")
                            receipt_label_address.config(text=f"Address: {address}")
                            receipt_label_phone_number.config(text=f"Phone Number: {phone_number}")
                            receipt_label_recipient_name.config(text=f"Recipient Name: {recipient_name}")
                            receipt_label_purchase_date.config(text=f"Purchase Date: {purchase_date}")


                            inserted_data = insert_customer_purchase(
                                field_id,
                                admin_data[1],
                                admin_data[2],
                                admin_data[3],
                                admin_data[4],
                                address,
                                phone_number,
                                recipient_name,
                                purchase_date
                            )
                            if inserted_data is not None:
                                messagebox.showinfo("Buy Successful", "Thank you for buying.")
                            else:
                                messagebox.showerror("Error", "Failed to insert data into PurchaseHistory table.")


                            clear_entry_fields()

                        else:
                            messagebox.showerror("Error", "No data found for the provided Field ID.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_entry_fields():
        field_id_entry.delete(0, tk.END)
        field_id_entry.insert(0, default_field_id)

        address_entry.delete(0, tk.END)
        address_entry.insert(0, default_address)

        phone_number_entry.delete(0, tk.END)
        phone_number_entry.insert(0, default_phone_number)

        recipient_name_entry.delete(0, tk.END)
        recipient_name_entry.insert(0, default_recipient_name)

        purchase_date_entry.delete(0, tk.END)
        purchase_date_entry.insert(0, default_purchase_date)

    receipt_frame = tk.LabelFrame(user_window, text="Preview", padx=10, pady=10)
    receipt_frame.place(x=650, y=50, width=430, height=250)

    receipt_label_field_id = tk.Label(receipt_frame, text="")
    receipt_label_field_id.pack()
    receipt_label_field_size = tk.Label(receipt_frame, text="")
    receipt_label_field_size.pack()
    receipt_label_planted_date = tk.Label(receipt_frame, text="")
    receipt_label_planted_date.pack()
    receipt_label_harvest_date = tk.Label(receipt_frame, text="")
    receipt_label_harvest_date.pack()
    receipt_label_stock = tk.Label(receipt_frame, text="")
    receipt_label_stock.pack()
    receipt_label_address = tk.Label(receipt_frame, text="")
    receipt_label_address.pack()
    receipt_label_phone_number = tk.Label(receipt_frame, text="")
    receipt_label_phone_number.pack()
    receipt_label_recipient_name = tk.Label(receipt_frame, text="")
    receipt_label_recipient_name.pack()
    receipt_label_purchase_date = tk.Label(receipt_frame, text="")
    receipt_label_purchase_date.pack()


    def on_entry_click(event, entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, "end")
            entry.config(fg='black')

    def on_focusout(event, entry, default_text):
        if entry.get() == '':
            entry.insert(0, default_text)
            entry.config(fg='grey')

    default_field_id = 'ex.F102'
    default_address = 'ex.Sitio 2'
    default_phone_number = '+63'
    default_recipient_name = 'LN, FN, MI'
    default_purchase_date = 'YYYY-MM-DD'

    frame1 = tk.Frame(user_window, highlightbackground="yellowgreen", highlightthickness=3, background="#E8D350")
    frame1.place(x=332,y=45, height=270, width=308)

    field_id_label = tk.Label(frame1, text="Field ID:", bg="#E8D350", font=("Arial", 12, 'bold'))
    field_id_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    field_id_entry = tk.Entry(frame1, fg="gray", highlightbackground="yellowgreen", highlightthickness=3)
    field_id_entry.insert(0, default_field_id)
    field_id_entry.bind('<FocusIn>', lambda event: on_entry_click(event, field_id_entry, default_field_id))
    field_id_entry.bind('<FocusOut>', lambda event: on_focusout(event, field_id_entry, default_field_id))
    field_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    address_label = tk.Label(frame1, text="Address:", bg="#E8D350", font=("Arial", 12, 'bold'))
    address_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    address_entry = tk.Entry(frame1, fg="gray", highlightbackground="yellowgreen", highlightthickness=3)
    address_entry.insert(0, default_address)
    address_entry.bind('<FocusIn>', lambda event: on_entry_click(event, address_entry, default_address))
    address_entry.bind('<FocusOut>', lambda event: on_focusout(event, address_entry, default_address))
    address_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

    phone_number_label = tk.Label(frame1, text="Phone Number:", bg="#E8D350", font=("Arial", 12, 'bold'))
    phone_number_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
    phone_number_entry = tk.Entry(frame1, fg="gray", highlightbackground="yellowgreen", highlightthickness=3)
    phone_number_entry.insert(0, default_phone_number)
    phone_number_entry.bind('<FocusIn>', lambda event: on_entry_click(event, phone_number_entry, default_phone_number))
    phone_number_entry.bind('<FocusOut>', lambda event: on_focusout(event, phone_number_entry, default_phone_number))
    phone_number_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

    recipient_name_label = tk.Label(frame1, text="Recipient Name:", bg="#E8D350", font=("Arial", 12, 'bold'))
    recipient_name_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
    recipient_name_entry = tk.Entry(frame1, fg="gray", highlightbackground="yellowgreen", highlightthickness=3)
    recipient_name_entry.insert(0, default_recipient_name)
    recipient_name_entry.bind('<FocusIn>',
                              lambda event: on_entry_click(event, recipient_name_entry, default_recipient_name))
    recipient_name_entry.bind('<FocusOut>',
                              lambda event: on_focusout(event, recipient_name_entry, default_recipient_name))
    recipient_name_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

    purchase_date_label = tk.Label(frame1, text="Purchase Date:", bg="#E8D350", font=("Arial", 12, 'bold'))
    purchase_date_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
    purchase_date_entry = tk.Entry(frame1, fg="gray", highlightbackground="yellowgreen", highlightthickness=3)
    purchase_date_entry.insert(0, default_purchase_date)
    purchase_date_entry.bind('<FocusIn>',
                             lambda event: on_entry_click(event, purchase_date_entry, default_purchase_date))
    purchase_date_entry.bind('<FocusOut>', lambda event: on_focusout(event, purchase_date_entry, default_purchase_date))
    purchase_date_entry.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)


    buy_button = tk.Button(receipt_frame, text="BUY", command=submit, bg='#9fe649',state=tk.DISABLED)

    def confirm_purchase():
        try:
            field_id = field_id_entry.get()
            address = address_entry.get()
            phone_number = phone_number_entry.get()
            recipient_name = recipient_name_entry.get()
            purchase_date = purchase_date_entry.get()

            if not all([address, phone_number, recipient_name, purchase_date]):
                messagebox.showerror("Missing Information", "Please fill in all the required fields.")
            else:
                admin_data = fetch_data(field_id)

                if admin_data is not None:
                    receipt_label_field_id.config(text=f"Field ID: {field_id}")
                    receipt_label_field_size.config(text=f"Field Size: {admin_data[1]}")
                    receipt_label_planted_date.config(text=f"Planted Date: {admin_data[2]}")
                    receipt_label_harvest_date.config(text=f"Harvest Date: {admin_data[3]}")
                    receipt_label_stock.config(text=f"Stock: {admin_data[4]}")
                    receipt_label_address.config(text=f"Address: {address}")
                    receipt_label_phone_number.config(text=f"Phone Number: {phone_number}")
                    receipt_label_recipient_name.config(text=f"Recipient Name: {recipient_name}")
                    receipt_label_purchase_date.config(text=f"Purchase Date: {purchase_date}")

                    messagebox.showinfo("Confirmation", "Receipt information updated.")

                    buy_button.config(state=tk.NORMAL)
                    buy_button.pack()

                else:
                    messagebox.showerror("Error", "No data found for the provided Field ID.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    confirm_button = tk.Button(frame1, text="UPDATE", bg='#9fe649', font=("Arial", 9, 'bold'), command=confirm_purchase)
    confirm_button.place(x=230, y=225)

    clear_button = tk.Button(frame1, text="CLEAR", bg='#9fe649', font=("Arial", 9, 'bold'), command=clear_entries)
    clear_button.place(x=178, y=225)

    purchase_history_button = tk.Button(frame1, text="ORDER HISTORY", font=("Arial", 9, 'bold'), bg='#9fe649', command=open_purchase_history_window,)
    purchase_history_button.place(x=71, y=225)

    hide_and_show(window, user_window)
    user_window.mainloop()


def create_main_window():
    def is_password_complex(password):
        uppercase_regex = re.compile(r'[A-Z]')
        if not uppercase_regex.search(password):
            return False

        lowercase_regex = re.compile(r'[a-z]')
        if not lowercase_regex.search(password):
            return False

        digit_regex = re.compile(r'\d')
        if not digit_regex.search(password):
            return False

        special_char_regex = re.compile(r'[!@#$%^&*(),.?":{}|<>]')
        if not special_char_regex.search(password):
            return False

        return True

    def signup():
        username = username_entry.get()
        password = password_entry.get()

        if username and password:
            if is_password_complex(password):
                success = mysqlconnect(username, password, "signup")
                if success:
                    messagebox.showinfo("SignedUp", "Signed Up Successfully!")
                else:
                    messagebox.showinfo("Error", "Username already exists. Please choose a different username.")
            else:
                messagebox.showinfo("Error",
                                    "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
        else:
            messagebox.showinfo("Error", "Username and Password cannot be empty")

    def signin():
        username = username_entry.get()
        password = password_entry.get()
        success = mysqlconnect(username, password, "signin")
        if success:
            show_user_window(window, username)
        else:
            messagebox.showinfo("Error", "Invalid username or password.")

    def check_password(password):
        if password == "123":
            password_window.destroy()
            open_admin_window()
        else:
            messagebox.showerror("Login Status", "Login failed")

    def admin_login1():
        global password_window, password_entry, show_password_var1
        password_window = tk.Toplevel(window)
        password_window.title("Admin Login")
        password_window.geometry("300x120+{}+{}".format(
            int((window.winfo_screenwidth() / 2) - (300 / 2)),
            int((window.winfo_screenheight() / 2) - (120 / 2))))
        password_window.resizable(0, 0)
        password_window.config(background="yellowgreen")

        password_label = ttk.Label(password_window, text="Enter password:", font=("Arial", 10, "bold"))
        password_label.configure(background="yellowgreen")
        password_label.pack()

        password_entry = ttk.Entry(password_window, show="*")
        password_entry.configure(background="white")
        password_entry.pack()

        show_password_var1 = tk.BooleanVar()
        show_password_checkbox1 = ttk.Checkbutton(password_window, text="Show Password", variable=show_password_var1,
                                                 command=toggle_show_password1, style='TCheckbutton')
        show_password_checkbox1.pack()
        style = ttk.Style()
        style.configure('TCheckbutton', background="yellowgreen", highlightbackground="yellowgreen",
                        highlightcolor="yellowgreen")

        submit_button = tk.Button(password_window, text="Submit", bg='yellow', font=("Arial", 10, "bold"),
                                  command=lambda: check_password(password_entry.get()))
        submit_button.place(x=120, y=65)

    def change_password_window():
        window.iconify()

        username_for_change = askstring("Change Password", "Enter your username for password change:")

        if username_for_change:
            new_password = askstring("Change Password", "Enter your new password:")

            if new_password:
                if not is_password_complex(new_password):
                    messagebox.showinfo("Error",
                                        "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
                    window.deiconify()
                    return

                success = mysql_change_password(username_for_change, new_password)
                if success:
                    messagebox.showinfo("Password Change", "Password changed successfully!")
                else:
                    messagebox.showinfo("Error", "Username not found or password change failed. Please try again.")
            else:
                messagebox.showinfo("Password Change", "New password cannot be empty. Please try again.")
        else:
            messagebox.showinfo("Password Change", "Username cannot be empty. Please try again.")

        window.deiconify()

    def open_admin_window():
            global admin_window
            Admin_window = tk.Tk()
            Admin_width = 1130
            Admin_height = 695
            Admin_window.resizable(width=False, height=False)
            screen_width = Admin_window.winfo_screenwidth()
            screen_height = Admin_window.winfo_screenheight()
            x_axis = (screen_width / 2) - (Admin_width / 2)
            y_axis = (screen_height / 2) - (Admin_height / 2)
            Admin_window.geometry("{}x{}+{}+{}".format(Admin_width, Admin_height, int(x_axis), int(y_axis)))
            Admin_window.title("Admin Workspace")
            style = ttk.Style(Admin_window)
            style.theme_use('alt')
            style.configure('Treeview', background='lightyellow')
            Admin_window.config(background="green")

            label = tk.Label(Admin_window, text="Corn Data", fg="white", background="green",
                                     font=("Algerian", 15, "bold"))
            label.place(x=70, y=300)

            label = tk.Label(Admin_window, text="Profit/Expenses", fg="white", background="green",
                                     font=("Algerian", 15, "bold"))
            label.place(x=350, y=380)


            WelcomeAdmin_label = tk.Label(Admin_window,bd=4, relief="raised", text="ADMIN WORKSPACE", width=25, fg="green", bg="#E8D350", font=("Times new Roman", 13, "bold"))
            WelcomeAdmin_label.place(x=420,y=15)

            frame1 = tk.Frame(Admin_window, width=100, highlightbackground="gold", highlightthickness=3,
                              background="green")
            frame1.grid(row=0, column=0, padx=20, pady=330, ipadx=1, ipady=35)

            FieldId_label = tk.Label(frame1, text="FIELD ID", fg="white", background="green", font=("Arial", 10, "bold"))
            FieldId_label.grid(padx=5, pady=5)
            FieldId_entry = tk.Entry(frame1, fg="white", highlightbackground="gold", highlightthickness=3, background="green")
            FieldId_entry.grid(padx=5, pady=0)

            FieldSize_label = tk.Label(frame1, text="FIELD SIZE", fg="white", background="green", font=("Arial", 10, "bold"))
            FieldSize_label.grid(padx=15, pady=5)
            FieldSize_entry = tk.Entry(frame1, fg="white", highlightbackground="gold", highlightthickness=3, background="green")
            FieldSize_entry.grid(padx=15, pady=0)

            Planted_Date_label = tk.Label(frame1, text="PLANTED DATE", fg="white", background="green", font=("Arial", 10, "bold"))
            Planted_Date_label.grid(padx=25, pady=5)
            Planted_Date = tk.Entry(frame1, fg="white", highlightbackground="gold", highlightthickness=3, background="green")
            Planted_Date.grid(padx=25, pady=0)

            Harvest_Date_label = tk.Label(frame1, text="HARVEST DATE", fg="white", background="green", font=("Arial", 10, "bold"))
            Harvest_Date_label.grid(padx=35, pady=5)
            Harvest_Date_entry = tk.Entry(frame1, fg="white", highlightbackground="gold", highlightthickness=3, background="green")
            Harvest_Date_entry.grid(padx=35, pady=0)

            Stock_label = tk.Label(frame1, text="STOCK", fg="white", background="green", font=("Arial", 10, "bold"))
            Stock_label.grid(padx=45, pady=5)
            Stock_entry = tk.Entry(frame1, fg="white", highlightbackground="gold", highlightthickness=3, background="green")
            Stock_entry.grid(padx=45, pady=0)

            Edit_button = tk.Button(frame1, text="EDIT", width=10, background="#E8D350", command=lambda: on_edit_button_click(tree_1))
            Edit_button.place(x=30, y=300)

            def show_graph():
                data = fetch_databusiness()

                fig = Figure(figsize=(7, 5), dpi=100)
                plot = fig.add_subplot(111)
                x = range(len(data))
                profits = [row[2] for row in data]
                expenses = [row[3] for row in data]
                months = [row[1] for row in data]

                plot.plot(x, profits, marker='o',linestyle='-', color='green', label='Profits')
                plot.plot(x, expenses, marker='o',linestyle='--', color='yellow', label='Expenses')
                plot.set_title('Profits and Expenses Over Time')
                plot.set_xlabel('Months')
                plot.set_ylabel('Pesos')
                plot.set_xticks(x)
                plot.set_xticklabels(months, rotation=45)
                plot.legend()

                graph_window = tk.Toplevel(Admin_window)
                graph_window.title("Business XY Plot")
                graph_window.config(bg="green")  # Set background color to green

                canvas = FigureCanvasTkAgg(fig, master=graph_window)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.config(bg="green")  # Set background color of the plot canvas
                canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                plot.set_facecolor("lightgray")
                plot.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

                download_button = tk.Button(graph_window, text="Download Graph", command=lambda: download_graph(fig),bg='#E8D350',font=("Arial", 10, "bold"))
                download_button.pack()

                graph_window.mainloop()

            def download_graph(fig):
                directory_path = r"C:\GRAPH PICTURES"

                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)

                filename = os.path.join(directory_path, "business_graph.png")
                fig.savefig(filename)

                messagebox.showinfo("Download Successful", f"The graph has been downloaded to {filename}.")

            def clear_businessentries():
                profits_entry.delete(0, tk.END)
                expenses_entry.delete(0, tk.END)
                dates_entry.delete(0, tk.END)

            frame2 = tk.Frame(Admin_window, width=100, highlightbackground="gold", highlightthickness=3,
                              background="green")
            frame2.place(x=290, y=410, height=280, width=340)

            tk.Label(frame2, text="PROFIT", fg="white", background="green", font=("Arial", 10, "bold")).grid(padx=5, pady=5)
            profits_entry = tk.Entry(frame2, fg="white", background="green", highlightthickness=2, highlightbackground="#E8D350")
            profits_entry.grid(padx=5, pady=0)

            tk.Label(frame2, text="EXPENSES", fg="white", background="green", font=("Arial", 10, "bold")).grid(padx=15, pady=5)
            expenses_entry = tk.Entry(frame2, fg="white", background="green", highlightthickness=2, highlightbackground="#E8D350")
            expenses_entry.grid(padx=15, pady=0)

            tk.Label(frame2, text="DATES", fg="white", background="green", font=("Arial", 10, "bold")).grid(padx=25, pady=5)
            dates_entry = tk.Entry(frame2, fg="white", background="green", highlightthickness=2, highlightbackground="#E8D350")
            dates_entry.grid(padx=25, pady=0)

            clear_button = tk.Button(frame2, text="CLEAR", width=10, background="#E8D350", command=clear_businessentries)
            clear_button.place(x=10, y=205)

            def update_plot(profits_entry, expenses_entry, dates_entry):
                new_profit = profits_entry.get()
                new_expense = expenses_entry.get()
                new_date = dates_entry.get()

                if not new_profit or not new_expense or not new_date:
                    tk.messagebox.showerror("Error", "All fields are required.")
                    return

                try:
                    new_profit = int(new_profit)
                    new_expense = int(new_expense)
                except ValueError:
                    tk.messagebox.showerror("Error", "Profit and Expense should be numbers.")
                    return

                insert_databusiness(new_date, new_profit, new_expense)
                refresh_listbox()

            update_button = tk.Button(frame2, text="ADD", width=10, background="#E8D350",command=lambda: update_plot(profits_entry, expenses_entry, dates_entry))
            update_button.place(x=90, y=180)

            show_graph_button = tk.Button(frame2, text="GRAPH", command=show_graph, bg="#E8D350")
            show_graph_button.place(x=65, y=240)

            def selectbusinessitem():
                selected_item = listbox.curselection()
                if not selected_item:
                    messagebox.showinfo("Error", "Please select an item from the list to delete.")
                else:
                    deletebusiness(listbox)

            def editbusinesswindow():
                if listbox.curselection():
                    edit_window = tk.Tk()
                    edit_window.title("Edit Item")
                    screen_width = edit_window.winfo_screenwidth()
                    screen_height = edit_window.winfo_screenheight()
                    window_width = 260
                    window_height = 150
                    x_coordinate = int((screen_width / 2) - (window_width / 2))
                    y_coordinate = int((screen_height / 2) - (window_height / 2))
                    edit_window.config(background="green")

                    edit_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
                    edit_window.resizable(False, False)

                    selected_item = listbox.get(listbox.curselection())
                    item_id = selected_item.split("-")[0].strip().split(":")[1].strip()
                    item_month = selected_item.split("-")[1].strip().split(":")[1].strip()
                    item_profit = selected_item.split("-")[2].strip().split(":")[1].strip()
                    item_expense = selected_item.split("-")[3].strip().split(":")[1].strip()

                    tk.Label(edit_window, text="New Month:", background="#E8D350", width=10).place(x=10, y=11)
                    new_month_entry = tk.Entry(edit_window, width=20, background="green", highlightthickness=3, highlightbackground="#E8D350",fg="white")
                    new_month_entry.insert(0, item_month)
                    new_month_entry.place(x=100, y=11)

                    tk.Label(edit_window, text="Profit:", background="#E8D350", width=10).place(x=10, y=40)
                    new_profit_entry = tk.Entry(edit_window, width=20, background="green", highlightthickness=3, highlightbackground="#E8D350",fg="white")
                    new_profit_entry.insert(0, item_profit)
                    new_profit_entry.place(x=100, y=40)

                    tk.Label(edit_window, text="Expense:", background="#E8D350", width=10).place(x=10, y=70)
                    new_expense_entry = tk.Entry(edit_window, width=20, background="green", highlightthickness=3, highlightbackground="#E8D350",fg="white")
                    new_expense_entry.insert(0, item_expense)
                    new_expense_entry.place(x=100, y=70)

                    confirm_edit_button = tk.Button(edit_window,text="Confirm", bg="#E8D350",command=lambda: confirm_edit(item_id, new_month_entry.get(), new_profit_entry.get(),new_expense_entry.get(), edit_window))
                    confirm_edit_button.place(x=140,y=105)

                    edit_window.mainloop()

                else:
                    messagebox.showinfo("Error", "Please select an item from the list to edit.")


            def refresh_listbox():
                listbox.delete(0, tk.END)
                data = fetch_databusiness()
                if data:
                    for row in data:
                        listbox.insert(tk.END, f"ID: {row[0]} - Month: {row[1]} - Profit: {row[2]} - Expense: {row[3]}")
                else:
                    messagebox.showinfo("Info", "No data available.")

            def confirm_edit(item_id, new_month, new_profit, new_expense, edit_window):
                update_business(item_id, new_month, new_profit, new_expense)
                edit_window.destroy()
                refresh_listbox()

            edit_button = tk.Button(frame2, text="EDIT", width=10, background="#E8D350",command=editbusinesswindow)
            edit_button.place(x=10, y=180)

            deletebusiness_button = tk.Button(frame2, text="DELETE", width=10, background="red", command=selectbusinessitem)
            deletebusiness_button.place(x=90, y=205)

            listbox = tk.Listbox(Admin_window, width=41, height=15, bg="green", font=("Arial", 9, "bold"), fg="white",
                                 highlightbackground="gold", highlightthickness=3, selectbackground="gray")
            listbox.place(x=480, y=425)

            data = fetch_databusiness()
            for row in data:
                listbox.insert(tk.END, f"ID: {row[0]} - Month: {row[1]} - Profit: {row[2]} - Expense: {row[3]}")

            def clear_entriesadmin():
                FieldId_entry.delete(0, 'end')
                FieldSize_entry.delete(0, 'end')
                Planted_Date.delete(0, 'end')
                Harvest_Date_entry.delete(0, 'end')
                Stock_entry.delete(0, 'end')

            Clear_button = tk.Button(frame1, text="CLEAR", width=10, background="#E8D350", command=clear_entriesadmin)
            Clear_button.place(x=30, y=325)

            def on_delete_button_click():
                selected_item = tree_1.focus()
                if not selected_item:
                    tk.messagebox.showinfo("Error", "Please select an item from the tree to delete.")
                else:
                    delete_item(tree_1)

            delete_button = tk.Button(frame1, text="DELETE", width=10, background="red", command=on_delete_button_click)
            delete_button.place(x=110, y=325)

            LogOut_button = tk.Button(Admin_window, text="LogOut", command=lambda: logout(Admin_window, window), bg="gold",width=10)
            LogOut_button.place(x=1040, y=660)

            def add_to_db():
                field_id = FieldId_entry.get()
                if not field_id or not FieldSize_entry.get() or not Planted_Date.get() or not Harvest_Date_entry.get() or not Stock_entry.get():
                    tk.messagebox.showinfo("Error", "Please fill in all the entries.")
                elif is_field_id_existing(field_id):
                    tk.messagebox.showinfo("Error", f"Field ID {field_id} already exists")
                else:
                    field_size = FieldSize_entry.get()
                    planted_date = Planted_Date.get()
                    harvest_date = Harvest_Date_entry.get()
                    stock = Stock_entry.get()
                    insert_data(field_id, field_size, planted_date, harvest_date, stock)
                    update_tree_1(tree_1)

            Add_button = tk.Button(frame1, text="ADD", width=10, background="#E8D350", command=add_to_db)
            Add_button.place(x=110, y=300)

            tree_1_frame = tk.Frame(Admin_window)
            tree_1_frame.place(x=40, y=50, width=1060, height=200)

            tree_1 = ttk.Treeview(tree_1_frame,
                                  columns=('FieldID', 'Field_Size', 'PlantedDate', 'HarvestDate', 'Stock'),
                                  show='headings')
            tree_1.heading('FieldID', text='Field ID')
            tree_1.heading('Field_Size', text='Field Size')
            tree_1.heading('PlantedDate', text='Planted Date')
            tree_1.heading('HarvestDate', text='Harvest Date')
            tree_1.heading('Stock', text='Stock')
            tree_1.place(x=0, y=0, width=1060, height=200)

            scrollbar = ttk.Scrollbar(tree_1_frame, orient="vertical", command=tree_1.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            tree_1.config(yscrollcommand=scrollbar.set)

            update_tree_1(tree_1)

            def on_edit_button_click(tree_1):
                selected_item = tree_1.focus()
                if not selected_item:
                    tk.messagebox.showinfo("Error", "Please select an item from the tree to edit.")
                else:
                    values = tree_1.item(selected_item, 'values')
                    if values:
                        edit_window = tk.Toplevel()
                        edit_window.title("Edit Item")
                        screen_width = edit_window.winfo_screenwidth()
                        screen_height = edit_window.winfo_screenheight()
                        window_width = 260
                        window_height = 200
                        x_coordinate = int((screen_width / 2) - (window_width / 2))
                        y_coordinate = int((screen_height / 2) - (window_height / 2))
                        edit_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
                        edit_window.resizable(False, False)
                        edit_window.config(background="green")

                        def save_edit():
                            new_values = (
                                field_id_entry.get(),
                                field_size_entry.get(),
                                planted_date_entry.get(),
                                harvest_date_entry.get(),
                                stock_entry.get()
                            )
                            tree_1.item(selected_item, values=new_values)
                            update_data(values[0], new_values)
                            edit_window.destroy()

                        field_id_label = tk.Label(edit_window, text="FIELD ID", background="#E8D350", width=12)
                        field_id_label.place(x=10, y=11)
                        field_id_entry = tk.Entry(edit_window, width=20, background="green", highlightthickness=3, highlightbackground="#E8D350", fg="white")
                        field_id_entry.place(x=105, y=11)
                        field_id_entry.insert(0, values[0])

                        field_size_label = tk.Label(edit_window, text="FIELD SIZE", background="#E8D350", width=12)
                        field_size_label.place(x=10, y=40)
                        field_size_entry = tk.Entry(edit_window, width=20, background="green", highlightthickness=3, highlightbackground="#E8D350", fg="white")
                        field_size_entry.place(x=105, y=40)
                        field_size_entry.insert(0, values[1])

                        planted_date_label = tk.Label(edit_window, text="PLANTED DATE", background="#E8D350", width=12)
                        planted_date_label.place(x=10, y=70)
                        planted_date_entry = tk.Entry(edit_window, width=20, background="green", highlightthickness=3, highlightbackground="#E8D350", fg="white")
                        planted_date_entry.place(x=105, y=70)
                        planted_date_entry.insert(0, values[2])

                        harvest_date_label = tk.Label(edit_window, text="HARVEST DATE", background="#E8D350", width=12)
                        harvest_date_label.place(x=10, y=100)
                        harvest_date_entry = tk.Entry(edit_window, width=20, background="green", highlightthickness=3, highlightbackground="#E8D350", fg="white")
                        harvest_date_entry.place(x=105, y=100)
                        harvest_date_entry.insert(0, values[3])

                        stock_label = tk.Label(edit_window, text="STOCK", background="#E8D350", width=12)
                        stock_label.place(x=10, y=130)
                        stock_entry = tk.Entry(edit_window, width=20, background="green", highlightthickness=3, highlightbackground="#E8D350", fg="white")
                        stock_entry.place(x=105, y=130)
                        stock_entry.insert(0, values[4])

                        save_button = tk.Button(edit_window,text="Save", bg="#E8D350", command=save_edit)
                        save_button.place(x=140,y=165)

                        edit_window.update_idletasks()
                        window_width = edit_window.winfo_width()
                        window_height = edit_window.winfo_height()
                        position_right = int(edit_window.winfo_screenwidth() / 2 - window_width / 2)
                        position_down = int(edit_window.winfo_screenheight() / 2 - window_height / 2)
                        edit_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

            def sort_size_ascending():
                sorted_data = sorting_data("ASC", "Field_Size")
                if sorted_data:
                    for row in tree_1.get_children():
                        tree_1.delete(row)
                    for data in sorted_data:
                        tree_1.insert("", "end", values=data)

            def sort_size_descending():
                sorted_data = sorting_data("DESC", "Field_Size")
                if sorted_data:
                    for row in tree_1.get_children():
                        tree_1.delete(row)
                    for data in sorted_data:
                        tree_1.insert("", "end", values=data)

            SortSizeAscending_button = tk.Button(Admin_window, text="   FIELDSIZE ASCENDING  ", command=sort_size_ascending, font=("times new roman", 10, "bold"), background="#E8D350")
            SortSizeAscending_button.place(x=40, y=265)

            SortSizeDescending_button = tk.Button(Admin_window, text="   FIELDSIZE DESCENDING ", command=sort_size_descending, font=("times new roman", 10, "bold"), background="#E8D350")
            SortSizeDescending_button.place(x=205, y=265)

            def sort_harvest_ascending():
                sorted_data = sorting_data("ASC", "HarvestDate")
                if sorted_data:
                    for row in tree_1.get_children():
                        tree_1.delete(row)
                    for data in sorted_data:
                        tree_1.insert("", "end", values=data)

            def sort_harvest_descending():
                sorted_data = sorting_data("DESC", "HarvestDate")
                if sorted_data:
                    for row in tree_1.get_children():
                        tree_1.delete(row)
                    for data in sorted_data:
                        tree_1.insert("", "end", values=data)

            HarvestAscending_button = tk.Button(Admin_window, text=" HARVESTDATE ASCENDING  ",command=sort_harvest_ascending, font=("times new roman", 10, "bold"), background="#E8D350")
            HarvestAscending_button.place(x=374, y=265)

            HarvestDescending_button = tk.Button(Admin_window, text=" HARVESTDATE DESCENDING  ", command=sort_harvest_descending, font=("times new roman", 10, "bold"), background="#E8D350")
            HarvestDescending_button.place(x=563, y=265)

            def sort_stocks_ascending():
                sorted_data = sorting_data("ASC", "Stock")
                if sorted_data:
                    for row in tree_1.get_children():
                        tree_1.delete(row)
                    for data in sorted_data:
                        tree_1.insert("", "end", values=data)

            def sort_stocks_descending():
                sorted_data = sorting_data("DESC", "Stock")
                if sorted_data:
                    for row in tree_1.get_children():
                        tree_1.delete(row)
                    for data in sorted_data:
                        tree_1.insert("", "end", values=data)

            stockSortAscending_button = tk.Button(Admin_window, text="        STOCKS ASCENDING     ",command=sort_stocks_ascending, font=("times new roman", 10, "bold"), background="#E8D350")
            stockSortAscending_button.place(x=759, y=265)

            stockSortDescending_button = tk.Button(Admin_window, text="   STOCKS DESCENDING   ",command=sort_stocks_descending, font=("times new roman", 10, "bold"), background="#E8D350")
            stockSortDescending_button.place(x=938, y=265)

            def search():
                search_id(search_entry, tree_1)

            search_label = tk.Label(Admin_window, text="Search :",font=('Arial',11,'bold'),  fg="white",bg="green", width=10)
            search_label.place(x=715, y=17)
            search_entry = tk.Entry(Admin_window, width=20)
            search_entry.place(x=795, y=18)
            search_button = tk.Button(Admin_window, text="SEARCH",font=("Arial", 10, "bold"),command=search, background="#E8D350", width=10)
            search_button.place(x=925, y=15)

            back_button = tk.Button(Admin_window, text="RESET",font=("Arial", 10, "bold"), background="#E8D350", width=10, command=lambda: update_tree_1(tree_1))
            back_button.place(x=1015, y=15)

            def search_purchase_history(purchase_tree, search_term):
                if purchase_tree:
                    for item in purchase_tree.get_children():
                        purchase_tree.delete(item)

                    all_receipts = fetch_purchase_history_data(search_term)

                    if all_receipts:
                        for receipt in all_receipts:
                            purchase_tree.insert("", "end", values=receipt)
                    else:
                        messagebox.showinfo("Information", "No matching records found.")
                else:
                    messagebox.showerror("Error", "Treeview not found.")

            def reset_purchase_history(purchase_tree, original_data):
                if purchase_tree:
                    for item in purchase_tree.get_children():
                        purchase_tree.delete(item)

                    for data in original_data:
                        purchase_tree.insert("", "end", values=data)

            def delete_purchase_history_from_window(purchase_tree, purchase_history_window):
                selected_item = purchase_tree.selection()

                if not selected_item:
                    messagebox.showinfo("Information", "Please select a row to delete.")
                    return

                purchase_id = purchase_tree.item(selected_item, 'values')[0]

                try:
                    delete_purchase_history(purchase_id)
                    search_purchase_history(purchase_tree, "")
                    messagebox.showinfo("Information", "Record deleted successfully.")

                except Exception as ex:
                    messagebox.showerror("Error", f"An error occurred: {ex}")

            def open_purchase_history_window():
                purchase_history_window = tk.Toplevel(Admin_window)
                purchase_history_window.title("Purchase History")

                window_width = purchase_history_window.winfo_reqwidth()
                window_height = purchase_history_window.winfo_reqheight()
                screen_width = purchase_history_window.winfo_screenwidth()
                screen_height = purchase_history_window.winfo_screenheight()

                x_coordinate = int((screen_width - window_width) / 5)
                y_coordinate = int((screen_height - window_height) / 2)

                purchase_history_window.geometry(f"+{x_coordinate}+{y_coordinate}")
                purchase_history_window.resizable(False, False)
                purchase_history_window.config(background="green")

                all_receipts = fetch_purchase_history_data()

                header_labels = [
                    "Purchase ID", "Field ID", "Field Size", "Planted Date", "Harvest Date",
                    "Stock", "Address", "Phone Number", "Recipient Name", "Purchase Date"
                ]

                Purchase_label = tk.Label(purchase_history_window, text="    CUSTOMER PURCHASE HISTORY    ", background="#E8D350", fg="green",
                                          font=("Aharoni", 20, 'bold'))
                Purchase_label.place(x=400, y=12)

                search_label = tk.Label(purchase_history_window, text="Search:", background="green",fg='white',
                                        font=("Arial", 10, 'bold'))
                search_label.place(x=10, y=20)

                search_entry = tk.Entry(purchase_history_window)
                search_entry.place(x=64, y=21)

                search_button = tk.Button(purchase_history_window, text="Search", background="#E8D350",
                                          font=("Arial", 9, 'bold'),
                                          command=lambda: search_purchase_history(purchase_tree, search_entry.get()))
                search_button.place(x=190, y=19)

                Back_button = tk.Button(purchase_history_window, text="Back", background="#E8D350",
                                        font=("Arial", 9, 'bold'),
                                        command=purchase_history_window.destroy)
                Back_button.place(x=930, y=19)

                reset_button = tk.Button(purchase_history_window, text="Reset", background="#E8D350",
                                         font=("Arial", 9, 'bold'),
                                         command=lambda: reset_purchase_history(purchase_tree, original_data))
                reset_button.grid(row=0, column=1, pady=19, padx=140, sticky=tk.W)

                delete_button = tk.Button(
                    purchase_history_window,
                    text="Delete",
                    background="red",
                    font=("Arial", 9, 'bold'),
                    command=lambda window=purchase_history_window: delete_purchase_history_from_window(purchase_tree,
                                                                                                       window)
                )
                delete_button.grid(row=0, column=1, pady=19, padx=85, sticky=tk.W)

                purchase_tree = ttk.Treeview(purchase_history_window, columns=header_labels, show="headings")

                column_widths = [100, 80, 80, 90, 90, 60, 150, 100, 120, 90]

                for header, width in zip(header_labels, column_widths):
                    purchase_tree.heading(header, text=header)
                    purchase_tree.column(header, width=width)

                for receipt in all_receipts:
                    purchase_tree.insert("", "end", values=receipt)

                purchase_tree.grid(row=1, column=0, columnspan=4, pady=5, padx=10, sticky=tk.W)

                original_data = all_receipts

                if not all_receipts:
                    label = tk.Label(purchase_history_window, text="No purchase history found.")
                    label.grid(row=2, column=0, columnspan=4, pady=5, padx=10, sticky=tk.W)


            def remove_receipt_and_admin(purchase_no, field_id, frame, tree):
                remove_receipt(purchase_no)
                remove_admin_data(field_id)
                update_tree_1(tree)
                frame.destroy()


            def view_all_receipts(Admin_window, tree_1):
                receipt_frame = tk.Frame(Admin_window, bg="green")
                receipt_frame.place(x=779, y=330, width=350, height=300)

                order_label = tk.Label(receipt_frame, text="Customer Order", fg="white", background="green",
                                     font=("Algerian", 15, "bold"))
                order_label.place(x=100, y=0)

                canvas = tk.Canvas(receipt_frame, bg="green", highlightbackground="gold", highlightthickness=3)
                canvas.place(x=40, y=30)

                scrollbar = ttk.Scrollbar(receipt_frame, orient=tk.VERTICAL)
                style = ttk.Style()
                style.configure("Vertical.TScrollbar", troughcolor="gold", gripcount=0, gripmargin=0)

                scrollbar.configure(style="Vertical.TScrollbar", command=canvas.yview)
                scrollbar.place(relx=1, rely=0.1, relheight=0.95, anchor=tk.NE)

                canvas.configure(yscrollcommand=scrollbar.set)

                all_receipts = fetch_all_receipts()

                frame = tk.Frame(canvas, bg="green")
                canvas.create_window((0, 0), window=frame, anchor="nw")

                for idx, receipt in enumerate(all_receipts):
                    purchase_no = receipt[0]
                    field_id = receipt[1]

                    inner_frame = tk.LabelFrame(frame, text=f"Receipt {idx + 1}", bg="green", fg="white",font=("Arial", 10, "bold"))
                    inner_frame.pack(pady=10, padx=18, fill=tk.X)

                    receipt_label_field_id = tk.Label(inner_frame, text=f"Order ID: {receipt[0]}", bg="green", fg="white",font=("Arial", 10, "bold"))
                    receipt_label_field_id.pack(pady=5)

                    receipt_label_field_id = tk.Label(inner_frame, text=f"Field ID: {receipt[1]}",bg="green", fg="white",font=("Arial", 10, "bold"))
                    receipt_label_field_id.pack(pady=5)

                    receipt_label_address = tk.Label(inner_frame, text=f"Address: {receipt[2]}",bg="green", fg="white",font=("Arial", 10, "bold"))
                    receipt_label_address.pack(pady=5)

                    receipt_label_phone_number = tk.Label(inner_frame, text=f"Phone Number: {receipt[3]}",bg="green", fg="white",font=("Arial", 10, "bold"))
                    receipt_label_phone_number.pack(pady=5)

                    receipt_label_recipient_name = tk.Label(inner_frame, text=f"Recipient Name: {receipt[4]}",bg="green", fg="white",font=("Arial", 10, "bold"))
                    receipt_label_recipient_name.pack(pady=5)

                    receipt_label_purchase_date = tk.Label(inner_frame, text=f"Purchase Date: {receipt[5]}",bg="green", fg="white",font=("Arial", 10, "bold"))
                    receipt_label_purchase_date.pack(pady=5)

                    remove_button = tk.Button(
                        inner_frame,
                        text="Deliver Item",background="#E8D350",
                                          font=("Arial", 9, 'bold'),
                        command=lambda i=purchase_no, f=field_id, current_frame=inner_frame,
                                       t=tree_1: confirm_remove_receipt(
                            i, f, current_frame, t
                        ),
                    )
                    remove_button.pack(pady=5)

                def on_frame_configure(canvas):
                    canvas.configure(scrollregion=canvas.bbox("all"))

                frame.bind("<Configure>", lambda event, canvas=canvas: on_frame_configure(canvas))


            def confirm_remove_receipt(purchase_no, field_id, current_frame, tree_1):
                confirm = messagebox.askquestion(
                    "Confirm Receipt Removal",
                    f"Are you sure you want to deliver Field ID: {field_id}?",
                )
                if confirm == "yes":
                    remove_receipt_and_admin(purchase_no, field_id, current_frame, tree_1)

            purchase_history_button = tk.Button(Admin_window, text="CUSTOMER ORDER HISTORY", command=open_purchase_history_window,
                                                font=("Arial", 10, "bold"), background="#E8D350")
            purchase_history_button.place(x=40, y=15)

            view_all_receipts(Admin_window, tree_1)


            def update_labels():
                total_field_size = get_total_field_size()
                total_profit = get_total_Profit()

                field_size_label.config(text=f"Total Field Size: {total_field_size} acres | Total Profit: {total_profit}₱")

                total_stock = get_total_stock()
                total_expenses = get_total_Expenses()
                profit_label.config(text=f"  Total Stock  : {total_stock} bushels | Total Expenses: {total_expenses}₱")

            def on_button_click():
                if frame.winfo_ismapped():
                    frame.place_forget()
                else:
                    update_labels()
                    frame.place(x=400, y=312)

            frame = tk.Frame(Admin_window, width=200, height=100, highlightbackground="gold", highlightthickness=3,
                             background="green")

            field_size_label = tk.Label(frame, fg="white", bg='green', font=("Helvetica", 12, 'bold'),)
            field_size_label.pack(anchor="w")

            profit_label = tk.Label(frame, fg="white", bg='green', font=("Helvetica", 12, 'bold'))
            profit_label.pack()

            update_labels()

            update_button = tk.Button(Admin_window, text="Total Information", font=("Arial", 10, "bold"),
                                      background="#E8D350", command=on_button_click)
            update_button.place(x=275, y=325)

            hide_and_show(window, Admin_window)
            Admin_window.mainloop()

    def toggle_show_password():
        if show_password_var.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    window = Tk()
    window_width = 500
    window_height = 500
    window.title("THE CORN COMPANY")
    icon = PhotoImage(file='corny.png')
    window.iconphoto(True, icon)
    window.resizable(width=False, height=False)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_axis = (screen_width / 2) - (window_width / 2)
    y_axis = (screen_height / 2) - (window_height / 2)
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, int(x_axis), int(y_axis)))
    window.config(background="yellowgreen")

    original_image = PhotoImage(file='—Pngtree—corn healthy fresh starch_6308916.png')
    small_image = original_image.subsample(20, 20)

    label = Label(window, text="CORN COMPANY", font=('Times New Roman', 25, 'bold'), fg='black', bg='yellowgreen',
                  relief=RAISED, bd=4, padx=20, pady=8, image=small_image, compound='right')
    label.place(x=20, y=10)

    username_label = Label(window, text="Username:", font=('Aharoni', 17, 'bold'), bg='yellowgreen')
    username_label.place(x=10, y=202)
    username_entry = Entry(window, font=("Arial", 20), bg='yellow')
    username_entry.place(x=140, y=200)

    password_label = Label(window, text="Password:", font=('Aharoni', 17, 'bold'), bg='yellowgreen')
    password_label.place(x=10, y=251)
    password_entry = Entry(window, font=("Arial", 20), show="*", bg='yellow')
    password_entry.place(x=140, y=250)

    show_password_var = tk.BooleanVar()
    show_password_checkbox = ttk.Checkbutton(window, text="Show Password", variable=show_password_var,
                                             command=toggle_show_password, style='TCheckbutton')
    show_password_checkbox.place(x=140, y=290)

    style = ttk.Style()
    style.configure('TCheckbutton', background="yellowgreen", highlightbackground="yellowgreen",
                    highlightcolor="yellowgreen")

    LogIn_button = Button(window, text="Log in", command=signin, font=("Arial", 12, 'bold'), bg='yellow')
    LogIn_button.place(x=200, y=320)

    Signup_button = Button(window, text="Sign up", command=signup, font=("Arial", 12, 'bold'), bg='yellow')
    Signup_button.place(x=320, y=320)

    Admin_button = Button(window, text="Admin Access", command=admin_login1, font=("Arial", 10, 'bold'), bg='gold')
    Admin_button.place(x=390, y=465)

    change_password_label = Label(window, text="Forgot Password?", font=("Arial", 10, 'bold'), fg='black',bg='yellowgreen',
                                  cursor='hand2')
    change_password_label.place(x=240, y=380)
    change_password_label.bind("<Button-1>", lambda event: change_password_window())

    window.mainloop()


create_main_window()
