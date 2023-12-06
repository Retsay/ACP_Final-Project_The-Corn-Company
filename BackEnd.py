import pymysql
import logging
from tkinter import messagebox
from hashlib import sha256

conn = pymysql.connect(
    host="localhost",
    user="Yaster",
    password="yaster18.",
    database="sheesh"
)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='app.log', level=logging.ERROR)

def get_total_Profit():
    try:
        with conn.cursor() as cursor:
            query = "SELECT SUM(Profit) FROM business_data"
            cursor.execute(query)
            total_profit = cursor.fetchone()[0]
            return total_profit if total_profit else 0
    except pymysql.Error as e:
        logger.error(f"MySQL Query Error: {e}")
        return 0

def get_total_Expenses():
    try:
        with conn.cursor() as cursor:
            query = "SELECT SUM(expense) FROM business_data"
            cursor.execute(query)
            total_expenses = cursor.fetchone()[0]
            return total_expenses if total_expenses else 0
    except pymysql.Error as e:
        logger.error(f"MySQL Query Error: {e}")
        return 0

def get_total_field_size():
    try:
        with conn.cursor() as cursor:
            query = "SELECT SUM(Field_Size) FROM admin_data"
            cursor.execute(query)
            total_field_size = cursor.fetchone()[0]
            return total_field_size if total_field_size else 0
    except pymysql.Error as e:
        logger.error(f"MySQL Query Error: {e}")
        return 0

def get_total_stock():
    try:
        with conn.cursor() as cursor:
            query = "SELECT SUM(Stock) FROM admin_data"
            cursor.execute(query)
            total_stock = cursor.fetchone()[0]
            return total_stock if total_stock else 0
    except pymysql.Error as e:
        logger.error(f"MySQL Query Error: {e}")
        return 0

def delete_purchase_history(purchase_id):
    global conn
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PurchaseHistory WHERE PurchaseID = %s", (purchase_id,))
        conn.commit()
    except pymysql.Error as e:
        logging.error(f"MySQL Delete Error: {e}")
        raise
    except Exception as ex:
        logging.exception("An unexpected error occurred:")
        raise
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

def fetch_purchase_history_data(search_term=None):
    global conn
    try:
        cursor = conn.cursor()

        if search_term:
            cursor.execute("SHOW COLUMNS FROM PurchaseHistory")
            columns = [column[0] for column in cursor.fetchall()]
            where_clause = " OR ".join([f"{column} LIKE %s" for column in columns])
            query = f"SELECT * FROM PurchaseHistory WHERE {where_clause}"
            cursor.execute(query, tuple([f"%{search_term}%" for _ in columns]))

        else:
            cursor.execute("SELECT * FROM PurchaseHistory")

        data = cursor.fetchall()

        return data

    except pymysql.Error as e:
        logging.error(f"MySQL Fetch Error: {e}")
        return None
    except Exception as ex:
        logging.exception("An unexpected error occurred:")
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()



def update_business(item_id, month, profit, expense):
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE business_data SET month=%s, profit=%s, expense=%s WHERE id=%s",
                           (month, profit, expense, item_id))
            conn.commit()
            return True
    except pymysql.Error as e:
        messagebox.showerror("Error", f"MySQL Delete Error: {e}")
        return False

def deletebusiness(listbox):
    global conn
    selected_item = listbox.get(listbox.curselection())
    item_id = selected_item.split("-")[0].strip().split(":")[1].strip()
    listbox.delete(listbox.curselection())

    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM business_data WHERE id=%s", (item_id,))
            conn.commit()
            messagebox.showinfo("Success", "Item deleted successfully.")
    except pymysql.Error as e:
        messagebox.showerror("Error", f"MySQL Delete Error: {e}")


def insert_databusiness(date, profit, expense):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO business_data (month, profit, expense)
                VALUES (%s, %s, %s)
            ''', (date, profit, expense))
            conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully.")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid Input: {e}")


def fetch_databusiness():
    try:
        with conn.cursor() as cursor:  # Make sure 'conn' is defined and available here
            cursor.execute('SELECT * FROM business_data')
            data = cursor.fetchall()
            return data
    except Exception as e:
        print(f"Error: {e}")
        return []

def remove_admin_data(field_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Admin_Data WHERE FieldId=%s", (field_id,))
    conn.commit()
    cursor.close()

def userupdate(PurchaseNo, new_values):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE CustomerPurchase SET Address=%s, PhoneNumber=%s, RecipientName=%s, PurchaseDate=%s WHERE FieldID=%s",
            (new_values[1], new_values[2], new_values[3], new_values[4], PurchaseNo)
        )
        conn.commit()
        cursor.close()
        admin_data = fetch_data(new_values[0])
        update_receipt(admin_data, *new_values)
        messagebox.showinfo("Success", "Record updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def fetch_data1(field_id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM CustomerPurchase WHERE FieldID = '{field_id}'")
    return cursor.fetchone()

def update_info(field_id, new_values):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE CustomerPurchase SET Address=%s, PhoneNumber=%s, RecipientName=%s, PurchaseDate=%s WHERE FieldID=%s",
        (new_values[0], new_values[1], new_values[2], new_values[3], field_id)
    )
    conn.commit()
    cursor.close()
    return fetch_data1(field_id)

def remove_receipt(purchase_no):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CustomerPurchase WHERE PurchaseNo = %s", (purchase_no,))
    conn.commit()
    cursor.close()

def remove_admin_data(field_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Admin_Data WHERE FieldId=%s", (field_id,))
    conn.commit()
    cursor.close()

def fetch_all_receipts():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CustomerPurchase")
    all_receipts = cursor.fetchall()
    cursor.close()
    return all_receipts

def update_customer_purchase(field_id, new_values):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE CustomerPurchase SET Address=%s, PhoneNumber=%s, RecipientName=%s, PurchaseDate=%s WHERE FieldID=%s",
            (new_values[0], new_values[1], new_values[2], new_values[3], field_id)
        )
        conn.commit()
        cursor.close()
        return fetch_data(field_id)
    except Exception as e:
        return str(e)

def insert_customer_purchase(field_id, field_size, planted_date, harvest_date, stock, address, phone_number, recipient_name, purchase_date):
    try:
        mycursor = conn.cursor()
        sql = "INSERT INTO PurchaseHistory (FieldID, FieldSize, PlantedDate, HarvestDate, Stock, Address, PhoneNumber, RecipientName, PurchaseDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (field_id, field_size, planted_date, harvest_date, stock, address, phone_number, recipient_name, purchase_date)
        mycursor.execute(sql, val)
        conn.commit()
        mycursor.close()
        return fetch_data(field_id)  # Assuming fetch_data is defined
    except Exception as e:
        return str(e)

def insert_data1(field_id, address, phone_number, recipient_name, purchase_date):
    mycursor = conn.cursor()
    sql = "INSERT INTO CustomerPurchase (FieldID, Address, PhoneNumber, RecipientName, PurchaseDate) VALUES (%s, %s, %s, %s, %s)"
    val = (field_id, address, phone_number, recipient_name, purchase_date)
    mycursor.execute(sql, val)
    conn.commit()
    mycursor.close()

def fetch_data(field_id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM admin_data WHERE FieldID = '{field_id}'")
    return cursor.fetchone()

def update_data(field_id, new_values): #sa edit
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE admin_data SET Field_Size=%s, PlantedDate=%s, HarvestDate=%s, Stock=%s WHERE FieldID=%s",
            (new_values[1], new_values[2], new_values[3], new_values[4], field_id)
        )
        conn.commit()
        cursor.close()
    except pymysql.Error as e:
        logger.error(f"MySQL Update Error: {e}")

#pang delete sa treeview kulang paaaaaa
def delete_item(tree):
    global conn
    selected_item = tree.focus()
    if selected_item:
        item_values = tree.item(selected_item)['values']
        item_id = item_values[0]
        tree.delete(selected_item)

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM admin_data WHERE FieldID=%s", (item_id,))
            conn.commit()
            cursor.close()
        except pymysql.Error as e:
            logger.error(f"MySQL Delete Error: {e}")
    else:
        messagebox.showerror("Error", "No item selected for deletion")

def insert_data(field_id, field_size, planted_date, harvest_date, stock):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO admin_data (FieldID, Field_Size, PlantedDate, HarvestDate, Stock) VALUES (%s, %s, %s, %s, %s)"
        val = (field_id, field_size, planted_date, harvest_date, stock)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
    except pymysql.Error as e:
        logger.error(f"MySQL Insert Error: {e}")

def is_field_id_existing(field_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin_data WHERE FieldID = %s", (field_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    except pymysql.Error as e:
        logger.error(f"MySQL Select Error: {e}")
        return False

def update_tree_1(tree):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin_data")
        rows = cursor.fetchall()
        for row in tree.get_children():
            tree.delete(row)
        for row in rows:
            tree.insert("", "end", values=row)
        cursor.close()
    except pymysql.Error as e:
        logging.error(f"MySQL Update Error: {e}")

def update_tree_2(tree):  # sa user
    global conn
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin_data")  # Replace with your actual table name
        rows = cursor.fetchall()
        for row in tree.get_children():
            tree.delete(row)
        for row in rows:
            tree.insert("", "end", values=row)
        cursor.close()
    except pymysql.Error as e:
        logger.error(f"MySQL Update Error: {e}")


def sorting_data(order, column): #admin/user sort
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM admin_data ORDER BY {column} {order};")
        return cursor.fetchall()
    except pymysql.Error as e:
        logger.error(f"MySQL Sorting Error: {e}")
        return None

def search_id(search_entry, tree):
    global conn
    try:
        search_value = search_entry.get()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin_data WHERE FieldID LIKE %s OR Field_Size LIKE %s OR PlantedDate LIKE %s OR HarvestDate LIKE %s OR ABS(Stock - %s) < 10",
                       (f'%{search_value}%', f'%{search_value}%', f'%{search_value}%', f'%{search_value}%', search_value))
        rows = cursor.fetchall()
        for row in tree.get_children():
            tree.delete(row)
        for row in rows:
            tree.insert("", "end", values=row)
        cursor.close()
    except pymysql.Error as e:
        logger.error(f"MySQL Search Error: {e}")

def mysql_change_password(username, new_password):
    global conn
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE user_namepass SET Password=%s WHERE UserName=%s", (new_password, username))
        conn.commit()
        return True  # Password change successful
    except pymysql.Error as e:
        messagebox.showerror("Error", f"MySQL Connection Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()

def mysqlconnect(username, password, mode):
    global conn
    cursor = None
    try:
        cursor = conn.cursor()
        if mode == "signup":
            cursor.execute("SELECT * FROM user_namepass WHERE UserName=%s", (username,))
            result = cursor.fetchone()
            if result:
                return False  # User already exists
            else:
                cursor.execute("INSERT INTO user_namepass (UserName, Password) VALUES (%s, %s)", (username, password))
                conn.commit()
                return True  # Signup successful

        elif mode == "signin":
            cursor.execute("SELECT * FROM user_namepass WHERE UserName=%s AND Password=%s", (username, password))
            if cursor.fetchone():
                return True  # Signin successful
            else:
                return False  # Incorrect credentials

    except pymysql.Error as e:
        messagebox.showerror("Error", f"MySQL Connection Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()

