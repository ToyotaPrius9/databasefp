import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox


def connect_to_database():
    return mysql.connector.connect(host='localhost', user='root', password='', database='databasetek', autocommit=True)



class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database ADMIN GUI")

        main_frame = ttk.Frame(root, padding="150")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create buttons for various operations
        
        # Viewing
        view_items_btn = ttk.Button(main_frame, text="View Items", command=self.handle_view_items)
        view_items_btn.grid(row=0, column=0, padx=10, pady=10)

        view_suppliers_btn = ttk.Button(main_frame, text="View Suppliers", command=self.handle_view_suppliers)
        view_suppliers_btn.grid(row=1, column=0, padx=10, pady=10)

        view_customers_btn = ttk.Button(main_frame, text="View Customers", command=self.handle_view_customers)
        view_customers_btn.grid(row=2, column=0, padx=10, pady=10)

        view_employees_btn = ttk.Button(main_frame, text="View Employees", command=self.handle_view_employees)
        view_employees_btn.grid(row=3, column=0, padx=10, pady=10)

        view_sale_orders_btn = ttk.Button(main_frame, text="View Sale Orders", command=self.handle_view_sale_orders)
        view_sale_orders_btn.grid(row=4, column=0, padx=10, pady=10)

        view_supply_orders_btn = ttk.Button(main_frame, text="View Supply Orders", command=self.handle_view_supply_orders)
        view_supply_orders_btn.grid(row=5, column=0, padx=10, pady=10)

        view_sales_btn = ttk.Button(main_frame, text="View Sales History", command=self.handle_view_sales)
        view_sales_btn.grid(row=6, column=0, padx=10, pady=10)

        view_purchase_btn = ttk.Button(main_frame, text="View Purchase History", command=self.handle_view_purchases)
        view_purchase_btn.grid(row=7, column=0, padx=10, pady=10)

        # Inserting
        insert_customer_btn = ttk.Button(main_frame, text="Insert New Customer", command=self.handle_insert_customer)
        insert_customer_btn.grid(row=0, column=1, padx=10, pady=10)

        insert_item_btn = ttk.Button(main_frame, text="Insert New Item", command=self.handle_insert_item)
        insert_item_btn.grid(row=1, column=1, padx=10, pady=10)

        new_supplier_btn = ttk.Button(main_frame, text="Insert New Supplier", command=self.handle_insert_supplier)
        new_supplier_btn.grid(row=2, column=1, padx=10, pady=10)

        new_employee_btn = ttk.Button(main_frame, text="Insert New Employee", command=self.handle_insert_employee)
        new_employee_btn.grid(row=3, column=1, padx=10, pady=10)

        # Removing

        remove_supplier_btn = ttk.Button(main_frame, text="Remove Supplier", command=self.handle_remove_supplier)
        remove_supplier_btn.grid(row=0, column=2, padx=10, pady=10)

        remove_employee_btn = ttk.Button(main_frame, text="Remove Employee", command=self.handle_remove_employee)
        remove_employee_btn.grid(row=1, column=2, padx=10, pady=10)

        # Buying Supplies
        buy_supplies_btn = ttk.Button(main_frame, text="Buy Supplies", command=self.handle_buy_supplies)
        buy_supplies_btn.grid(row=4, column=1, padx=10, pady=10)

        # Selling
        sale_btn = ttk.Button(main_frame, text="New Sale", command=self.handle_make_sale)
        sale_btn.grid(row=5, column=1, padx=10, pady=10)

       



    def create_menus(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.destroy)

    def show_message(self, message):
        messagebox.showinfo("Message", message)

    def handle_view_items(self):
        # Connect
        with connect_to_database() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT item_name, item_weight, item_price, item_quantity FROM items")
                    items = cursor.fetchall()

                    # Create a new Toplevel window for displaying items
                    items_window = tk.Toplevel(self.root)
                    items_window.title("Items List")

                    # Create a text widget to display items
                    items_text = tk.Text(items_window, wrap=tk.WORD)
                    items_text.pack(expand=True, fill=tk.BOTH)

                    # Iterate through items and append to the text widget
                    for index, item in enumerate(items, start=1):
                        items_text.insert(tk.END, f"{index}. Name: {item[0]}\n")
                        items_text.insert(tk.END, f"   Weight: {item[1]} Grams\n")
                        items_text.insert(tk.END, f"   Price: {item[2]} Rupiah\n")
                        items_text.insert(tk.END, f"   Stock: {item[3]} Units\n")
                        items_text.insert(tk.END, "----------------------------------------------\n")

                    # Make the text widget read-only
                    items_text.config(state=tk.DISABLED)


    def handle_view_suppliers(self):
    # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM suppliers")
                suppliers = cursor.fetchall()

                # Create a new Toplevel window for displaying suppliers
                suppliers_window = tk.Toplevel(self.root)
                suppliers_window.title("Suppliers List")

                # Create a text widget to display suppliers
                suppliers_text = tk.Text(suppliers_window, wrap=tk.WORD)
                suppliers_text.pack(expand=True, fill=tk.BOTH)

                # Iterate through suppliers and append to the text widget
                for index, supplier in enumerate(suppliers, start=1):
                    suppliers_text.insert(tk.END, f"{index}. Supplier ID: {supplier[0]}\n")
                    suppliers_text.insert(tk.END, f"   Supplier Name: {supplier[1]}\n")
                    suppliers_text.insert(tk.END, f"   Email: {supplier[2]}\n")
                    suppliers_text.insert(tk.END, f"   Address: {supplier[3]}\n")
                    suppliers_text.insert(tk.END, f"   Phone Number: {supplier[4]}\n")
                    suppliers_text.insert(tk.END, "----------------------------------------------\n")

                # Make the text widget read-only
                suppliers_text.config(state=tk.DISABLED)

    def handle_view_customers(self):
    # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customers")
                customers = cursor.fetchall()

                # Create a new Toplevel window for displaying customers
                customers_window = tk.Toplevel(self.root)
                customers_window.title("Customers List")

                # Create a text widget to display customers
                customers_text = tk.Text(customers_window, wrap=tk.WORD)
                customers_text.pack(expand=True, fill=tk.BOTH)

                # Iterate through customers and append to the text widget
                for index, customer in enumerate(customers, start=1):
                    customers_text.insert(tk.END, f"\n{index}. Customer ID: {customer[0]}\n")
                    customers_text.insert(tk.END, f"   Name: {customer[1]}\n")
                    customers_text.insert(tk.END, f"   Email: {customer[2]}\n")
                    customers_text.insert(tk.END, f"   Address: {customer[3]}\n")
                    customers_text.insert(tk.END, f"   Phone Number: {customer[4]}\n")
                    customers_text.insert(tk.END, f"   Points: {customer[5]}\n")
                    customers_text.insert(tk.END, "\n----------------------------------------------\n")

                # Make the text widget read-only
                customers_text.config(state=tk.DISABLED)


    def handle_view_employees(self):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM employees")
                employees = cursor.fetchall()

                # Create a new Toplevel window for displaying employees
                employees_window = tk.Toplevel(self.root)
                employees_window.title("Employees List")

                # Create a text widget to display employees
                employees_text = tk.Text(employees_window, wrap=tk.WORD)
                employees_text.pack(expand=True, fill=tk.BOTH)

                # Iterate through employees and append to the text widget
                for index, employee in enumerate(employees, start=1):
                    employees_text.insert(tk.END, f"\n{index}. employee_id: {employee[0]}\n")
                    employees_text.insert(tk.END, f"   Employee Name: {employee[1]}\n")
                    employees_text.insert(tk.END, f"   Employee Role: {employee[2]}\n")
                    employees_text.insert(tk.END, "\n----------------------------------------------\n")

                # Make the text widget read-only
                employees_text.config(state=tk.DISABLED)

    def handle_view_sale_orders(self):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customer_orders")
                sale_orders = cursor.fetchall()

                # Create a new Toplevel window for displaying sale orders
                sale_orders_window = tk.Toplevel(self.root)
                sale_orders_window.title("Sale Orders List")

                # Create a text widget to display sale orders
                sale_orders_text = tk.Text(sale_orders_window, wrap=tk.WORD)
                sale_orders_text.pack(expand=True, fill=tk.BOTH)

                # Iterate through sale orders and append to the text widget
                for index, sale_order in enumerate(sale_orders, start=1):
                    sale_orders_text.insert(tk.END, f"\n{index}. Customer Order ID: {sale_order[0]}\n")
                    sale_orders_text.insert(tk.END, f"   Customer ID: {sale_order[1]}\n")
                    sale_orders_text.insert(tk.END, f"   Item ID: {sale_order[2]}\n")
                    sale_orders_text.insert(tk.END, f"   Item Price: {sale_order[3]}\n")
                    sale_orders_text.insert(tk.END, f"   Quantity Ordered: {sale_order[4]}\n")
                    sale_orders_text.insert(tk.END, f"   Sale Time: {sale_order[5]}\n")
                    sale_orders_text.insert(tk.END, f"   Points Used: {sale_order[7]}\n")
                    sale_orders_text.insert(tk.END, f"   Total Amount: {sale_order[6]}\n")
                    sale_orders_text.insert(tk.END, "\n----------------------------------------------\n")

                # Make the text widget read-only
                sale_orders_text.config(state=tk.DISABLED)

    def handle_view_supply_orders(self):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM supply_orderss")
                supply_orders = cursor.fetchall()

                # Create a new Toplevel window for displaying sale orders
                supply_orders_window = tk.Toplevel(self.root)
                supply_orders_window.title("Supply Orders List")

                # Create a text widget to display sale orders
                supply_orders_text = tk.Text(supply_orders_window, wrap=tk.WORD)
                supply_orders_text.pack(expand=True, fill=tk.BOTH)

                # Iterate through sale orders and append to the text widget
                for index, supply_orders in enumerate(supply_orders, start=1):
                    supply_orders_text.insert(tk.END, f"\n{index}. supply Order ID: {supply_orders[0]}\n")
                    supply_orders_text.insert(tk.END, f"   Supplier ID: {supply_orders[1]}\n")
                    supply_orders_text.insert(tk.END, f"   Item ID: {supply_orders[2]}\n")
                    supply_orders_text.insert(tk.END, f"   Purchase Time: {supply_orders[3]}\n")
                    supply_orders_text.insert(tk.END, f"   Quantity Ordered: {supply_orders[4]}\n")
                    supply_orders_text.insert(tk.END, f"   Purchase Total: {supply_orders[5]}\n")
                    supply_orders_text.insert(tk.END, "\n----------------------------------------------\n")

                # Make the text widget read-only
                supply_orders_text.config(state=tk.DISABLED)

    def handle_view_sales(self):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Select relevant columns from both tables using a JOIN operation
                cursor.execute("SELECT sales.customer_id, sales.sale_time, sales.customer_order_id, sales.sale_total, customers.customer_name "
                            "FROM sales "
                            "JOIN customers ON sales.customer_id = customers.customer_id")
                supply_orders = cursor.fetchall()

                # Create a new Toplevel window for displaying sale orders
                supply_orders_window = tk.Toplevel(self.root)
                supply_orders_window.title("Sales History")

                # Create a text widget to display sale orders
                supply_orders_text = tk.Text(supply_orders_window, wrap=tk.WORD)
                supply_orders_text.pack(expand=True, fill=tk.BOTH)

                # Iterate through sale orders and append to the text widget
                for index, supply_order in enumerate(supply_orders, start=1):
                    supply_orders_text.insert(tk.END, f"   Customer ID: {supply_order[0]}\n")
                    supply_orders_text.insert(tk.END, f"   Customer Name: {supply_order[4]}\n")
                    supply_orders_text.insert(tk.END, f"   Sale Time: {supply_order[1]}\n")
                    supply_orders_text.insert(tk.END, f"   Customer Order ID: {supply_order[2]}\n")
                    supply_orders_text.insert(tk.END, f"\n   Sale Total: {supply_order[3]}\n")
                    supply_orders_text.insert(tk.END, "\n----------------------------------------------\n")

                # Make the text widget read-only
                supply_orders_text.config(state=tk.DISABLED)

    def handle_view_purchases(self):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Select relevant columns from both tables using a JOIN operation
                cursor.execute("SELECT purchases.supplier_id, purchases.purchase_time, purchases.supply_order_id, purchases.purchase_total, suppliers.supplier_name "
                            "FROM purchases "
                            "JOIN suppliers ON purchases.supplier_id = suppliers.supplier_id")
                purchase_orders = cursor.fetchall()

                # Create a new Toplevel window for displaying sale orders
                purchase_orders_window = tk.Toplevel(self.root)
                purchase_orders_window.title("Sales History")

                # Create a text widget to display sale orders
                purchase_orders_text = tk.Text(purchase_orders_window, wrap=tk.WORD)
                purchase_orders_text.pack(expand=True, fill=tk.BOTH)

                # Iterate through sale orders and append to the text widget
                for index, supply_order in enumerate(purchase_orders, start=1):
                    purchase_orders_text.insert(tk.END, f"   Supplier ID: {supply_order[0]}\n")
                    purchase_orders_text.insert(tk.END, f"   Supplier Name: {supply_order[4]}\n")
                    purchase_orders_text.insert(tk.END, f"   Purchase Time: {supply_order[1]}\n")
                    purchase_orders_text.insert(tk.END, f"   Supply Order ID: {supply_order[2]}\n")
                    purchase_orders_text.insert(tk.END, f"\n   Purchase Total: {supply_order[3]}\n")
                    purchase_orders_text.insert(tk.END, "\n----------------------------------------------\n")

                # Make the text widget read-only
                purchase_orders_text.config(state=tk.DISABLED)


    def handle_insert_customer(self):
        # Create a new Toplevel window for the customer entry form
        customer_entry_window = tk.Toplevel(self.root)
        customer_entry_window.title("Insert Customer")

        # Create labels and entry widgets for customer information
        name_label = ttk.Label(customer_entry_window, text="Name:")
        name_label.grid(row=0, column=0, padx=7, pady=7)
        name_entry = ttk.Entry(customer_entry_window)
        name_entry.grid(row=0, column=1, padx=7, pady=7)

        email_label = ttk.Label(customer_entry_window, text="Email:")
        email_label.grid(row=1, column=0, padx=7, pady=7)
        email_entry = ttk.Entry(customer_entry_window)
        email_entry.grid(row=1, column=1, padx=7, pady=7)

        phone_label = ttk.Label(customer_entry_window, text="Phone Number:")
        phone_label.grid(row=2, column=0, padx=7, pady=7)
        phone_entry = ttk.Entry(customer_entry_window)
        phone_entry.grid(row=2, column=1, padx=7, pady=7)

        address_label = ttk.Label(customer_entry_window, text="Address:")
        address_label.grid(row=3, column=0, padx=7, pady=7)
        address_entry = ttk.Entry(customer_entry_window)
        address_entry.grid(row=3, column=1, padx=7, pady=7)

        # Create a button to submit the customer information
        submit_button = ttk.Button(
            customer_entry_window, text="Insert Customer", command=lambda: self.insert_customer_to_database(
                name_entry.get(), email_entry.get(), phone_entry.get(), address_entry.get(), customer_entry_window
            )
        )
        submit_button.grid(row=4, columnspan=2, padx=5, pady=10)

    def insert_customer_to_database(self, name, email, phone_number, address, window):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO customers (customer_name, customer_email, customer_phone_number, customer_address) VALUES (%s, %s, %s, %s)"
                values = (name, email, phone_number, address)
                cursor.execute(query, values)
                self.show_message("Customer inserted successfully.")
                # Close the customer entry window after insertion
                window.destroy()

    
    def handle_insert_item(self):
        # Create a new Toplevel window for the item entry form
        item_entry_window = tk.Toplevel(self.root)
        item_entry_window.title("Insert Item")

        # Create labels and entry widgets for item information
        name_label = ttk.Label(item_entry_window, text="Name:")
        name_label.grid(row=0, column=0, padx=7, pady=7)
        name_entry = ttk.Entry(item_entry_window)
        name_entry.grid(row=0, column=1, padx=7, pady=7)

        weight_label = ttk.Label(item_entry_window, text="Weight:")
        weight_label.grid(row=1, column=0, padx=7, pady=7)
        weight_entry = ttk.Entry(item_entry_window)
        weight_entry.grid(row=1, column=1, padx=7, pady=7)

        price_label = ttk.Label(item_entry_window, text="Price:")
        price_label.grid(row=2, column=0, padx=7, pady=7)
        price_entry = ttk.Entry(item_entry_window)
        price_entry.grid(row=2, column=1, padx=7, pady=7)

        quantity_label = ttk.Label(item_entry_window, text="Quantity:")
        quantity_label.grid(row=3, column=0, padx=7, pady=7)
        quantity_entry = ttk.Entry(item_entry_window)
        quantity_entry.grid(row=3, column=1, padx=7, pady=7)

        # Create a button to submit the item information
        submit_button = ttk.Button(
            item_entry_window, text="Insert Item", command=lambda: self.insert_item_to_database(
                name_entry.get(), weight_entry.get(), price_entry.get(), quantity_entry.get(), item_entry_window
            )
        )
        submit_button.grid(row=4, columnspan=2, padx=5, pady=10)

    def insert_item_to_database(self, name, weight, price, quantity, window):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO items (item_name, item_weight, item_price, item_quantity) VALUES (%s, %s, %s, %s)"
                values = (name, float(weight), float(price), int(quantity))
                cursor.execute(query, values)
                self.show_message("Item inserted successfully.")
                # Close the item entry window after insertion
                window.destroy()



    def handle_insert_supplier(self):
        # Create a new Toplevel window for the supplier entry form
        supply_entry_window = tk.Toplevel(self.root)
        supply_entry_window.title("Insert New Supplier")

        # Create labels and entry widgets for supplier information
        name_label = ttk.Label(supply_entry_window, text="Supplier Name:")
        name_label.grid(row=0, column=0, padx=7, pady=7)
        name_entry = ttk.Entry(supply_entry_window)
        name_entry.grid(row=0, column=1, padx=7, pady=7)

        email_label = ttk.Label(supply_entry_window, text="Email:")
        email_label.grid(row=1, column=0, padx=7, pady=7)
        email_entry = ttk.Entry(supply_entry_window)
        email_entry.grid(row=1, column=1, padx=7, pady=7)

        address_label = ttk.Label(supply_entry_window, text="Address:")
        address_label.grid(row=2, column=0, padx=7, pady=7)
        address_entry = ttk.Entry(supply_entry_window)
        address_entry.grid(row=2, column=1, padx=7, pady=7)

        phone_number_label = ttk.Label(supply_entry_window, text="Phone Number:")
        phone_number_label.grid(row=3, column=0, padx=7, pady=7)
        phone_number_entry = ttk.Entry(supply_entry_window)
        phone_number_entry.grid(row=3, column=1, padx=7, pady=7)

        # Create a button to submit the supplier information
        submit_button = ttk.Button(
            supply_entry_window, text="Insert Supplier", command=lambda: self.insert_supplier_to_database(
                name_entry.get(), email_entry.get(), address_entry.get(), phone_number_entry.get(), supply_entry_window
            )
        )
        submit_button.grid(row=4, columnspan=2, padx=5, pady=10)

    def insert_supplier_to_database(self, name, email, address, phone_number, window):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO suppliers (`supplier_name`, supplier_email, supplier_address, supplier_phone_number) VALUES (%s, %s, %s, %s)"
                values = (name, email, address, phone_number)
                cursor.execute(query, values)
                self.show_message("Supplier inserted successfully.")
               # Close the supply entry window after insertion
            window.destroy()


    def handle_insert_employee(self):
        # Connect
            with connect_to_database() as connection:
                with connection.cursor() as cursor:
                    # Create a new Toplevel window for the employee entry form
                    roles_entry_window = tk.Toplevel(self.root)
                    roles_entry_window.title("New Employee!")

                    # Create labels and entry widgets for employee information
                    name_label = ttk.Label(roles_entry_window, text="Name:")
                    name_label.grid(row=0, column=0, padx=7, pady=7)
                    name_entry = ttk.Entry(roles_entry_window)
                    name_entry.grid(row=0, column=1, padx=7, pady=7)

                    # Fetch the list of roles
                    cursor.execute("SELECT `employee_role` FROM employees")
                    roles = cursor.fetchall()

                    # Display the list of roles in a dropdown
                    roles_label = ttk.Label(roles_entry_window, text="Select Role:")
                    roles_label.grid(row=2, column=0, padx=7, pady=7)

                    roles_var = tk.StringVar()
                    roles_dropdown = ttk.Combobox(roles_entry_window, textvariable=roles_var, state="readonly")
                    roles_dropdown["values"] = [f"{roles[0]}" for roles in roles]
                    roles_dropdown.grid(row=2, column=1, padx=7, pady=7)


                    submit_button = ttk.Button(
                        roles_entry_window, text="Create Employee", command=lambda: self.insert_employee_to_database(
                            name_entry.get(), roles_var.get(), roles_entry_window
                        )
                    )
                    submit_button.grid(row=4, columnspan=2, padx=5, pady=10)

    def insert_employee_to_database(self, name, role, window):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:

                query = "INSERT INTO employees (`employee_name`, `employee_role`) VALUES (%s, %s)"
                values = (name, role)
                cursor.execute(query, values)
                self.show_message("New employee inserted successfully.")
            
            # Close the employee entry window after insertion
            window.destroy()


#################################### BUY #########################################
            

    def handle_buy_supplies(self):
        # Connect
            with connect_to_database() as connection:
                with connection.cursor() as cursor:
                    # Create a new Toplevel window for the supply order entry form
                    supply_order_entry_window = tk.Toplevel(self.root)
                    supply_order_entry_window.title("Buy Supplies")

                    # Fetch the list of suppliers
                    cursor.execute("SELECT `supplier_id`, `supplier_name` FROM suppliers")
                    suppliers = cursor.fetchall()

                    # Display the list of suppliers in a dropdown
                    supplier_label = ttk.Label(supply_order_entry_window, text="Select Supplier:")
                    supplier_label.grid(row=0, column=0, padx=7, pady=7)

                    supplier_var = tk.StringVar()
                    supplier_dropdown = ttk.Combobox(supply_order_entry_window, textvariable=supplier_var, state="readonly")
                    supplier_dropdown["values"] = [f"{supplier[0]}: {supplier[1]}" for supplier in suppliers]
                    supplier_dropdown.grid(row=0, column=1, padx=7, pady=7)

                    # Fetch the list of items
                    cursor.execute("SELECT `item_id`, `item_name` FROM items")
                    items = cursor.fetchall()

                    # Display the list of items in a dropdown
                    item_id_label = ttk.Label(supply_order_entry_window, text="Select Item:")
                    item_id_label.grid(row=1, column=0, padx=7, pady=7)

                    item_id_var = tk.StringVar()
                    item_id_dropdown = ttk.Combobox(supply_order_entry_window, textvariable=item_id_var, state="readonly")
                    item_id_dropdown["values"] = [f"{item[0]}: {item[1]}" for item in items]
                    item_id_dropdown.grid(row=1, column=1, padx=7, pady=7)

                    # Entry widgets for user input
                    quantity_label = ttk.Label(supply_order_entry_window, text="Quantity:")
                    quantity_label.grid(row=2, column=0, padx=7, pady=7)
                    quantity_entry = ttk.Entry(supply_order_entry_window)
                    quantity_entry.grid(row=2, column=1, padx=7, pady=7)

                    purchase_total_label = ttk.Label(supply_order_entry_window, text="Purchase Total:")
                    purchase_total_label.grid(row=3, column=0, padx=7, pady=7)
                    purchase_total_entry = ttk.Entry(supply_order_entry_window)
                    purchase_total_entry.grid(row=3, column=1, padx=7, pady=7)

                    # Button to submit the supply order
                    submit_button = ttk.Button(
                        supply_order_entry_window,
                        text="Submit",
                        command=lambda: self.buy_supplies_to_database(
                            supplier_var.get(), item_id_var.get(), quantity_entry.get(), purchase_total_entry.get(),
                            supply_order_entry_window
                        ),
                    )
                    submit_button.grid(row=4, columnspan=2, padx=5, pady=10)

    def buy_supplies_to_database(self, selected_supplier, item_id_var, quantity, purchase_total, window):
            # Connect
            with connect_to_database() as connection:
                with connection.cursor() as cursor:
                    # Extract supplier ID from the selected option in the dropdown
                    supplier_id = int(selected_supplier.split(":")[0])

                    # Extract item ID from the selected option in the dropdown
                    item_id = int(item_id_var.split(":")[0])

                    # Fetch item details
                    cursor.execute("SELECT item_name FROM items WHERE item_id = %s", (item_id,))
                    item_details = cursor.fetchone()

                    if not item_details:
                        self.show_message("Item not found. Please enter a valid Item ID.")
                        return

                    item_name = item_details[0]

                    # Insert the supply order into the database
                    query = "INSERT INTO supply_orderss (supplier_id, item_id, supply_quantity_ordered, purchase_total) VALUES (%s, %s, %s, %s)"
                    values = (supplier_id, item_id, int(quantity), float(purchase_total))
                    cursor.execute(query, values)

                    # Update the item quantity in the items table
                    cursor.execute("UPDATE items SET item_quantity = item_quantity + %s WHERE item_id = %s", (int(quantity), item_id))

                    
                    # Retrieve the most recent customer_order_id
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    last_inserted_id = cursor.fetchone()[0]
                    
                    # Update purchases table
                    purchases_query = "INSERT INTO purchases (supplier_id, supply_order_id, purchase_total) VALUES (%s, %s, %s)"
                    purchases_values = (supplier_id, last_inserted_id, purchase_total )
                    cursor.execute(purchases_query, purchases_values)

                    # Show a success message
                    self.show_message(f"Supply order for {quantity} units of {item_name} from supplier {selected_supplier} recorded successfully.\nTotal Cost: {purchase_total}")

                    # Close the supply order entry window after insertion
                    window.destroy()



    #################################### SALE #########################################          


    def handle_make_sale(self):
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Fetch the list of customers
                cursor.execute("SELECT customer_id, customer_name FROM customers")
                customers = cursor.fetchall()

                # Display the list of customers in a dropdown
                customer_label = ttk.Label(self.root, text="Select Customer:")
                customer_label.grid(row=0, column=5, padx=7, pady=7)

                customer_var = tk.StringVar()
                customer_dropdown = ttk.Combobox(self.root, textvariable=customer_var, state="readonly")
                customer_dropdown["values"] = [f"{customer[0]}: {customer[1]}" for customer in customers]
                customer_dropdown.grid(row=0, column=6, padx=7, pady=7)

                # Fetch the list of items
                cursor.execute("SELECT item_id, item_name FROM items")
                items = cursor.fetchall()

                # Display the list of items in a dropdown
                item_label = ttk.Label(self.root, text="Select Item:")
                item_label.grid(row=1, column=5, padx=7, pady=7)

                item_var = tk.StringVar()
                item_dropdown = ttk.Combobox(self.root, textvariable=item_var, state="readonly")
                item_dropdown["values"] = [f"{item[0]}: {item[1]}" for item in items]
                item_dropdown.grid(row=1, column=6, padx=7, pady=7)

                # Entry widgets for user input
                quantity_label = ttk.Label(self.root, text="Quantity:")
                quantity_label.grid(row=2, column=5, padx=7, pady=7)
                quantity_entry = ttk.Entry(self.root)
                quantity_entry.grid(row=2, column=6, padx=7, pady=7)

                # Button to submit the sale order
                submit_button = ttk.Button(
                    self.root,
                    text="Submit Sale",
                    command=lambda: self.make_sale_to_database(
                        customer_var.get(), item_var.get(), quantity_entry.get()
                    ),
                )
                submit_button.grid(row=3, column=5, columnspan=2, padx=5, pady=10)

    def make_sale_to_database(self, selected_customer, item_id_var, quantity):
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Extract customer ID from the selected option in the dropdown
                customer_id = int(selected_customer.split(":")[0])

                # Extract item ID from the selected option in the dropdown
                item_id = int(item_id_var.split(":")[0])

                # Fetch item details
                cursor.execute("SELECT item_name, item_price, item_quantity FROM items WHERE item_id = %s", (item_id,))
                item_details = cursor.fetchone()

                if not item_details:
                    self.show_message("Item not found. Please enter a valid Item ID.")
                    return

                item_name, item_price, item_quantity = item_details


                # Check if there is enough stock
                if int(quantity) > item_quantity:
                    self.show_message(f"Purchase failed. Not enough stock for {item_name}.\n:( ")
                    return
                
                if int(quantity) <=0:
                    self.show_message(f"Purchase failed. Invalid Number of Quantity for {item_name}.\n:( ")
                    return

                # Calculate total amount before applying points discount
                total_amount_before_discount = int(quantity) * item_price

                # Fetch customer details
                cursor.execute("SELECT points FROM customers WHERE customer_id = %s", (customer_id,))
                points_available = cursor.fetchone()[0]

                # Check if customer wants to use points for a discount
                use_points = messagebox.askyesno(
                    "Use Points",
                    f"You have {points_available} points. Do you want to use points for a discount?",
                )

                if use_points:
                    # Calculate discount based on available points (10% off per point)
                    discount_percentage = min(10, points_available)  # Maximum discount of 10%
                    discount_amount = (discount_percentage / 100) * total_amount_before_discount

                    # Calculate total amount after applying points discount
                    total_amount_after_discount = total_amount_before_discount - discount_amount

                    # Insert the sale order into the customer_orders table
                    query = "INSERT INTO customer_orders (customer_id, item_id, item_price, item_quantity_ordered, sale_total, points_used) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (customer_id, item_id, item_price, int(quantity), total_amount_after_discount, discount_percentage)
                    cursor.execute(query, values)

                    # Deduct only the points used from the customer's total
                    cursor.execute(
                        "UPDATE customers SET points = points - %s WHERE customer_id = %s",
                        (points_available, customer_id),
                    )
                else:
                    # If points are not used, set total amount after discount to total amount before discount
                    total_amount_after_discount = total_amount_before_discount

                    # Insert the sale order into the customer_orders table without points_used
                    query = "INSERT INTO customer_orders (customer_id, item_id, item_price, item_quantity_ordered, sale_total) VALUES (%s, %s, %s, %s, %s)"
                    values = (customer_id, item_id, item_price, int(quantity), total_amount_after_discount)
                    cursor.execute(query, values)
                

                # Update the item quantity in the items table
                cursor.execute("UPDATE items SET item_quantity = item_quantity - %s WHERE item_id = %s", (int(quantity), item_id))

                # Update points based on the total purchase amount (1 point per 800,000)
                points_earned = total_amount_before_discount // 800000
                cursor.execute("UPDATE customers SET points = points + %s WHERE customer_id = %s", (points_earned, customer_id))

                # Retrieve the most recent customer_order_id
                cursor.execute("SELECT LAST_INSERT_ID()")
                last_inserted_id = cursor.fetchone()[0]
                    
                # Update purchases table
                sales_query = "INSERT INTO sales (customer_id, customer_order_id, sale_total) VALUES (%s, %s, %s)"
                sales_values = (customer_id, last_inserted_id, total_amount_after_discount)
                cursor.execute(sales_query, sales_values)

                # Show a success message
                self.show_message(
                    f"Sale order for {quantity} units of {item_name} to customer {selected_customer} recorded successfully.\n"
                    f"Total Amount Before Discount: {total_amount_before_discount}\n"
                    f"Discount Applied: {discount_amount if use_points else 0}\n"
                    f"Total Amount After Discount: {total_amount_after_discount}\n"
                    f"Points Earned: {points_earned}"
                )


#################################### REMOVAL #########################################
    
    def handle_remove_supplier(self):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Fetch the list of suppliers
                cursor.execute("SELECT supplier_id, `supplier_name` FROM suppliers")
                suppliers = cursor.fetchall()

                # Create a new Toplevel window for the supplier removal form
                supplier_removal_window = tk.Toplevel(self.root)
                supplier_removal_window.title("Remove Supplier")

                # Display the list of suppliers in a dropdown
                supplier_label = ttk.Label(supplier_removal_window, text="Select Supplier:")
                supplier_label.grid(row=0, column=0, padx=7, pady=7)

                supplier_var = tk.StringVar()
                supplier_dropdown = ttk.Combobox(supplier_removal_window, textvariable=supplier_var, state="readonly")
                supplier_dropdown["values"] = [f"{supplier[0]}: {supplier[1]}" for supplier in suppliers]
                supplier_dropdown.grid(row=0, column=1, padx=7, pady=7)

                # Create a button to submit the supplier removal request
                submit_button = ttk.Button(
                    supplier_removal_window,
                    text="Remove Supplier",
                    command=lambda: self.remove_supplier_from_database(supplier_var.get(), supplier_removal_window),
                )
                submit_button.grid(row=1, columnspan=2, padx=5, pady=10)

    def remove_supplier_from_database(self, selected_supplier, window):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Extract supplier ID from the selected option in the dropdown
                supplier_id = int(selected_supplier.split(":")[0])

                query = "DELETE FROM suppliers WHERE supplier_id = %s"
                cursor.execute(query, (supplier_id,))
                self.show_message("Supplier deleted successfully.")
                # Close the supplier removal window after deletion
                window.destroy()

    def handle_remove_employee(self):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Fetch the list of employees
                cursor.execute("SELECT employee_id, employee_name, employee_role FROM employees")
                employees = cursor.fetchall()

                # Create a new Toplevel window for the employee removal form
                employee_removal_window = tk.Toplevel(self.root)
                employee_removal_window.title("Remove Employee")

                # Display the list of employees in a dropdown
                employee_label = ttk.Label(employee_removal_window, text="Select Employee:")
                employee_label.grid(row=0, column=0, padx=7, pady=7)

                employee_var = tk.StringVar()
                employee_dropdown = ttk.Combobox(employee_removal_window, textvariable=employee_var, state="readonly")
                employee_dropdown["values"] = [f"{employee[0]}: {employee[1]}" for employee in employees]
                employee_dropdown.grid(row=0, column=1, padx=7, pady=7)

                # Create a button to submit the employee removal request
                submit_button = ttk.Button(
                    employee_removal_window,
                    text="Remove Employee",
                    command=lambda: self.remove_employee_from_database(employee_var.get(), employee_removal_window),
                )
                submit_button.grid(row=1, columnspan=2, padx=5, pady=10)

    def remove_employee_from_database(self, selected_employee, window):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # Extract employee_id from the selected option in the dropdown
                employee_id = int(selected_employee.split(":")[0])

                query = "DELETE FROM employees WHERE employee_id = %s"
                cursor.execute(query, (employee_id,))
                self.show_message("Employee deleted successfully.")
                # Close the employee removal window after deletion
                window.destroy()


def main():
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
