import tkinter as tk
from adminGUI import connect_to_database
from tkinter import ttk, messagebox



class CustomerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Customer Portal")

        self.customer_id = None

        self.create_customer_id_prompt()

        # Call mainloop at the end of __init__
        self.root.mainloop()

    def show_message(self, message):
        messagebox.showinfo("Message", message)

    def create_customer_id_prompt(self):
        customer_id_prompt = tk.Toplevel(self.root)
        customer_id_prompt.title("Enter Customer ID")

        label = ttk.Label(customer_id_prompt, text="Enter your Customer ID:")
        label.pack(padx=10, pady=10)

        entry = ttk.Entry(customer_id_prompt)
        entry.pack(padx=10, pady=10)

        submit_button = ttk.Button(
            customer_id_prompt,
            text="Submit",
            command=lambda: self.on_customer_id_submit(entry.get(), customer_id_prompt),
        )
        submit_button.pack(pady=10)

    def on_customer_id_submit(self, customer_id, window):

        if self.is_valid_customer_id(customer_id):
            self.customer_id = customer_id
            window.destroy()
            self.create_customer_dashboard()
        else:
            pass


    def is_valid_customer_id(self, customer_id):
        
        with connect_to_database() as connection:

            with connection.cursor() as cursor:

                # Execute a query to check if the customer_id exists in the customers table
                query = "SELECT COUNT(*) FROM customers WHERE customer_id = %s"
                cursor.execute(query, (customer_id,))
                count = cursor.fetchone()[0]

                # If count is greater than 0, the customer_id is valid (exists in the table)
                return count > 0

    def create_customer_dashboard(self):
        dashboard = ttk.Frame(self.root, padding=10)
        dashboard.grid(row=0, column=0, sticky="nsew")

        view_items_button = ttk.Button(dashboard, text="View Items", command=self.handle_view_items)
        view_items_button.grid(row=0, column=0, padx=5, pady=5)

        buy_item_button = ttk.Button(dashboard, text="Buy Item", command=self.handle_make_sale)
        buy_item_button.grid(row=1, column=0, padx=5, pady=5)

        customer_info_frame = ttk.Frame(self.root, padding=10)
        customer_info_frame.grid(row=0, column=1, sticky="nsew")

        update_info_button = ttk.Button(dashboard, text="Update Information", command=self.handle_update_info)
        update_info_button.grid(row=2, column=0, padx=5, pady=5)

        view_history_button = ttk.Button(dashboard, text="View Purchase History", command=self.handle_view_purchase_history)
        view_history_button.grid(row=3, column=0, padx=5, pady=5)

        # Display customer information based on the customer_id
        customer_info_label = ttk.Label(customer_info_frame, text=f" Welcome to Customer Portal!")
        customer_info_label.grid(row=0, column=0, padx=5, pady=5)
        
        # Fetch and display customer information from the database 
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                query = "SELECT * FROM customers WHERE customer_id = %s"
                cursor.execute(query, (self.customer_id,))
                customer = cursor.fetchone()
                customer_name = customer[1]
                customer_email = customer[2]
                customer_pn = customer[3]
                customer_address = customer[4]
                customer_points = customer[5]
        # For now, just display placeholder information
        customer_info_text = f"Name: {customer_name}\nEmail: {customer_email}\nPhone: {customer_pn}\nAddress: {customer_address}\nPoints: {customer_points}"
        customer_info_display = ttk.Label(customer_info_frame, text=customer_info_text)
        customer_info_display.grid(row=1, column=0, padx=5, pady=5)

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

    def handle_make_sale(self):
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
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
                    text="Make Purchase",
                    command=lambda: self.make_sale_to_database(item_var.get(), quantity_entry.get()),
                )
                submit_button.grid(row=3, column=5, columnspan=2, padx=5, pady=10)

    def make_sale_to_database(self, item_id_var, quantity):

        with connect_to_database() as connection:
            with connection.cursor() as cursor:
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
                customer_id = self.customer_id
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

                # Update sales table
                sales_query = "INSERT INTO sales (customer_id, customer_order_id, sale_total) VALUES (%s, %s, %s)"
                sales_values = (customer_id, last_inserted_id, total_amount_after_discount)
                cursor.execute(sales_query, sales_values)


                # Show a success message
                self.show_message(
                    f"Sale order for {quantity} units of {item_name} to customer {self.customer_id} recorded successfully.\n"
                    f"Total Amount Before Discount: {total_amount_before_discount}\n"
                    f"Discount Applied: {discount_amount if use_points else 0}\n"
                    f"Total Amount After Discount: {total_amount_after_discount}\n"
                    f"Points Earned: {points_earned}"
                )

    def handle_update_info(self):
        # Create a new Toplevel window for updating information
        update_info_window = tk.Toplevel(self.root)
        update_info_window.title("Update Information")

        # Create Entry widgets for user input
        new_name_label = ttk.Label(update_info_window, text="New Name:")
        new_name_label.grid(row=0, column=0, padx=5, pady=5)
        new_name_entry = ttk.Entry(update_info_window)
        new_name_entry.grid(row=0, column=1, padx=5, pady=5)

        new_email_label = ttk.Label(update_info_window, text="New Email:")
        new_email_label.grid(row=1, column=0, padx=5, pady=5)
        new_email_entry = ttk.Entry(update_info_window)
        new_email_entry.grid(row=1, column=1, padx=5, pady=5)

        new_phone_label = ttk.Label(update_info_window, text="New Phone:")
        new_phone_label.grid(row=2, column=0, padx=5, pady=5)
        new_phone_entry = ttk.Entry(update_info_window)
        new_phone_entry.grid(row=2, column=1, padx=5, pady=5)

        new_address_label = ttk.Label(update_info_window, text="New Address:")
        new_address_label.grid(row=3, column=0, padx=5, pady=5)
        new_address_entry = ttk.Entry(update_info_window)
        new_address_entry.grid(row=3, column=1, padx=5, pady=5)

        # Button to submit the updated information
        submit_button = ttk.Button(
            update_info_window,
            text="Submit Update",
            command=lambda: self.update_info_to_database(
                new_name_entry.get(),new_email_entry.get(), new_phone_entry.get(), new_address_entry.get()
            ),
        )
        submit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        

    def update_info_to_database(self, new_name, new_email, new_phone, new_address):
        # Update customer information in the database
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                query = "UPDATE customers SET customer_name = %s,customer_email = %s, customer_phone_number = %s, customer_address = %s WHERE customer_id = %s"
                values = (new_name, new_email, new_phone, new_address, self.customer_id)
                cursor.execute(query, values)

        # Show a success message
        self.show_message("Information updated successfully.")

    def handle_view_purchase_history(self):
        # Connect to the database
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT co.*, i.item_name, s.sale_total
                    FROM customer_orders co
                    JOIN items i ON co.item_id = i.item_id
                    LEFT JOIN sales s ON co.customer_order_id = s.customer_order_id
                    WHERE co.customer_id = %s
                    """, (self.customer_id,))
                purchase_history = cursor.fetchall()

                

                # Create a new Toplevel window for displaying purchase history
                history_window = tk.Toplevel(self.root)
                history_window.title("Purchase History")

                # Create a text widget to display purchase history
                history_text = tk.Text(history_window, wrap=tk.WORD)
                history_text.pack(expand=True, fill=tk.BOTH)

                # Iterate through purchase history and append to the text widget
                for index, order in enumerate(purchase_history, start=1):
                    history_text.insert(tk.END, f"\n{index}. Customer ID: {order[1]}\n")
                    history_text.insert(tk.END, f"   Item Name: {order[8]}\n")
                    history_text.insert(tk.END, f"   Item Price: {order[3]}\n")
                    history_text.insert(tk.END, f"   Quantity Ordered: {order[4]}\n")
                    history_text.insert(tk.END, f"   Purchase Time: {order[5]}\n")
                    history_text.insert(tk.END, f"   Total Price: {order[6]}\n")
                    history_text.insert(tk.END, f"   Points Used: {order[7]}\n")
                    history_text.insert(tk.END, f"   Total Price After Discount: {order[9]}\n")
                    history_text.insert(tk.END, "\n----------------------------------------------\n")

                # Make the text widget read-only
                history_text.config(state=tk.DISABLED)
        
    


if __name__ == "__main__":
    customer_gui = CustomerGUI()