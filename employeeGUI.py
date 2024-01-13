import tkinter as tk
from adminGUI import connect_to_database
from tkinter import ttk, messagebox


class EmployeeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Employee Dashboard")
        self.employee_id = None
        self.employee_attendance = None
        self.has_clocked_in = False
        self.create_employee_id_prompt()

        # Call mainloop at the end of __init__
        self.root.mainloop()

    def show_message(self, message):
        messagebox.showinfo("Message", message)

    def create_employee_id_prompt(self):
        employee_id_prompt = tk.Toplevel(self.root)
        employee_id_prompt.title("Enter Employee ID")

        label = ttk.Label(employee_id_prompt, text="Enter Employee ID:")
        label.pack(padx=10, pady=10)

        entry = ttk.Entry(employee_id_prompt)
        entry.pack(padx=10, pady=10)

        submit_button = ttk.Button(
            employee_id_prompt,
            text="Submit",
            command=lambda: self.on_employee_id_submit(entry.get(), employee_id_prompt),
        )
        submit_button.pack(pady=10)

    def on_employee_id_submit(self, employee_id, window):
        # Validate employee_id
        if self.is_valid_employee_id(employee_id):
            self.employee_id = employee_id
            window.destroy()
            self.create_employee_dashboard()
        else:
            self.show_error("Invalid Employee ID. Try again.")

    def is_valid_employee_id(self, employee_id):

        with connect_to_database() as connection:

            with connection.cursor() as cursor:

                # Query to check if the employee_id exists in the employees table
                query = "SELECT COUNT(*) FROM employees WHERE employee_id = %s"
                cursor.execute(query, (employee_id,))
                count = cursor.fetchone()[0]

                # If count is greater than 0, the employee_id is valid (exists in the table)
                return count > 0
        

    def create_employee_dashboard(self):
        # Create UI
        dashboard = ttk.Frame(self.root, padding=10)
        dashboard.grid(row=0, column=0, sticky="nsew")

        view_items_button = ttk.Button(dashboard, text="View Items", command=self.handle_view_items)
        view_items_button.grid(row=0, column=0, padx=5, pady=5)

        clock_in_button = ttk.Button(dashboard, text="Clock In", command=self.handle_clock_in)
        clock_in_button.grid(row=1, column=0, padx=5, pady=5)

        # Fetch employee_role based on employee_id
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                query = "SELECT employee_role FROM employees WHERE employee_id = %s"
                cursor.execute(query, (self.employee_id,))
                employee_role = cursor.fetchone()[0]

        # Show additional buttons if the employee role is sales
        if employee_role == "Sales":
            make_sale_button = ttk.Button(dashboard, text="Make Sale", command=self.handle_make_sale)
            make_sale_button.grid(row=2, column=0, padx=5, pady=5)

        # If role is accountant:    
        elif employee_role == "Accountant":

            view_sales_button = ttk.Button(dashboard, text="View Sales History", command=self.handle_view_sales)
            view_sales_button.grid(row=4, column=0, padx=5, pady=5)

            view_purchases_button = ttk.Button(dashboard, text="View Purchase History", command=self.handle_view_purchases)
            view_purchases_button.grid(row=5, column=0, padx=5, pady=5)


        elif employee_role == "Manager":

            make_sale_button = ttk.Button(dashboard, text="Make Sale", command=self.handle_make_sale)
            make_sale_button.grid(row=2, column=0, padx=5, pady=5)

            view_employees_button = ttk.Button(dashboard, text="View Employees", command=self.handle_view_employees)
            view_employees_button.grid(row=3, column=0, padx=5, pady=5)

            remove_employee_button = ttk.Button(dashboard, text="Fire Employee", command=self.handle_remove_employee)
            remove_employee_button.grid(row=5, column=0, padx=5, pady=5)

            insert_employee_button = ttk.Button(dashboard, text="New Employee", command=self.handle_insert_employee)
            insert_employee_button.grid(row=4, column=0, padx=5, pady=5)

            
            view_top_selling_button = ttk.Button(dashboard, text="View Top 5 Best Selling", command=self.handle_top_selling_items_report)
            view_top_selling_button.grid(row=6, column=0, padx=5, pady=5)

            

        # Creeate frame to show employee info
        employee_info_frame = ttk.Frame(self.root, padding=10)
        employee_info_frame.grid(row=0, column=1, sticky="nsew")

        employee_info_label = ttk.Label(employee_info_frame, text=f" Welcome to Employee Dashboard!")
        employee_info_label.grid(row=0, column=0, padx=5, pady=5)

        # Display the info based on the employee_id
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                # For info from employees table
                query = "SELECT * FROM employees WHERE employee_id = %s"
                cursor.execute(query, (self.employee_id,))
                employee = cursor.fetchone()
                employee_id = employee[0]
                employee_name = employee[1]
                employee_position = employee[2]

                # For info from employees_attendance table
                query = "SELECT Present_Sessions FROM employees_attendance WHERE employee_id = %s"
                values = (employee_id,)
                cursor.execute(query, values)
                result = cursor.fetchone()
                present_sessions = result[0]

        # Display placeholder information
        employee_info_text = f"ID: {employee_id}\nName: {employee_name}\nPosition: {employee_position}\nAttendances: {present_sessions}"
        employee_info_display = ttk.Label(employee_info_frame, text=employee_info_text)
        employee_info_display.grid(row=1, column=0, padx=5, pady=5)

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

                # Iterate through customer_orders table and append to text widget
                for index, sale_order in enumerate(sale_orders, start=1):
                    sale_orders_text.insert(tk.END, f"\n{index}. Customer Order ID: {sale_order[0]}\n")
                    sale_orders_text.insert(tk.END, f"   Customer ID: {sale_order[1]}\n")
                    sale_orders_text.insert(tk.END, f"   Item ID: {sale_order[2]}\n")
                    sale_orders_text.insert(tk.END, f"   Item Price: {sale_order[3]}\n")
                    sale_orders_text.insert(tk.END, f"   Quantity Ordered: {sale_order[4]}\n")
                    sale_orders_text.insert(tk.END, f"   Sale Time: {sale_order[5]}\n")
                    sale_orders_text.insert(tk.END, f"   Total Amount: {sale_order[6]}\n")
                    sale_orders_text.insert(tk.END, f"   Points Added: {sale_order[7]}\n")
                    sale_orders_text.insert(tk.END, "\n----------------------------------------------\n")

                # Make the text read-only
                sale_orders_text.config(state=tk.DISABLED)

    def handle_view_supply_orders(self):
        # Connect
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM supply_orders")
                supply_orders = cursor.fetchall()

                # Create a new Toplevel window for displaying supply orders
                supply_orders_window = tk.Toplevel(self.root)
                supply_orders_window.title("Supply Orders List")

                # Create a text widget to display supply orders
                supply_orders_text = tk.Text(supply_orders_window, wrap=tk.WORD)
                supply_orders_text.pack(expand=True, fill=tk.BOTH)

                # Iterate through supply+orders and append to the text widget
                for index, supply_order in enumerate(supply_orders, start=1):
                    supply_orders_text.insert(tk.END, f"\n{index}. Supply Order ID: {supply_order[0]}\n")
                    supply_orders_text.insert(tk.END, f"   Supplier ID: {supply_order[1]}\n")
                    supply_orders_text.insert(tk.END, f"   Item ID: {supply_order[2]}\n")
                    supply_orders_text.insert(tk.END, f"   Purchase Time: {supply_order[3]}\n")
                    supply_orders_text.insert(tk.END, f"   Quantity Ordered: {supply_order[4]}\n")
                    supply_orders_text.insert(tk.END, f"   Purchase Total: {supply_order[5]}\n")
                    supply_orders_text.insert(tk.END, "\n----------------------------------------------\n")

                # Make the text read-only
                supply_orders_text.config(state=tk.DISABLED)


    def handle_view_items(self):
        # Connect
            with connect_to_database() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT item_name, item_weight, item_price, item_quantity FROM items")
                        items = cursor.fetchall()

                        # Toplevel window for displaying items
                        items_window = tk.Toplevel(self.root)
                        items_window.title("Items List")

                        # Create a text widget to display items
                        items_text = tk.Text(items_window, wrap=tk.WORD)
                        items_text.pack(expand=True, fill=tk.BOTH)

                        # Iterate through items table and append to the text widget 
                        for index, item in enumerate(items, start=1):
                            items_text.insert(tk.END, f"{index}. Name: {item[0]}\n")
                            items_text.insert(tk.END, f"   Weight: {item[1]} Grams\n")
                            items_text.insert(tk.END, f"   Price: {item[2]} Rupiah\n")
                            items_text.insert(tk.END, f"   Stock: {item[3]} Units\n")
                            items_text.insert(tk.END, "----------------------------------------------\n")

                        # Make the text read-only
                        items_text.config(state=tk.DISABLED)


    # For employee attendance incrementation
    def handle_clock_in(self):
        if not self.has_clocked_in:  # Check if the employee has not already clocked in
            with connect_to_database() as connection:
                with connection.cursor() as cursor:

                    # Store table info in variable
                    cursor.execute("SELECT * FROM employees_attendance WHERE employee_id = %s", (self.employee_id,))
                    attendance_record = cursor.fetchone()

                    if attendance_record:
                        # If the employee has existing value, increment and update 'Present_Sessions' 
                        cursor.execute("UPDATE employees_attendance SET Present_Sessions = Present_Sessions + 1 WHERE employee_id = %s", (self.employee_id,))
                    else:
                        # If the employee doesn't have existing value, insert a new value of 'Present_Sessions' set to 1
                        cursor.execute("INSERT INTO employees_attendance (employee_id, Present_Sessions) VALUES (%s, 1)", (self.employee_id,))

            # Update the var to indicate that the employee has clocked in
            self.has_clocked_in = True

            # Show a success message 
            self.show_message(f"Attendance recorded successfully for Employee ID: {self.employee_id}")
        else:
            # Show a message indicating that employee has already clocked in
            self.show_message("You have already clocked in for this session.")
    

    def handle_make_sale(self):
        with connect_to_database() as connection:
            with connection.cursor() as cursor:

                # Store id and name from customers table to a var
                cursor.execute("SELECT customer_id, customer_name FROM customers")
                customers = cursor.fetchall()

                # Display the list of customers in a dropdown
                customer_label = ttk.Label(self.root, text="Select Customer:")
                customer_label.grid(row=0, column=5, padx=7, pady=7)

                customer_var = tk.StringVar()
                customer_dropdown = ttk.Combobox(self.root, textvariable=customer_var, state="readonly")
                customer_dropdown["values"] = [f"{customer[0]}: {customer[1]}" for customer in customers]
                customer_dropdown.grid(row=0, column=6, padx=7, pady=7)

                # Store values from items table to a var
                cursor.execute("SELECT item_id, item_name FROM items")
                items = cursor.fetchall()

                # Display the list of items in a dropdown
                item_label = ttk.Label(self.root, text="Select Item:")
                item_label.grid(row=1, column=5, padx=7, pady=7)

                item_var = tk.StringVar()
                item_dropdown = ttk.Combobox(self.root, textvariable=item_var, state="readonly")
                item_dropdown["values"] = [f"{item[0]}: {item[1]}" for item in items] # Be displayed as item id : item name
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

                # Store item details
                cursor.execute("SELECT item_name, item_price, item_quantity FROM items WHERE item_id = %s", (item_id,))
                item_details = cursor.fetchone()

                # Dont need this but eh, just to be safe
                if not item_details:
                    self.show_message("Item not found. Please enter a valid Item ID.")
                    return
                
                # Declare and set vars
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
                    # Calculate discount based on available points 
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

    # Add functions for the 5 report queries
    def handle_top_selling_items_report(self):
        # Connect to the database
            with connect_to_database() as connection:
                with connection.cursor() as cursor:
                    # Query to retrieve top selling items report
                    cursor.execute("SELECT i.item_name, SUM(co.item_quantity_ordered) AS total_quantity_ordered "
                                "FROM items i "
                                "JOIN customer_orders co ON i.item_id = co.item_id "
                                "GROUP BY i.item_name "
                                "ORDER BY total_quantity_ordered DESC "
                                "LIMIT 5")
                    top_selling_items_report = cursor.fetchall()

                    # Display the results in a new Toplevel window
                    report_window = tk.Toplevel(self.root)
                    report_window.title("Top Selling Items Report")

                    # Create a text widget to display the top selling items report
                    report_text = tk.Text(report_window, wrap=tk.WORD)
                    report_text.pack(expand=True, fill=tk.BOTH)

                    # Iterate through the report and append to the text widget
                    for index, entry in enumerate(top_selling_items_report, start=1):
                        report_text.insert(tk.END, f"\n{index}. Item Name: {entry[0]}\n")
                        report_text.insert(tk.END, f"   Total Quantity Ordered: {entry[1]}\n")
                        report_text.insert(tk.END, "\n----------------------------------------------\n")

                    # Make the text read-only
                    report_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    employee_gui = EmployeeGUI()