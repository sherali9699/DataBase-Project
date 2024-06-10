import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDateEdit, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QGroupBox, QMessageBox, QDialog, QVBoxLayout, QLabel
from PyQt5.uic import loadUi
import pyodbc
import addmin_interface

 # Replace these with your own database connection details
server = ''
database = 'POSHAAK'  # Name of your Northwind database
use_windows_authentication = False  # Set to True to use Windows Authentication
username = 'sa'  # Specify a username if not using Windows Authentication
password = ''  # Specify a password if not using Windows Authentication

# # Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

class AdminView1(QMainWindow):
    def __init__(self):
        super(AdminView1, self).__init__() 
        
        # Creating a cursor to execute SQL queries
        # self.cursor = self.conn.cursor()
        connection = pyodbc.connect(connection_string)

        self.cursor = connection.cursor()
        # Loading the UI from the .ui file
        uic.loadUi("AdminView.ui", self)

        # Connecting buttons to their respective functions
        self.ClearButton.clicked.connect(self.clear_data)
        self.ShowButton.clicked.connect(self.show_data)
        self.BackButton.clicked.connect(self.hide)
        
        self.view_product=self.findChild(QPushButton,"ViewProductsButton")
        self.view_product.clicked.connect(self.open_products_screen)

        # # Connecting delete buttons to their respective functions
        self.OrdersDeleteButton.clicked.connect(self.delete_func)
        self.ShippersDeleteButton.clicked.connect(self.delete_func)
        self.CategoryDeleteButton.clicked.connect(self.delete_func)
        self.CustomersDeleteButton.clicked.connect(self.delete_func)
        self.DeliveryDeleteButton.clicked.connect(self.delete_func)

        # Connecting insert buttons to their respective functions
        self.ShipperInsertButton.clicked.connect(self.open_shipper_insert_window)
        self.CategoryInsertButton.clicked.connect(self.open_category_insert_window)
        self.DeliveryInsertButton.clicked.connect(self.open_delivery_insert_window)

        self.show_data()
    def delete_func(self):
            QMessageBox.warning(self, "Input Error", "You do not have permission to delete")
            return

    def open_products_screen(self):
        self.pro_screen = addmin_interface.UI()
        self.pro_screen.show()

    def clear_data(self):
        # Clearing data in all table widgets
        self.CategoriesTableWidget.setRowCount(0)
        self.OrdersTableWidget.setRowCount(0)
        self.CustomersTableWidget.setRowCount(0)
        self.ShippersTableWidget.setRowCount(0)
        self.DeliveryTableWidget.setRowCount(0)

    def show_data(self):
        # Clearing data before showing new data
        self.clear_data()

        # Retrieving data based on filters and populating table widgets
        self.show_categories()
        self.show_orders()
        self.show_customers()
        self.show_shippers()
        self.show_delivery_areas()

    def show_categories(self):
        # Getting the selected category from the CategoryComboBox
        selected_category = self.CategoryComboBox.currentText()

        # Constructing the SQL query based on the selected category
        if selected_category == "All":
            sql_query = "SELECT * FROM Categories"
        else:
            sql_query = f"SELECT * FROM Categories WHERE id = {selected_category}"

        # Executing the query and populating the CategoriesTableWidget
        self.cursor.execute(sql_query)
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.CategoriesTableWidget.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.CategoriesTableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def show_orders(self):
        # Getting the selected date from the OrdersDateEdit
        from_date = self.FromDateEdit.date().toString("dd-MM-yyyy")
        to_date =  self.ToDateEdit.date().toString("dd-MM-yyyy")
        # Constructing the SQL query based on the selected date
        if from_date== "01-01-2000" and to_date == "01-01-2000":
            sql_query = "SELECT * FROM Orders"
        else:
            sql_query = f"SELECT * FROM Orders WHERE order_date BETWEEN '{from_date}' AND '{to_date}'"

        # Executing the query and populating the OrdersTableWidget
        self.cursor.execute(sql_query)
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.OrdersTableWidget.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.OrdersTableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def show_customers(self):
        # Getting the entered CustomerID from the CustomerIDLineEdit
        customer_id_text = self.CustomerIDLineEdit.text()

        # Validate if customer_id_text is an integer
        try:
            customer_id = int(customer_id_text) if customer_id_text else None
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Customer ID should be a number.")
            return

        # Constructing the SQL query based on the entered CustomerID
        if customer_id is not None:
            sql_query = f"SELECT * FROM Customers WHERE id = {customer_id}"
        else:
            sql_query = "SELECT * FROM Customers"

        # Executing the query and populating the CustomersTableWidget
        self.cursor.execute(sql_query)
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.CustomersTableWidget.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.CustomersTableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def show_shippers(self):
        # Getting the entered ShipperID from the ShipperIDLineEdit
        shipper_id_text = self.ShipperIDLineEdit.text()

        # Validate if shipper_id_text is an integer
        try:
            shipper_id = int(shipper_id_text) if shipper_id_text else None
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Shipper ID should be a number.")
            return

        # Constructing the SQL query based on the entered ShipperID
        if shipper_id is not None:
            sql_query = f"SELECT * FROM Shippers WHERE id = {shipper_id}"
        else:
            sql_query = "SELECT * FROM Shippers"

        # Executing the query and populating the ShippersTableWidget
        self.cursor.execute(sql_query)
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.ShippersTableWidget.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.ShippersTableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def show_delivery_areas(self):
         # Getting the entered city from the CityLineEdit
        city = self.CityLineEdit.text()

        # Validate if city is a string
        if city and not isinstance(city, str):
            QMessageBox.warning(self, "Input Error", "City should be a string.")
            return

        # Constructing the SQL query based on the entered city
        if city:
            sql_query = f"SELECT * FROM [Delivery Areas] WHERE city LIKE '%{city}%'"
        else:
            sql_query = "SELECT * FROM [Delivery Areas]"

        # Executing the query and populating the DeliveryTableWidget
        self.cursor.execute(sql_query)
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.DeliveryTableWidget.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.DeliveryTableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def delete_selected_orders(self):
        # Get the selected row
        selected_row = self.OrdersTableWidget.currentRow()

        # Delete the selected row from the table widget and the database
        if selected_row != -1:
            order_id = self.OrdersTableWidget.item(selected_row, 0).text()  # Assuming ID is in the first column
            self.OrdersTableWidget.removeRow(selected_row)
            # self.delete_order_from_database(order_id)
            QMessageBox.information(self, "Delete Successful", "Order deleted successfully!")
        else:
            QMessageBox.warning(self, "Delete Warning", "Please select a row to delete.")

    # def delete_order_from_database(self, order_id):
    #     # Delete the order from the Orders table in the database
    #     sql_query = f"DELETE FROM Orders WHERE id = {order_id}"
    #     self.cursor.execute(sql_query)
    #     self.conn.commit()

    def delete_selected_shippers(self):
        # Get the selected row
        selected_row = self.ShippersTableWidget.currentRow()

        # Delete the selected row from the table widget and the database
        if selected_row != -1:
            shipper_id = self.ShippersTableWidget.item(selected_row, 0).text()  # Assuming ID is in the first column
            self.ShippersTableWidget.removeRow(selected_row)
            # self.delete_shipper_from_database(shipper_id)
            QMessageBox.information(self, "Delete Successful", "Shipper deleted successfully!")
        else:
            QMessageBox.warning(self, "Delete Warning", "Please select a row to delete.")

    # def delete_shipper_from_database(self, shipper_id):
    #     # Delete the shipper from the Shippers table in the database
    #     sql_query = f"DELETE FROM Shippers WHERE id = {shipper_id}"
    #     self.cursor.execute(sql_query)
    #     self.conn.commit()

    def delete_selected_categories(self):
        # Get the selected row
        selected_row = self.CategoriesTableWidget.currentRow()

        # Delete the selected row from the table widget and the database
        if selected_row != -1:
            category_id = self.CategoriesTableWidget.item(selected_row, 0).text()  # Assuming ID is in the first column
            self.CategoriesTableWidget.removeRow(selected_row)
            # self.delete_category_from_database(category_id)
            QMessageBox.information(self, "Delete Successful", "Category deleted successfully!")
        else:
            QMessageBox.warning(self, "Delete Warning", "Please select a row to delete.")

    # def delete_category_from_database(self, category_id):
    #     # Delete the category from the Categories table in the database
    #     sql_query = f"DELETE FROM Categories WHERE id = {category_id}"
    #     self.cursor.execute(sql_query)
    #     self.conn.commit()

    def delete_selected_customers(self):
        # Get the selected row
        selected_row = self.CustomersTableWidget.currentRow()

        # Delete the selected row from the table widget and the database
        if selected_row != -1:
            customer_id = self.CustomersTableWidget.item(selected_row, 0).text()  # Assuming ID is in the first column
            self.CustomersTableWidget.removeRow(selected_row)
            # self.delete_customer_from_database(customer_id)
            QMessageBox.information(self, "Delete Successful", "Customer deleted successfully!")
        else:
            QMessageBox.warning(self, "Delete Warning", "Please select a row to delete.")

    # def delete_customer_from_database(self, customer_id):
    #     # Delete the customer from the Customers table in the database
    #     sql_query = f"DELETE FROM Customers WHERE id = {customer_id}"
    #     self.cursor.execute(sql_query)
    #     self.conn.commit()

    def delete_selected_delivery_areas(self):
        # Get the selected row
        selected_row = self.DeliveryTableWidget.currentRow()

        # Delete the selected row from the table widget and the database
        if selected_row != -1:
            delivery_area_id = self.DeliveryTableWidget.item(selected_row, 0).text()  # Assuming ID is in the first column
            self.DeliveryTableWidget.removeRow(selected_row)
            # self.delete_delivery_area_from_database(delivery_area_id)
            QMessageBox.information(self, "Delete Successful", "Delivery Area deleted successfully!")
        else:
            QMessageBox.warning(self, "Delete Warning", "Please select a row to delete.")

    # def delete_delivery_area_from_database(self, delivery_area_id):
    #     # Delete the delivery area from the [Delivery Areas] table in the database
    #     sql_query = f"DELETE FROM [Delivery Areas] WHERE id = {delivery_area_id}"
    #     self.cursor.execute(sql_query)
    #     self.conn.commit()

    def open_shipper_insert_window(self):
        # Open the ShipperInsert window
        self.shipper_insert_window = ShipperInsertWindow(self)
        self.shipper_insert_window.show()

    def open_category_insert_window(self):
        # Open the CategoryInsert window
        self.category_insert_window = CategoryInsertWindow(self)
        self.category_insert_window.show()

    def open_delivery_insert_window(self):
        # Open the DeliveryInsert window
        self.delivery_insert_window = DeliveryInsertWindow(self)
        self.delivery_insert_window.show()

    def closeEvent(self, event):
        # Closing the database connection when the application is closed
        self.conn.close()
        event.accept()

class ShipperInsertWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ShipperInsertWindow, self).__init__(parent)
        loadUi("ShipperInsert.ui", self)

        # Connect button to function
        self.InsertButton.clicked.connect(self.insert_shipper)

        # Save the reference to the parent
        self.parent = parent

    def insert_shipper(self):
        # Get data from line edits
        shipper_id = self.IDLineEdit.text()
        shipper_name = self.NameLineEdit.text()
        contact_number = self.ContactLineEdit.text()
        email = self.EmailLineEdit.text()

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Validate data types and insert into the Shippers table
        try:
            shipper_id = int(shipper_id)
            contact_number = int(contact_number)
            
            # Check length of contact number and ID
            if len(str(contact_number)) != 13:
                QMessageBox.warning(self, "Insert Warning", "Contact number should be 13 digits.")
                return
            
            if len(str(shipper_id)) > 3:
                QMessageBox.warning(self, "Insert Warning", "ID should be maximum 3 digits.")
                return

            # Ensure the name contains only letters and spaces
            if not shipper_name.replace(' ', '').isalpha():
                QMessageBox.warning(self, "Insert Warning", "Name should contain only letters and spaces.")
                return

            # Ensure other validations as needed for your specific case
            if not email.endswith("@gmail.com"):
                QMessageBox.warning(self, "Insert Warning", "Email should end with '@gmail.com'.")
                return
                
            # Check if the ID already exists in the table
            cursor.execute(f"SELECT id FROM Shippers WHERE id = {shipper_id}")
            existing_id = cursor.fetchone()

            if existing_id:
                # ID already exists, show an error message
                QMessageBox.warning(self, "Insert Warning", f"Shipper with ID {shipper_id} already exists.")
                return        

            # Insert data into the Shippers table
            sql_query = f"INSERT INTO Shippers (id, name, contact_number, email) VALUES ({shipper_id}, '{shipper_name}', {contact_number}, '{email}')"
            cursor.execute(sql_query)
            connection.commit()

            QMessageBox.information(self, "Insert Successful", "Shipper inserted successfully!")
            self.close()

        except ValueError:
            QMessageBox.warning(self, "Insert Warning", "Invalid data types. Please enter valid data.")


class CategoryInsertWindow(QMainWindow):
    def __init__(self, parent=None):
        super(CategoryInsertWindow, self).__init__(parent)
        loadUi("CategoryInsert.ui", self)

        # Connect button to function
        self.InsertButton.clicked.connect(self.insert_category)
        self.parent = parent  # Save the reference to the parent

    def insert_category(self):
        # Get data from line edits
        category_id = self.IDLineEdit.text()
        category_name = self.NameLineEdit.text()
        category_description = self.DesLineEdit.text()
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Validate data types and insert into the Categories table
        try:
            category_id = int(category_id)
            
            # Check maximum category ID
            if category_id > 1000:
                QMessageBox.warning(self, "Insert Warning", "Category ID should be at most 1000.")
                return

            # Ensure the name contains only letters and spaces
            if not category_name.replace(' ', '').isalpha():
                QMessageBox.warning(self, "Insert Warning", "Category name should contain only letters and spaces.")
                return

            # Check if the ID already exists in the table
            cursor.execute(f"SELECT id FROM Categories WHERE id = {category_id}")
            existing_id = cursor.fetchone()

            if existing_id:
                # ID already exists, show an error message
                QMessageBox.warning(self, "Insert Warning", f"Category with ID {category_id} already exists.")
                return  

            # Insert data into the Categories table
            sql_query = f"INSERT INTO Categories (id, name, description) VALUES ({category_id}, '{category_name}', '{category_description}')"
            cursor.execute(sql_query)
            connection.commit()

            QMessageBox.information(self, "Insert Successful", "Category inserted successfully!")
            self.close()

        except ValueError:
            QMessageBox.warning(self, "Insert Warning", "Invalid data types. Please enter valid data.")


class DeliveryInsertWindow(QMainWindow):
    def __init__(self, parent=None):
        super(DeliveryInsertWindow, self).__init__(parent)
        loadUi("DeliveryInsert.ui", self)

        # Connect button to function
        self.InsertButton.clicked.connect(self.insert_delivery_area)
        self.parent = parent  # Save the reference to the parent

    def insert_delivery_area(self):
        # Get data from line edits
        city = self.CityLineEdit.text()
        area = self.AreaLineEdit.text()
        country = self.CountryLineEdit.text()
        postal_code = self.PostalLineEdit.text()
        delivery_charges = self.ChargesLineEdit.text()
        possible = self.PossibleLineEdit.text()
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Validate data types and insert into the [Delivery Areas] table
        try:
            delivery_charges = float(delivery_charges)  # Assuming charges are in float format
            # Ensure other validations as needed for your specific case

            # Insert data into the [Delivery Areas] table
            sql_query = f"INSERT INTO [Delivery Areas] (city, area, country, postal_code, delivery_charges, possible) " \
                        f"VALUES ('{city}', '{area}', '{country}', '{postal_code}', {delivery_charges}, {possible})"
            cursor.execute(sql_query)
            connection.commit()

            QMessageBox.information(self, "Insert Successful", "Delivery Area inserted successfully!")
            self.close()

        except ValueError:
            QMessageBox.warning(self, "Insert Warning", "Invalid data types. Please enter valid data.")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = AdminView()
#     window.show()
#     sys.exit(app.exec())

