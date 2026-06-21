import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime, timedelta
import hashlib

from pip._internal.vcs import git
from tkcalendar import DateEntry
import csv
from PIL import Image, ImageTk
import io


class SalesManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Management System - Professional Edition")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure colors
        self.bg_color = '#f0f0f0'
        self.primary_color = '#1f77b4'
        self.secondary_color = '#ff7f0e'
        self.success_color = '#2ca02c'
        self.danger_color = '#d62728'

        self.root.configure(bg=self.bg_color)

        self.current_user = None
        self.init_database()
        self.show_login_window()

    def init_database(self):
        """Initialize an SQLite database with all required tables"""
        self.conn = sqlite3.connect('sales_system.db')
        self.cursor = self.conn.cursor()

        # Users' table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS users
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                username
                                TEXT
                                UNIQUE
                                NOT
                                NULL,
                                password
                                TEXT
                                NOT
                                NULL,
                                email
                                TEXT,
                                phone
                                TEXT,
                                company
                                TEXT,
                                created_at
                                TIMESTAMP
                                DEFAULT
                                CURRENT_TIMESTAMP
                            )
                            ''')

        # Product table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS products
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                user_id
                                INTEGER
                                NOT
                                NULL,
                                product_code
                                TEXT
                                NOT
                                NULL,
                                product_name
                                TEXT
                                NOT
                                NULL,
                                description
                                TEXT,
                                unit_price
                                REAL
                                NOT
                                NULL,
                                stock_quantity
                                INTEGER
                                DEFAULT
                                0,
                                category
                                TEXT,
                                created_at
                                TIMESTAMP
                                DEFAULT
                                CURRENT_TIMESTAMP,
                                FOREIGN
                                KEY
                            (
                                user_id
                            ) REFERENCES users
                            (
                                id
                            )
                                )
                            ''')

        # Customers' table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS customers
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                user_id
                                INTEGER
                                NOT
                                NULL,
                                customer_name
                                TEXT
                                NOT
                                NULL,
                                email
                                TEXT,
                                phone
                                TEXT,
                                address
                                TEXT,
                                city
                                TEXT,
                                state
                                TEXT,
                                zip_code
                                TEXT,
                                company_name
                                TEXT,
                                created_at
                                TIMESTAMP
                                DEFAULT
                                CURRENT_TIMESTAMP,
                                FOREIGN
                                KEY
                            (
                                user_id
                            ) REFERENCES users
                            (
                                id
                            )
                                )
                            ''')

        # Sales table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS sales
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                user_id
                                INTEGER
                                NOT
                                NULL,
                                product_id
                                INTEGER,
                                customer_id
                                INTEGER,
                                product_name
                                TEXT
                                NOT
                                NULL,
                                customer_name
                                TEXT
                                NOT
                                NULL,
                                quantity
                                INTEGER
                                NOT
                                NULL,
                                unit_price
                                REAL
                                NOT
                                NULL,
                                discount
                                REAL
                                DEFAULT
                                0,
                                tax
                                REAL
                                DEFAULT
                                0,
                                total_amount
                                REAL
                                NOT
                                NULL,
                                payment_status
                                TEXT
                                DEFAULT
                                'Pending',
                                notes
                                TEXT,
                                sale_date
                                TIMESTAMP
                                DEFAULT
                                CURRENT_TIMESTAMP,
                                FOREIGN
                                KEY
                            (
                                user_id
                            ) REFERENCES users
                            (
                                id
                            ),
                                FOREIGN KEY
                            (
                                product_id
                            ) REFERENCES products
                            (
                                id
                            ),
                                FOREIGN KEY
                            (
                                customer_id
                            ) REFERENCES customers
                            (
                                id
                            )
                                )
                            ''')

        # Invoice table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS invoices
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                sale_id
                                INTEGER
                                NOT
                                NULL,
                                invoice_number
                                TEXT
                                UNIQUE,
                                invoice_date
                                TIMESTAMP
                                DEFAULT
                                CURRENT_TIMESTAMP,
                                due_date
                                TIMESTAMP,
                                status
                                TEXT
                                DEFAULT
                                'Unpaid',
                                FOREIGN
                                KEY
                            (
                                sale_id
                            ) REFERENCES sales
                            (
                                id
                            )
                                )
                            ''')

        self.conn.commit()

    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def show_login_window(self):
        """Display professional login window"""
        self.clear_window()

        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left side - Info panel
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        left_panel.configure(height=700)
        left_inner = ttk.Frame(left_panel)
        left_inner.pack(fill=tk.BOTH, expand=True, padx=40, pady=100)

        title = ttk.Label(left_inner, text="Sales Management", font=("Segoe UI", 32, "bold"))
        title.pack(pady=20)

        subtitle = ttk.Label(left_inner, text="Group 2", font=("Segoe UI", 14))
        subtitle.pack(pady=10)

        info_text = ttk.Label(left_inner, text=
        "Manage your sales efficiently with our\n"
        "comprehensive management system.\n\n"
        "• Track Sales & Invoices\n"
        "• Manage Customers & Products\n"
        "• Generate Reports\n"
        "• Secure Authentication",
                              font=("Segoe UI", 10), justify=tk.LEFT)
        info_text.pack(pady=40)

        # Right side - Login form
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        form_frame = ttk.Frame(right_panel)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=100)

        form_title = ttk.Label(form_frame, text="User Login", font=("Segoe UI", 18, "bold"))
        form_title.pack(pady=20)

        # Username field
        ttk.Label(form_frame, text="Username", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(10, 5))
        self.username_entry = ttk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.username_entry.pack(pady=(0, 15), ipady=8)
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())

        # Password field
        ttk.Label(form_frame, text="Password", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(10, 5))
        self.password_entry = ttk.Entry(form_frame, font=("Segoe UI", 10), width=30, show="●")
        self.password_entry.pack(pady=(0, 20), ipady=8)
        self.password_entry.bind('<Return>', lambda e: self.login_user())

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)

        login_btn = ttk.Button(button_frame, text="Login", command=self.login_user)
        login_btn.pack(side=tk.LEFT, padx=5)

        register_btn = ttk.Button(button_frame, text="Register", command=self.show_register_window)
        register_btn.pack(side=tk.LEFT, padx=5)

    def show_register_window(self):
        """Display registration window"""
        self.clear_window()

        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        form_frame = ttk.Frame(main_container)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)

        # Title with back button
        title_frame = ttk.Frame(form_frame)
        title_frame.pack(fill=tk.X, pady=10)

        back_btn = ttk.Button(title_frame, text="← Back to Login", command=self.show_login_window, width=20)
        back_btn.pack(side=tk.LEFT)

        form_title = ttk.Label(form_frame, text="Create New Account", font=("Segoe UI", 18, "bold"))
        form_title.pack(pady=20)

        # Create scrollable frame
        canvas = tk.Canvas(form_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Form fields
        fields = {}
        field_names = [
            ("Username", "username"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Company Name", "company"),
            ("Password", "password"),
            ("Confirm Password", "confirm_password")
        ]

        for label_text, field_name in field_names:
            ttk.Label(scrollable_frame, text=label_text, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(10, 5))
            entry = ttk.Entry(scrollable_frame, font=("Segoe UI", 10), width=40)
            entry.pack(pady=(0, 15), ipady=6)
            if label_text.endswith("Password"):
                entry.config(show="●")
            fields[field_name] = entry

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def register():
            username = fields["username"].get().strip()
            email = fields["email"].get().strip()
            phone = fields["phone"].get().strip()
            company = fields["company"].get().strip()
            password = fields["password"].get()
            confirm = fields["confirm_password"].get()

            # Validation
            if not all([username, email, password, confirm]):
                messagebox.showerror("Error", "Username, Email, and Password are required!")
                return

            if len(username) < 3:
                messagebox.showerror("Error", "Username must be at least 3 characters!")
                return

            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match!")
                return

            if len(password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters!")
                return

            if "@" not in email:
                messagebox.showerror("Error", "Please enter a valid email address!")
                return

            try:
                hashed_pwd = self.hash_password(password)
                self.cursor.execute(
                    'INSERT INTO users (username, email, phone, company, password) VALUES (?, ?, ?, ?, ?)',
                    (username, email, phone, company, hashed_pwd)
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Account created successfully! Please login.")
                self.show_login_window()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")

        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)

        register_btn = ttk.Button(button_frame, text="Create Account", command=register)
        register_btn.pack(side=tk.LEFT, padx=5)

    def login_user(self):
        """Authenticate user login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return

        hashed_pwd = self.hash_password(password)
        self.cursor.execute('SELECT id, username, email, company FROM users WHERE username = ? AND password = ?',
                            (username, hashed_pwd))
        user = self.cursor.fetchone()

        if user:
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'company': user[3]
            }
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def show_dashboard(self):
        """Display the main dashboard with a menu"""
        self.clear_window()

        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Sales to CSV", command=self.export_sales_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.logout_user)
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Sales menu
        sales_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sales", menu=sales_menu)
        sales_menu.add_command(label="New Sale", command=lambda: self.show_page("add_sale"))
        sales_menu.add_command(label="View Sales", command=lambda: self.show_page("view_sales"))
        sales_menu.add_command(label="Sales Reports", command=lambda: self.show_page("reports"))

        # Customers menu
        customer_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Customers", menu=customer_menu)
        customer_menu.add_command(label="Add Customer", command=lambda: self.show_page("add_customer"))
        customer_menu.add_command(label="View Customers", command=lambda: self.show_page("view_customers"))

        # Products menu
        product_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Products", menu=product_menu)
        product_menu.add_command(label="Add Product", command=lambda: self.show_page("add_product"))
        product_menu.add_command(label="View Products", command=lambda: self.show_page("view_products"))

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top header with user info
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=10)

        user_info = ttk.Label(header_frame,
                              text=f"User: {self.current_user['username']} | Company: {self.current_user['company'] or 'N/A'} | Email: {self.current_user['email']}",
                              font=("Segoe UI", 10))
        user_info.pack(side=tk.LEFT)

        logout_btn = ttk.Button(header_frame, text="Logout", command=self.logout_user, width=15)
        logout_btn.pack(side=tk.RIGHT)

        # Main content area
        self.main_content = ttk.Frame(main_frame)
        self.main_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Show dashboard home
        self.show_page("dashboard")

    def show_page(self, page_name):
        """Navigate to different pages"""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        if page_name == "dashboard":
            self.show_dashboard_home()
        elif page_name == "add_sale":
            self.show_add_sale_form()
        elif page_name == "view_sales":
            self.show_sales_list()
        elif page_name == "add_customer":
            self.show_add_customer_form()
        elif page_name == "view_customers":
            self.show_customers_list()
        elif page_name == "add_product":
            self.show_add_product_form()
        elif page_name == "view_products":
            self.show_products_list()
        elif page_name == "reports":
            self.show_reports_page()

    def show_dashboard_home(self):
        """Display dashboard home with statistics"""
        # Title
        title = ttk.Label(self.main_content, text="Dashboard", font=("Segoe UI", 20, "bold"))
        title.pack(pady=10)

        # Statistics frame
        stats_frame = ttk.LabelFrame(self.main_content, text="Quick Statistics", padding=15)
        stats_frame.pack(fill=tk.X, pady=10)

        # Get statistics
        self.cursor.execute('SELECT COUNT(*) FROM sales WHERE user_id = ?', (self.current_user['id'],))
        total_sales = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT SUM(total_amount) FROM sales WHERE user_id = ?', (self.current_user['id'],))
        total_revenue = self.cursor.fetchone()[0] or 0

        self.cursor.execute('SELECT COUNT(*) FROM customers WHERE user_id = ?', (self.current_user['id'],))
        total_customers = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT COUNT(*) FROM products WHERE user_id = ?', (self.current_user['id'],))
        total_products = self.cursor.fetchone()[0]

        # Create stat cards
        stats_data = [
            ("Total Sales", str(total_sales), "#1f77b4"),
            ("Total Revenue", f"LE{total_revenue:.2f}", "#2ca02c"),
            ("Total Customers", str(total_customers), "#ff7f0e"),
            ("Total Products", str(total_products), "#d62728")
        ]

        for stat_name, stat_value, color in stats_data:
            stat_card = ttk.Frame(stats_frame, relief=tk.RAISED, borderwidth=2)
            stat_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

            name_label = ttk.Label(stat_card, text=stat_name, font=("Segoe UI", 10))
            name_label.pack(pady=(10, 5))

            value_label = ttk.Label(stat_card, text=stat_value, font=("Segoe UI", 16, "bold"))
            value_label.pack(pady=(5, 10))

        # Quick actions
        actions_frame = ttk.LabelFrame(self.main_content, text="Quick Actions", padding=15)
        actions_frame.pack(fill=tk.X, pady=10)

        actions = [
            ("New Sale", lambda: self.show_page("add_sale")),
            ("Add Customer", lambda: self.show_page("add_customer")),
            ("Add Product", lambda: self.show_page("add_product")),
            ("View Reports", lambda: self.show_page("reports"))
        ]

        for action_name, action_cmd in actions:
            btn = ttk.Button(actions_frame, text=action_name, command=action_cmd, width=20)
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Recent sales
        recent_frame = ttk.LabelFrame(self.main_content, text="Recent Sales", padding=10)
        recent_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ('Sale ID', 'Product', 'Customer', 'Amount', 'Date')
        tree = ttk.Treeview(recent_frame, columns=columns, height=8, show='headings')

        for col in columns:
            tree.column(col, width=150, anchor=tk.CENTER)
            tree.heading(col, text=col)

        self.cursor.execute('''
                            SELECT id, product_name, customer_name, total_amount, sale_date
                            FROM sales
                            WHERE user_id = ?
                            ORDER BY sale_date DESC LIMIT 10
                            ''', (self.current_user['id'],))

        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=(row[0], row[1], row[2], f"LE{row[3]:.2f}", row[4][:10]))

        tree.pack(fill=tk.BOTH, expand=True)

    def show_add_sale_form(self):
        """Display form to add a new sale"""
        title = ttk.Label(self.main_content, text="Add New Sale", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        # Create form frame
        form_frame = ttk.LabelFrame(self.main_content, text="Sale Details", padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create scrollable canvas
        canvas = tk.Canvas(form_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Form fields
        fields = {}

        # Row 1: Product selection
        ttk.Label(scrollable_frame, text="Product", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W,
                                                                                        pady=(10, 5))

        self.cursor.execute('SELECT id, product_name FROM products WHERE user_id = ?', (self.current_user['id'],))
        products = self.cursor.fetchall()
        product_options = [f"{p[1]} (ID: {p[0]})" for p in products]

        product_var = tk.StringVar()
        product_combo = ttk.Combobox(scrollable_frame, textvariable=product_var, values=product_options, width=40)
        product_combo.grid(row=0, column=1, padx=10, pady=(10, 5), ipady=6)
        fields['product'] = product_combo

        # Row 1: Customer selection
        ttk.Label(scrollable_frame, text="Customer", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky=tk.W,
                                                                                         pady=(10, 5))

        self.cursor.execute('SELECT id, customer_name FROM customers WHERE user_id = ?', (self.current_user['id'],))
        customers = self.cursor.fetchall()
        customer_options = [f"{c[1]} (ID: {c[0]})" for c in customers]

        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(scrollable_frame, textvariable=customer_var, values=customer_options, width=40)
        customer_combo.grid(row=0, column=3, padx=10, pady=(10, 5), ipady=6)
        fields['customer'] = customer_combo

        # Row 2: Quantity
        ttk.Label(scrollable_frame, text="Quantity", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky=tk.W,
                                                                                         pady=(10, 5))
        quantity_entry = ttk.Entry(scrollable_frame, width=25)
        quantity_entry.grid(row=1, column=1, padx=10, pady=(10, 5), ipady=6)
        fields['quantity'] = quantity_entry

        # Row 2: Unit Price
        ttk.Label(scrollable_frame, text="Unit Price (LE)", font=("Segoe UI", 10, "bold")).grid(row=1, column=2,
                                                                                                sticky=tk.W,
                                                                                                pady=(10, 5))
        price_entry = ttk.Entry(scrollable_frame, width=25)
        price_entry.grid(row=1, column=3, padx=10, pady=(10, 5), ipady=6)
        fields['price'] = price_entry

        # Row 3: Discount
        ttk.Label(scrollable_frame, text="Discount (LE)", font=("Segoe UI", 10, "bold")).grid(row=2, column=0,
                                                                                              sticky=tk.W, pady=(10, 5))
        discount_entry = ttk.Entry(scrollable_frame, width=25)
        discount_entry.insert(0, "0")
        discount_entry.grid(row=2, column=1, padx=10, pady=(10, 5), ipady=6)
        fields['discount'] = discount_entry

        # Row 3: Tax
        ttk.Label(scrollable_frame, text="Tax (LE)", font=("Segoe UI", 10, "bold")).grid(row=2, column=2, sticky=tk.W,
                                                                                         pady=(10, 5))
        tax_entry = ttk.Entry(scrollable_frame, width=25)
        tax_entry.insert(0, "0")
        tax_entry.grid(row=2, column=3, padx=10, pady=(10, 5), ipady=6)
        fields['tax'] = tax_entry

        # Row 4: Payment Status
        ttk.Label(scrollable_frame, text="Payment Status", font=("Segoe UI", 10, "bold")).grid(row=3, column=0,
                                                                                               sticky=tk.W,
                                                                                               pady=(10, 5))
        status_var = tk.StringVar(value="Pending")
        status_combo = ttk.Combobox(scrollable_frame, textvariable=status_var, values=["Pending", "Paid", "Partial"],
                                    width=23)
        status_combo.grid(row=3, column=1, padx=10, pady=(10, 5), ipady=6)
        fields['status'] = status_combo

        # Row 4: Sale Date
        ttk.Label(scrollable_frame, text="Sale Date", font=("Segoe UI", 10, "bold")).grid(row=3, column=2, sticky=tk.W,
                                                                                          pady=(10, 5))
        date_entry = DateEntry(scrollable_frame, width=23)
        date_entry.grid(row=3, column=3, padx=10, pady=(10, 5), ipady=6)
        fields['date'] = date_entry

        # Row 5: Notes
        ttk.Label(scrollable_frame, text="Notes", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky=tk.NW,
                                                                                      pady=(10, 5))
        notes_text = tk.Text(scrollable_frame, height=4, width=85)
        notes_text.grid(row=4, column=1, columnspan=3, padx=10, pady=(10, 5), ipady=6)
        fields['notes'] = notes_text

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Button frame
        button_frame = ttk.Frame(self.main_content)
        button_frame.pack(fill=tk.X, pady=10)

        def save_sale():
            try:
                product_str = fields['product'].get()
                customer_str = fields['customer'].get()

                if not all([product_str, customer_str, fields['quantity'].get(), fields['price'].get()]):
                    messagebox.showerror("Error", "Please fill all required fields!")
                    return

                # Extract names from combo selections
                product_name = product_str.split(" (ID:")[0]
                customer_name = customer_str.split(" (ID:")[0]

                quantity = int(fields['quantity'].get())
                unit_price = float(fields['price'].get())
                discount = float(fields['discount'].get())
                tax = float(fields['tax'].get())
                total = (quantity * unit_price) - discount + tax

                payment_status = fields['status'].get()
                sale_date = fields['date'].get()
                notes = fields['notes'].get("1.0", tk.END).strip()

                self.cursor.execute('''
                                    INSERT INTO sales (user_id, product_name, customer_name, quantity, unit_price,
                                                       discount, tax, total_amount, payment_status, notes, sale_date)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    ''', (self.current_user['id'], product_name, customer_name, quantity, unit_price,
                                          discount, tax, total, payment_status, notes, sale_date))

                self.conn.commit()
                messagebox.showinfo("Success", "Sale record saved successfully!")
                self.show_page("view_sales")
            except ValueError as e:
                messagebox.showerror("Error", "Please enter valid numbers for quantity, price, discount, and tax!")

        save_btn = ttk.Button(button_frame, text="Save Sale", command=save_sale, width=20)
        save_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = ttk.Button(button_frame, text="Reset Form", command=lambda: self.show_page("add_sale"), width=20)
        reset_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=lambda: self.show_page("dashboard"), width=20)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def show_sales_list(self):
        """Display all sales records with filtering and search"""
        title = ttk.Label(self.main_content, text="Sales Records", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        # Filter frame
        filter_frame = ttk.LabelFrame(self.main_content, text="Filters", padding=10)
        filter_frame.pack(fill=tk.X, pady=10)

        # Search
        ttk.Label(filter_frame, text="Search by Customer/Product:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Payment Status filter
        ttk.Label(filter_frame, text="Payment Status:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(filter_frame, textvariable=status_var, values=["All", "Pending", "Paid", "Partial"],
                                    width=15)
        status_combo.pack(side=tk.LEFT, padx=5)

        # Date range
        ttk.Label(filter_frame, text="From Date:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        from_date = DateEntry(filter_frame, width=15)
        from_date.pack(side=tk.LEFT, padx=5)

        ttk.Label(filter_frame, text="To Date:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        to_date = DateEntry(filter_frame, width=15)
        to_date.pack(side=tk.LEFT, padx=5)

        # Table frame
        table_frame = ttk.LabelFrame(self.main_content, text="Sales Table", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ('Sale ID', 'Product', 'Customer', 'Quantity', 'Unit Price', 'Discount', 'Tax', 'Total', 'Status',
                   'Date')
        tree = ttk.Treeview(table_frame, columns=columns, height=15, show='headings')

        col_widths = [60, 100, 100, 70, 80, 70, 60, 80, 80, 100]
        for col, width in zip(columns, col_widths):
            tree.column(col, width=width, anchor=tk.CENTER)
            tree.heading(col, text=col)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        def load_data():
            for item in tree.get_children():
                tree.delete(item)

            query = 'SELECT * FROM sales WHERE user_id = ?'
            params = [self.current_user['id']]

            search_term = search_var.get()
            if search_term:
                query += ' AND (product_name LIKE ? OR customer_name LIKE ?)'
                params.extend([f'%{search_term}%', f'%{search_term}%'])

            if status_var.get() != 'All':
                query += ' AND payment_status = ?'
                params.append(status_var.get())

            from_str = from_date.get_date().isoformat()
            to_str = to_date.get_date().isoformat()
            query += ' AND DATE(sale_date) BETWEEN ? AND ?'
            params.extend([from_str, to_str])

            query += ' ORDER BY sale_date DESC'

            self.cursor.execute(query, params)
            for row in self.cursor.fetchall():
                tree.insert('', 'end', values=(row[0], row[2], row[3], row[4], f"${row[5]:.2f}",
                                               f"${row[6]:.2f}", f"${row[7]:.2f}", f"${row[8]:.2f}",
                                               row[9], row[12][:10]))

        load_btn = ttk.Button(filter_frame, text="Apply Filters", command=load_data)
        load_btn.pack(side=tk.RIGHT, padx=5)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        load_data()

    def show_add_customer_form(self):
        """Display form to add a new customer"""
        title = ttk.Label(self.main_content, text="Add New Customer", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        form_frame = ttk.LabelFrame(self.main_content, text="Customer Information", padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        fields = {}

        # Row 1: Name and Email
        ttk.Label(form_frame, text="Customer Name *", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W,
                                                                                          pady=10)
        name_entry = ttk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10, ipady=6)
        fields['name'] = name_entry

        ttk.Label(form_frame, text="Email", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky=tk.W, pady=10)
        email_entry = ttk.Entry(form_frame, width=30)
        email_entry.grid(row=0, column=3, padx=10, pady=10, ipady=6)
        fields['email'] = email_entry

        # Row 2: Phone and Company
        ttk.Label(form_frame, text="Phone", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=10)
        phone_entry = ttk.Entry(form_frame, width=30)
        phone_entry.grid(row=1, column=1, padx=10, pady=10, ipady=6)
        fields['phone'] = phone_entry

        ttk.Label(form_frame, text="Company Name", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, sticky=tk.W,
                                                                                       pady=10)
        company_entry = ttk.Entry(form_frame, width=30)
        company_entry.grid(row=1, column=3, padx=10, pady=10, ipady=6)
        fields['company'] = company_entry

        # Row 3: Address
        ttk.Label(form_frame, text="Address", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=10)
        address_entry = ttk.Entry(form_frame, width=30)
        address_entry.grid(row=2, column=1, padx=10, pady=10, ipady=6)
        fields['address'] = address_entry

        # Row 4: City, State, ZIP
        ttk.Label(form_frame, text="City", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=10)
        city_entry = ttk.Entry(form_frame, width=30)
        city_entry.grid(row=3, column=1, padx=10, pady=10, ipady=6)
        fields['city'] = city_entry

        ttk.Label(form_frame, text="State", font=("Segoe UI", 10, "bold")).grid(row=3, column=2, sticky=tk.W, pady=10)
        state_entry = ttk.Entry(form_frame, width=30)
        state_entry.grid(row=3, column=3, padx=10, pady=10, ipady=6)
        fields['state'] = state_entry

        ttk.Label(form_frame, text="ZIP Code", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky=tk.W,
                                                                                   pady=10)
        zip_entry = ttk.Entry(form_frame, width=30)
        zip_entry.grid(row=4, column=1, padx=10, pady=10, ipady=6)
        fields['zip'] = zip_entry

        # Button frame
        button_frame = ttk.Frame(self.main_content)
        button_frame.pack(fill=tk.X, pady=10)

        def save_customer():
            name = fields['name'].get().strip()
            if not name:
                messagebox.showerror("Error", "Customer name is required!")
                return

            try:
                self.cursor.execute('''
                                    INSERT INTO customers (user_id, customer_name, email, phone, company_name, address,
                                                           city, state, zip_code)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    ''', (self.current_user['id'], name, fields['email'].get(), fields['phone'].get(),
                                          fields['company'].get(), fields['address'].get(), fields['city'].get(),
                                          fields['state'].get(), fields['zip'].get()))

                self.conn.commit()
                messagebox.showinfo("Success", "Customer added successfully!")
                self.show_page("view_customers")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save customer: {str(e)}")

        save_btn = ttk.Button(button_frame, text="Save Customer", command=save_customer, width=20)
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=lambda: self.show_page("dashboard"), width=20)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def show_customers_list(self):
        """Display all customers"""
        title = ttk.Label(self.main_content, text="Customers", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        # Search frame
        search_frame = ttk.LabelFrame(self.main_content, text="Search", padding=10)
        search_frame.pack(fill=tk.X, pady=10)

        search_var = tk.StringVar()
        ttk.Label(search_frame, text="Search by name or email:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Table frame
        table_frame = ttk.LabelFrame(self.main_content, text="Customers Table", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ('ID', 'Name', 'Email', 'Phone', 'Company', 'City', 'State')
        tree = ttk.Treeview(table_frame, columns=columns, height=15, show='headings')

        for col in columns:
            tree.column(col, width=120, anchor=tk.W)
            tree.heading(col, text=col)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        def load_data():
            for item in tree.get_children():
                tree.delete(item)

            search_term = search_var.get()
            if search_term:
                query = 'SELECT * FROM customers WHERE user_id = ? AND (customer_name LIKE ? OR email LIKE ?)'
                params = [self.current_user['id'], f'%{search_term}%', f'%{search_term}%']
            else:
                query = 'SELECT * FROM customers WHERE user_id = ?'
                params = [self.current_user['id']]

            self.cursor.execute(query, params)
            for row in self.cursor.fetchall():
                tree.insert('', 'end', values=(row[0], row[2], row[3], row[4], row[8], row[6], row[7]))

        search_btn = ttk.Button(search_frame, text="Search", command=load_data)
        search_btn.pack(side=tk.LEFT, padx=5)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        load_data()

    def show_add_product_form(self):
        """Display form to add a new product"""
        title = ttk.Label(self.main_content, text="Add New Product", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        form_frame = ttk.LabelFrame(self.main_content, text="Product Information", padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        fields = {}

        # Row 1: Product Code and Name
        ttk.Label(form_frame, text="Product Code *", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W,
                                                                                         pady=10)
        code_entry = ttk.Entry(form_frame, width=30)
        code_entry.grid(row=0, column=1, padx=10, pady=10, ipady=6)
        fields['code'] = code_entry

        ttk.Label(form_frame, text="Product Name *", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky=tk.W,
                                                                                         pady=10)
        name_entry = ttk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=3, padx=10, pady=10, ipady=6)
        fields['name'] = name_entry

        # Row 2: Category and Price
        ttk.Label(form_frame, text="Category", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky=tk.W,
                                                                                   pady=10)
        category_entry = ttk.Entry(form_frame, width=30)
        category_entry.grid(row=1, column=1, padx=10, pady=10, ipady=6)
        fields['category'] = category_entry

        ttk.Label(form_frame, text="Unit Price (LE) *", font=("Segoe UI", 10, "bold")).grid(row=1, column=2,
                                                                                            sticky=tk.W, pady=10)
        price_entry = ttk.Entry(form_frame, width=30)
        price_entry.grid(row=1, column=3, padx=10, pady=10, ipady=6)
        fields['price'] = price_entry

        # Row 3: Stock and Description
        ttk.Label(form_frame, text="Stock Quantity", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky=tk.W,
                                                                                         pady=10)
        stock_entry = ttk.Entry(form_frame, width=30)
        stock_entry.insert(0, "0")
        stock_entry.grid(row=2, column=1, padx=10, pady=10, ipady=6)
        fields['stock'] = stock_entry

        ttk.Label(form_frame, text="Description", font=("Segoe UI", 10, "bold")).grid(row=2, column=2, sticky=tk.NW,
                                                                                      pady=10)
        desc_text = tk.Text(form_frame, height=4, width=30)
        desc_text.grid(row=2, column=3, padx=10, pady=10, ipady=6)
        fields['description'] = desc_text

        # Button frame
        button_frame = ttk.Frame(self.main_content)
        button_frame.pack(fill=tk.X, pady=10)

        def save_product():
            code = fields['code'].get().strip()
            name = fields['name'].get().strip()
            price = fields['price'].get()

            if not all([code, name, price]):
                messagebox.showerror("Error", "Product Code, Name, and Price are required!")
                return

            try:
                unit_price = float(price)
                stock = int(fields['stock'].get())

                self.cursor.execute('''
                                    INSERT INTO products (user_id, product_code, product_name, category, unit_price,
                                                          stock_quantity, description)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)
                                    ''', (self.current_user['id'], code, name, fields['category'].get(),
                                          unit_price, stock, fields['description'].get("1.0", tk.END).strip()))

                self.conn.commit()
                messagebox.showinfo("Success", "Product added successfully!")
                self.show_page("view_products")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price and stock!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Product code already exists!")

        save_btn = ttk.Button(button_frame, text="Save Product", command=save_product, width=20)
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=lambda: self.show_page("dashboard"), width=20)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def show_products_list(self):
        """Display all products"""
        title = ttk.Label(self.main_content, text="Products", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        # Search frame
        search_frame = ttk.LabelFrame(self.main_content, text="Search", padding=10)
        search_frame.pack(fill=tk.X, pady=10)

        search_var = tk.StringVar()
        ttk.Label(search_frame, text="Search by name or code:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Table frame
        table_frame = ttk.LabelFrame(self.main_content, text="Products Table", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ('ID', 'Code', 'Name', 'Category', 'Unit Price', 'Stock', 'Date Added')
        tree = ttk.Treeview(table_frame, columns=columns, height=15, show='headings')

        col_widths = [40, 80, 120, 100, 100, 80, 100]
        for col, width in zip(columns, col_widths):
            tree.column(col, width=width, anchor=tk.W)
            tree.heading(col, text=col)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        def load_data():
            for item in tree.get_children():
                tree.delete(item)

            search_term = search_var.get()
            if search_term:
                query = 'SELECT * FROM products WHERE user_id = ? AND (product_name LIKE ? OR product_code LIKE ?)'
                params = [self.current_user['id'], f'%{search_term}%', f'%{search_term}%']
            else:
                query = 'SELECT * FROM products WHERE user_id = ?'
                params = [self.current_user['id']]

            self.cursor.execute(query, params)
            for row in self.cursor.fetchall():
                tree.insert('', 'end', values=(row[0], row[2], row[3], row[4], f"${row[5]:.2f}", row[6], row[8][:10]))

        search_btn = ttk.Button(search_frame, text="Search", command=load_data)
        search_btn.pack(side=tk.LEFT, padx=5)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        load_data()

    def show_reports_page(self):
        """Display reports and analytics"""
        title = ttk.Label(self.main_content, text="Sales Reports & Analytics", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        # Summary statistics
        stats_frame = ttk.LabelFrame(self.main_content, text="Summary Statistics", padding=15)
        stats_frame.pack(fill=tk.X, pady=10)

        self.cursor.execute('''
                            SELECT COUNT(*)          as total_sales,
                                   SUM(total_amount) as total_revenue,
                                   AVG(total_amount) as avg_sale,
                                   MAX(total_amount) as max_sale
                            FROM sales
                            WHERE user_id = ?
                            ''', (self.current_user['id'],))

        stats = self.cursor.fetchone()
        total_sales = stats[0] or 0
        total_revenue = stats[1] or 0
        avg_sale = stats[2] or 0
        max_sale = stats[3] or 0

        # Display statistics in cards
        stat_data = [
            ("Total Sales", str(total_sales)),
            ("Total Revenue", f"LE{total_revenue:.2f}"),
            ("Average Sale", f"LE{avg_sale:.2f}"),
            ("Highest Sale", f"LE{max_sale:.2f}")
        ]

        for stat_name, stat_value in stat_data:
            stat_card = ttk.Frame(stats_frame, relief=tk.SUNKEN, borderwidth=2)
            stat_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

            name_label = ttk.Label(stat_card, text=stat_name, font=("Segoe UI", 10))
            name_label.pack(pady=(10, 5))

            value_label = ttk.Label(stat_card, text=stat_value, font=("Segoe UI", 14, "bold"))
            value_label.pack(pady=(5, 10))

        # Top products
        products_frame = ttk.LabelFrame(self.main_content, text="Top 5 Products by Sales", padding=10)
        products_frame.pack(fill=tk.X, pady=10)

        self.cursor.execute('''
                            SELECT product_name, SUM(quantity) as total_qty, SUM(total_amount) as revenue
                            FROM sales
                            WHERE user_id = ?
                            GROUP BY product_name
                            ORDER BY revenue DESC LIMIT 5
                            ''', (self.current_user['id'],))

        columns = ('Product', 'Quantity Sold', 'Revenue')
        tree = ttk.Treeview(products_frame, columns=columns, height=6, show='headings')

        for col in columns:
            tree.column(col, width=250, anchor=tk.W)
            tree.heading(col, text=col)

        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=(row[0], row[1], f"LE{row[2]:.2f}"))

        tree.pack(fill=tk.X)

        # Top customers
        customers_frame = ttk.LabelFrame(self.main_content, text="Top 5 Customers by Sales", padding=10)
        customers_frame.pack(fill=tk.X, pady=10)

        self.cursor.execute('''
                            SELECT customer_name, COUNT(*) as orders, SUM(total_amount) as revenue
                            FROM sales
                            WHERE user_id = ?
                            GROUP BY customer_name
                            ORDER BY revenue DESC LIMIT 5
                            ''', (self.current_user['id'],))

        columns = ('Customer', 'Orders', 'Revenue')
        tree = ttk.Treeview(customers_frame, columns=columns, height=6, show='headings')

        for col in columns:
            tree.column(col, width=250, anchor=tk.W)
            tree.heading(col, text=col)

        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=(row[0], row[1], f"LE{row[2]:.2f}"))

        tree.pack(fill=tk.X)

        # Payment status summary
        status_frame = ttk.LabelFrame(self.main_content, text="Payment Status Summary", padding=10)
        status_frame.pack(fill=tk.X, pady=10)

        self.cursor.execute('''
                            SELECT payment_status, COUNT(*) as count, SUM(total_amount) as amount
                            FROM sales
                            WHERE user_id = ?
                            GROUP BY payment_status
                            ''', (self.current_user['id'],))

        columns = ('Status', 'Count', 'Amount')
        tree = ttk.Treeview(status_frame, columns=columns, height=4, show='headings')

        for col in columns:
            tree.column(col, width=250, anchor=tk.W)
            tree.heading(col, text=col)

        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=(row[0], row[1], f"LE{row[2]:.2f}"))

        tree.pack(fill=tk.X)

    def export_sales_csv(self):
        """Export sales data to CSV"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"sales_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        if not file_path:
            return

        try:
            self.cursor.execute('''
                                SELECT id,
                                       product_name,
                                       customer_name,
                                       quantity,
                                       unit_price,
                                       discount,
                                       tax,
                                       total_amount,
                                       payment_status,
                                       sale_date
                                FROM sales
                                WHERE user_id = ?
                                ORDER BY sale_date DESC
                                ''', (self.current_user['id'],))

            rows = self.cursor.fetchall()

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Sale ID', 'Product', 'Customer', 'Quantity', 'Unit Price',
                                 'Discount', 'Tax', 'Total Amount', 'Payment Status', 'Date'])
                writer.writerows(rows)

            messagebox.showinfo("Success", f"Data exported successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")

    def show_about(self):
        """Display about dialog"""
        about_text = """
Sales Management System
Professional Edition v1.0

A comprehensive sales management solution with:
• User Authentication
• Sales Tracking
• Customer Management
• Product Inventory
• Sales Analytics & Reports
• Data Export

© 2026- All Rights Reserved
        """
        messagebox.showinfo("About", about_text)

    def logout_user(self):
        """Logout current user"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.show_login_window()

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SalesManagementSystem(root)
    root.mainloop()

    self.root.configure(bg=self.bg_color)

    self.current_user = "dee"
    self.init_database()
    self.show_login_window()
    def init_database(self):
        """Initialize with all required tables"""
        self.conn = sqlite3.connect('sales_system.db')
        self.cursor = self.conn.cursor()
        
        # Users' table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                company TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Product table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_code TEXT NOT NULL,
                product_name TEXT NOT NULL,
                description TEXT,
                unit_price REAL NOT NULL,
                stock_quantity INTEGER DEFAULT 0,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        # Customers' table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                zip_code TEXT,
                company_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        # Sales table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER,
                customer_id INTEGER,
                product_name TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                discount REAL DEFAULT 0,
                tax REAL DEFAULT 0,
                total_amount REAL NOT NULL,
                payment_status TEXT DEFAULT 'Pending',
                notes TEXT,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(product_id) REFERENCES products(id),
                FOREIGN KEY(customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Invoice table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                invoice_number TEXT UNIQUE,
                invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                status TEXT DEFAULT 'Unpaid',
                FOREIGN KEY(sale_id) REFERENCES sales(id)
            )
        ''')
        
        self.conn.commit()

    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def show_login_window(self):
        """Display professional login window"""
        self.clear_window()
        
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Info panel
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        left_panel.configure(height=700)
        left_inner = ttk.Frame(left_panel)
        left_inner.pack(fill=tk.BOTH, expand=True, padx=40, pady=100)
        
        title = ttk.Label(left_inner, text="Sales Management", font=("Segoe UI", 32, "bold"))
        title.pack(pady=20)
        
        subtitle = ttk.Label(left_inner, text="Group 2", font=("Segoe UI", 14))
        subtitle.pack(pady=10)
        
        info_text = ttk.Label(left_inner, text=
            "Manage your sales efficiently with our\n"
            "comprehensive management system.\n\n"
            "• Track Sales & Invoices\n"
            "• Manage Customers & Products\n"
            "• Generate Reports\n"
            "• Secure Authentication",
            font=("Segoe UI", 10), justify=tk.LEFT)
        info_text.pack(pady=40)
        
        # Right side - Login form
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        form_frame = ttk.Frame(right_panel)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=100)
        
        form_title = ttk.Label(form_frame, text="User Login", font=("Segoe UI", 18, "bold"))
        form_title.pack(pady=20)
        
        # Username field
        ttk.Label(form_frame, text="Username", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(10, 5))
        self.username_entry = ttk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.username_entry.pack(pady=(0, 15), ipady=8)
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        
        # Password field
        ttk.Label(form_frame, text="Password", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(10, 5))
        self.password_entry = ttk.Entry(form_frame, font=("Segoe UI", 10), width=30, show="●")
        self.password_entry.pack(pady=(0, 20), ipady=8)
        self.password_entry.bind('<Return>', lambda e: self.login_user())
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)
        
        login_btn = ttk.Button(button_frame, text="Login", command=self.login_user)
        login_btn.pack(side=tk.LEFT, padx=5)
        
        register_btn = ttk.Button(button_frame, text="Register", command=self.show_register_window)
        register_btn.pack(side=tk.LEFT, padx=5)

    def show_register_window(self):
        """Display registration window"""
        self.clear_window()
        
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        form_frame = ttk.Frame(main_container)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        # Title with back button
        title_frame = ttk.Frame(form_frame)
        title_frame.pack(fill=tk.X, pady=10)
        
        back_btn = ttk.Button(title_frame, text="← Back to Login", command=self.show_login_window, width=20)
        back_btn.pack(side=tk.LEFT)
        
        form_title = ttk.Label(form_frame, text="Create New Account", font=("Segoe UI", 18, "bold"))
        form_title.pack(pady=20)
        
        # Create scrollable frame
        canvas = tk.Canvas(form_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        fields = {}
        field_names = [
            ("Username", "username"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Company Name", "company"),
            ("Password", "password"),
            ("Confirm Password", "confirm_password")
        ]
        
        for label_text, field_name in field_names:
            ttk.Label(scrollable_frame, text=label_text, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(10, 5))
            entry = ttk.Entry(scrollable_frame, font=("Segoe UI", 10), width=40)
            entry.pack(pady=(0, 15), ipady=6)
            if label_text.endswith("Password"):
                entry.config(show="●")
            fields[field_name] = entry
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def register():
            username = fields["username"].get().strip()
            email = fields["email"].get().strip()
            phone = fields["phone"].get().strip()
            company = fields["company"].get().strip()
            password = fields["password"].get()
            confirm = fields["confirm_password"].get()
            
            # Validation
            if not all([username, email, password, confirm]):
                messagebox.showerror("Error", "Username, Email, and Password are required!")
                return
            
            if len(username) < 3:
                messagebox.showerror("Error", "Username must be at least 3 characters!")
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match!")
                return
            
            if len(password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters!")
                return
            
            if "@" not in email:
                messagebox.showerror("Error", "Please enter a valid email address!")
                return
            
            try:
                hashed_pwd = self.hash_password(password)
                self.cursor.execute(
                    'INSERT INTO users (username, email, phone, company, password) VALUES (?, ?, ?, ?, ?)',
                    (username, email, phone, company, hashed_pwd)
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Account created successfully! Please login.")
                self.show_login_window()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")
        
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)
        
        register_btn = ttk.Button(button_frame, text="Create Account", command=register)
        register_btn.pack(side=tk.LEFT, padx=5)

    def login_user(self):
        """Authenticate user login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return
        
        hashed_pwd = self.hash_password(password)
        self.cursor.execute('SELECT id, username, email, company FROM users WHERE username = ? AND password = ?',
                          (username, hashed_pwd))
        user = self.cursor.fetchone()
        
        if user:
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'company': user[3]
            }
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def show_dashboard(self):
        """Display the main dashboard with a menu"""
        self.clear_window()
        
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Sales to CSV", command=self.export_sales_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.logout_user)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Sales menu
        sales_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sales", menu=sales_menu)
        sales_menu.add_command(label="New Sale", command=lambda: self.show_page("add_sale"))
        sales_menu.add_command(label="View Sales", command=lambda: self.show_page("view_sales"))
        sales_menu.add_command(label="Sales Reports", command=lambda: self.show_page("reports"))
        
        # Customers menu
        customer_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Customers", menu=customer_menu)
        customer_menu.add_command(label="Add Customer", command=lambda: self.show_page("add_customer"))
        customer_menu.add_command(label="View Customers", command=lambda: self.show_page("view_customers"))
        
        # Products menu
        product_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Products", menu=product_menu)
        product_menu.add_command(label="Add Product", command=lambda: self.show_page("add_product"))
        product_menu.add_command(label="View Products", command=lambda: self.show_page("view_products"))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top header with user info
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        
        user_info = ttk.Label(header_frame, 
            text=f"User: {self.current_user['username']} | Company: {self.current_user['company'] or 'N/A'} | Email: {self.current_user['email']}", 
            font=("Segoe UI", 10))
        user_info.pack(side=tk.LEFT)
        
        logout_btn = ttk.Button(header_frame, text="Logout", command=self.logout_user, width=15)
        logout_btn.pack(side=tk.RIGHT)
        
        # Main content area
        self.main_content = ttk.Frame(main_frame)
        self.main_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Show dashboard home
        self.show_page("dashboard")

    def show_page(self, page_name):
        """Navigate to different pages"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        if page_name == "dashboard":
            self.show_dashboard_home()
        elif page_name == "add_sale":
            self.show_add_sale_form()
        elif page_name == "view_sales":
            self.show_sales_list()
        elif page_name == "add_customer":
            self.show_add_customer_form()
        elif page_name == "view_customers":
            self.show_customers_list()
        elif page_name == "add_product":
            self.show_add_product_form()
        elif page_name == "view_products":
            self.show_products_list()
        elif page_name == "reports":
            self.show_reports_page()

    def show_dashboard_home(self):
        """Display dashboard home with statistics"""
        # Title
        title = ttk.Label(self.main_content, text="Dashboard", font=("Segoe UI", 20, "bold"))
        title.pack(pady=10)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(self.main_content, text="Quick Statistics", padding=15)
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Get statistics
        self.cursor.execute('SELECT COUNT(*) FROM sales WHERE user_id = ?', (self.current_user['id'],))
        total_sales = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT SUM(total_amount) FROM sales WHERE user_id = ?', (self.current_user['id'],))
        total_revenue = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute('SELECT COUNT(*) FROM customers WHERE user_id = ?', (self.current_user['id'],))
        total_customers = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM products WHERE user_id = ?', (self.current_user['id'],))
        total_products = self.cursor.fetchone()[0]
        
        # Create stat cards
        stats_data = [
            ("Total Sales", str(total_sales), "#1f77b4"),
            ("Total Revenue", f"LE{total_revenue:.2f}", "#2ca02c"),
            ("Total Customers", str(total_customers), "#ff7f0e"),
            ("Total Products", str(total_products), "#d62728")
        ]
        
        for stat_name, stat_value, color in stats_data:
            stat_card = ttk.Frame(stats_frame, relief=tk.RAISED, borderwidth=2)
            stat_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            name_label = ttk.Label(stat_card, text=stat_name, font=("Segoe UI", 10))
            name_label.pack(pady=(10, 5))
            
            value_label = ttk.Label(stat_card, text=stat_value, font=("Segoe UI", 16, "bold"))
            value_label.pack(pady=(5, 10))
        
        # Quick actions
        actions_frame = ttk.LabelFrame(self.main_content, text="Quick Actions", padding=15)
        actions_frame.pack(fill=tk.X, pady=10)
        
        actions = [
            ("New Sale", lambda: self.show_page("add_sale")),
            ("Add Customer", lambda: self.show_page("add_customer")),
            ("Add Product", lambda: self.show_page("add_product")),
            ("View Reports", lambda: self.show_page("reports"))
        ]
        
        for action_name, action_cmd in actions:
            btn = ttk.Button(actions_frame, text=action_name, command=action_cmd, width=20)
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Recent sales
        recent_frame = ttk.LabelFrame(self.main_content, text="Recent Sales", padding=10)
        recent_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ('Sale ID', 'Product', 'Customer', 'Amount', 'Date')
        tree = ttk.Treeview(recent_frame, columns=columns, height=8, show='headings')
        
        for col in columns:
            tree.column(col, width=150, anchor=tk.CENTER)
            tree.heading(col, text=col)
        
        self.cursor.execute('''
            SELECT id, product_name, customer_name, total_amount, sale_date
            FROM sales WHERE user_id = ? ORDER BY sale_date DESC LIMIT 10
        ''', (self.current_user['id'],))
        
        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=(row[0], row[1], row[2], f"LE{row[3]:.2f}", row[4][:10]))
        
        tree.pack(fill=tk.BOTH, expand=True)

    def show_add_sale_form(self):
        """Display form to add a new sale"""
        title = ttk.Label(self.main_content, text="Add New Sale", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)
        
        # Create form frame
        form_frame = ttk.LabelFrame(self.main_content, text="Sale Details", padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create scrollable canvas
        canvas = tk.Canvas(form_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        fields = {}
        
        # Row 1: Product selection
        ttk.Label(scrollable_frame, text="Product", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        
        self.cursor.execute('SELECT id, product_name FROM products WHERE user_id = ?', (self.current_user['id'],))
        products = self.cursor.fetchall()
        product_options = [f"{p[1]} (ID: {p[0]})" for p in products]
        
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(scrollable_frame, textvariable=product_var, values=product_options, width=40)
        product_combo.grid(row=0, column=1, padx=10, pady=(10, 5), ipady=6)
        fields['product'] = product_combo
        
        # Row 1: Customer selection
        ttk.Label(scrollable_frame, text="Customer", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky=tk.W, pady=(10, 5))
        
        self.cursor.execute('SELECT id, customer_name FROM customers WHERE user_id = ?', (self.current_user['id'],))
        customers = self.cursor.fetchall()
        customer_options = [f"{c[1]} (ID: {c[0]})" for c in customers]
        
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(scrollable_frame, textvariable=customer_var, values=customer_options, width=40)
        customer_combo.grid(row=0, column=3, padx=10, pady=(10, 5), ipady=6)
        fields['customer'] = customer_combo
        
        # Row 2: Quantity
        ttk.Label(scrollable_frame, text="Quantity", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=(10, 5))
        quantity_entry = ttk.Entry(scrollable_frame, width=25)
        quantity_entry.grid(row=1, column=1, padx=10, pady=(10, 5), ipady=6)
        fields['quantity'] = quantity_entry
        
        # Row 2: Unit Price
        ttk.Label(scrollable_frame, text="Unit Price (LE)", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, sticky=tk.W, pady=(10, 5))
        price_entry = ttk.Entry(scrollable_frame, width=25)
        price_entry.grid(row=1, column=3, padx=10, pady=(10, 5), ipady=6)
        fields['price'] = price_entry
        
        # Row 3: Discount
        ttk.Label(scrollable_frame, text="Discount (LE)", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        discount_entry = ttk.Entry(scrollable_frame, width=25)
        discount_entry.insert(0, "0")
        discount_entry.grid(row=2, column=1, padx=10, pady=(10, 5), ipady=6)
        fields['discount'] = discount_entry
        
        # Row 3: Tax
        ttk.Label(scrollable_frame, text="Tax (LE)", font=("Segoe UI", 10, "bold")).grid(row=2, column=2, sticky=tk.W, pady=(10, 5))
        tax_entry = ttk.Entry(scrollable_frame, width=25)
        tax_entry.insert(0, "0")
        tax_entry.grid(row=2, column=3, padx=10, pady=(10, 5), ipady=6)
        fields['tax'] = tax_entry
        
        # Row 4: Payment Status
        ttk.Label(scrollable_frame, text="Payment Status", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        status_var = tk.StringVar(value="Pending")
        status_combo = ttk.Combobox(scrollable_frame, textvariable=status_var, values=["Pending", "Paid", "Partial"], width=23)
        status_combo.grid(row=3, column=1, padx=10, pady=(10, 5), ipady=6)
        fields['status'] = status_combo
        
        # Row 4: Sale Date
        ttk.Label(scrollable_frame, text="Sale Date", font=("Segoe UI", 10, "bold")).grid(row=3, column=2, sticky=tk.W, pady=(10, 5))
        date_entry = DateEntry(scrollable_frame, width=23)
        date_entry.grid(row=3, column=3, padx=10, pady=(10, 5), ipady=6)
        fields['date'] = date_entry
        
        # Row 5: Notes
        ttk.Label(scrollable_frame, text="Notes", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky=tk.NW, pady=(10, 5))
        notes_text = tk.Text(scrollable_frame, height=4, width=85)
        notes_text.grid(row=4, column=1, columnspan=3, padx=10, pady=(10, 5), ipady=6)
        fields['notes'] = notes_text
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        button_frame = ttk.Frame(self.main_content)
        button_frame.pack(fill=tk.X, pady=10)
        
        def save_sale():
            try:
                product_str = fields['product'].get()
                customer_str = fields['customer'].get()
                
                if not all([product_str, customer_str, fields['quantity'].get(), fields['price'].get()]):
                    messagebox.showerror("Error", "Please fill all required fields!")
                    return
                
                # Extract names from combo selections
                product_name = product_str.split(" (ID:")[0]
                customer_name = customer_str.split(" (ID:")[0]
                
                quantity = int(fields['quantity'].get())
                unit_price = float(fields['price'].get())
                discount = float(fields['discount'].get())
                tax = float(fields['tax'].get())
                total = (quantity * unit_price) - discount + tax
                
                payment_status = fields['status'].get()
                sale_date = fields['date'].get()
                notes = fields['notes'].get("1.0", tk.END).strip()
                
                self.cursor.execute('''
                    INSERT INTO sales (user_id, product_name, customer_name, quantity, unit_price, 
                                      discount, tax, total_amount, payment_status, notes, sale_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (self.current_user['id'], product_name, customer_name, quantity, unit_price,
                      discount, tax, total, payment_status, notes, sale_date))
                
                self.conn.commit()
                messagebox.showinfo("Success", "Sale record saved successfully!")
                self.show_page("view_sales")
            except ValueError as e:
                messagebox.showerror("Error", "Please enter valid numbers for quantity, price, discount, and tax!")
        
        save_btn = ttk.Button(button_frame, text="Save Sale", command=save_sale, width=20)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = ttk.Button(button_frame, text="Reset Form", command=lambda: self.show_page("add_sale"), width=20)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=lambda: self.show_page("dashboard"), width=20)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def show_sales_list(self):
        """Display all sales records with filtering and search"""
        title = ttk.Label(self.main_content, text="Sales Records", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)
        
        # Filter frame
        filter_frame = ttk.LabelFrame(self.main_content, text="Filters", padding=10)
        filter_frame.pack(fill=tk.X, pady=10)
        
        # Search
        ttk.Label(filter_frame, text="Search by Customer/Product:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Payment Status filter
        ttk.Label(filter_frame, text="Payment Status:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(filter_frame, textvariable=status_var, values=["All", "Pending", "Paid", "Partial"], width=15)
        status_combo.pack(side=tk.LEFT, padx=5)
        
        # Date range
        ttk.Label(filter_frame, text="From Date:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        from_date = DateEntry(filter_frame, width=15)
        from_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="To Date:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        to_date = DateEntry(filter_frame, width=15)
        to_date.pack(side=tk.LEFT, padx=5)
        
        # Table frame
        table_frame = ttk.LabelFrame(self.main_content, text="Sales Table", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ('Sale ID', 'Product', 'Customer', 'Quantity', 'Unit Price', 'Discount', 'Tax', 'Total', 'Status', 'Date')
        tree = ttk.Treeview(table_frame, columns=columns, height=15, show='headings')
        
        col_widths = [60, 100, 100, 70, 80, 70, 60, 80, 80, 100]
        for col, width in zip(columns, col_widths):
            tree.column(col, width=width, anchor=tk.CENTER)
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        def load_data():
            for item in tree.get_children():
                tree.delete(item)
            
            query = 'SELECT * FROM sales WHERE user_id = ?'
            params = [self.current_user['id']]
            
            search_term = search_var.get()
            if search_term:
                query += ' AND (product_name LIKE ? OR customer_name LIKE ?)'
                params.extend([f'%{search_term}%', f'%{search_term}%'])
            
            if status_var.get() != 'All':
                query += ' AND payment_status = ?'
                params.append(status_var.get())
            
            from_str = from_date.get_date().isoformat()
            to_str = to_date.get_date().isoformat()
            query += ' AND DATE(sale_date) BETWEEN ? AND ?'
            params.extend([from_str, to_str])
            
            query += ' ORDER BY sale_date DESC'
            
            self.cursor.execute(query, params)
            for row in self.cursor.fetchall():
                tree.insert('', 'end', values=(row[0], row[2], row[3], row[4], f"${row[5]:.2f}", 
                                              f"${row[6]:.2f}", f"${row[7]:.2f}", f"${row[8]:.2f}", 
                                              row[9], row[12][:10]))
        
        load_btn = ttk.Button(filter_frame, text="Apply Filters", command=load_data)
        load_btn.pack(side=tk.RIGHT, padx=5)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        load_data()

    def show_add_customer_form(self):
        """Display form to add a new customer"""
        title = ttk.Label(self.main_content, text="Add New Customer", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)
        
        form_frame = ttk.LabelFrame(self.main_content, text="Customer Information", padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        fields = {}
        
        # Row 1: Name and Email
        ttk.Label(form_frame, text="Customer Name *", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=10)
        name_entry = ttk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10, ipady=6)
        fields['name'] = name_entry
        
        ttk.Label(form_frame, text="Email", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky=tk.W, pady=10)
        email_entry = ttk.Entry(form_frame, width=30)
        email_entry.grid(row=0, column=3, padx=10, pady=10, ipady=6)
        fields['email'] = email_entry
        
        # Row 2: Phone and Company
        ttk.Label(form_frame, text="Phone", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=10)
        phone_entry = ttk.Entry(form_frame, width=30)
        phone_entry.grid(row=1, column=1, padx=10, pady=10, ipady=6)
        fields['phone'] = phone_entry
        
        ttk.Label(form_frame, text="Company Name", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, sticky=tk.W, pady=10)
        company_entry = ttk.Entry(form_frame, width=30)
        company_entry.grid(row=1, column=3, padx=10, pady=10, ipady=6)
        fields['company'] = company_entry
        
        # Row 3: Address
        ttk.Label(form_frame, text="Address", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=10)
        address_entry = ttk.Entry(form_frame, width=30)
        address_entry.grid(row=2, column=1, padx=10, pady=10, ipady=6)
        fields['address'] = address_entry
        
        # Row 4: City, State, ZIP
        ttk.Label(form_frame, text="City", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=10)
        city_entry = ttk.Entry(form_frame, width=30)
        city_entry.grid(row=3, column=1, padx=10, pady=10, ipady=6)
        fields['city'] = city_entry
        
        ttk.Label(form_frame, text="State", font=("Segoe UI", 10, "bold")).grid(row=3, column=2, sticky=tk.W, pady=10)
        state_entry = ttk.Entry(form_frame, width=30)
        state_entry.grid(row=3, column=3, padx=10, pady=10, ipady=6)
        fields['state'] = state_entry
        
        ttk.Label(form_frame, text="ZIP Code", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=10)
        zip_entry = ttk.Entry(form_frame, width=30)
        zip_entry.grid(row=4, column=1, padx=10, pady=10, ipady=6)
        fields['zip'] = zip_entry
        
        # Button frame
        button_frame = ttk.Frame(self.main_content)
        button_frame.pack(fill=tk.X, pady=10)
        
        def save_customer():
            name = fields['name'].get().strip()
            if not name:
                messagebox.showerror("Error", "Customer name is required!")
                return
            
            try:
                self.cursor.execute('''
                    INSERT INTO customers (user_id, customer_name, email, phone, company_name, address, city, state, zip_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (self.current_user['id'], name, fields['email'].get(), fields['phone'].get(),
                      fields['company'].get(), fields['address'].get(), fields['city'].get(),
                      fields['state'].get(), fields['zip'].get()))
                
                self.conn.commit()
                messagebox.showinfo("Success", "Customer added successfully!")
                self.show_page("view_customers")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save customer: {str(e)}")
        
        save_btn = ttk.Button(button_frame, text="Save Customer", command=save_customer, width=20)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=lambda: self.show_page("dashboard"), width=20)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def show_customers_list(self):
        """Display all customers"""
        title = ttk.Label(self.main_content, text="Customers", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)
        
        # Search frame
        search_frame = ttk.LabelFrame(self.main_content, text="Search", padding=10)
        search_frame.pack(fill=tk.X, pady=10)
        
        search_var = tk.StringVar()
        ttk.Label(search_frame, text="Search by name or email:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Table frame
        table_frame = ttk.LabelFrame(self.main_content, text="Customers Table", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ('ID', 'Name', 'Email', 'Phone', 'Company', 'City', 'State')
        tree = ttk.Treeview(table_frame, columns=columns, height=15, show='headings')
        
        for col in columns:
            tree.column(col, width=120, anchor=tk.W)
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        def load_data():
            for item in tree.get_children():
                tree.delete(item)
            
            search_term = search_var.get()
            if search_term:
                query = 'SELECT * FROM customers WHERE user_id = ? AND (customer_name LIKE ? OR email LIKE ?)'
                params = [self.current_user['id'], f'%{search_term}%', f'%{search_term}%']
            else:
                query = 'SELECT * FROM customers WHERE user_id = ?'
                params = [self.current_user['id']]
            
            self.cursor.execute(query, params)
            for row in self.cursor.fetchall():
                tree.insert('', 'end', values=(row[0], row[2], row[3], row[4], row[8], row[6], row[7]))
        
        search_btn = ttk.Button(search_frame, text="Search", command=load_data)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        load_data()

    def show_add_product_form(self):
        """Display form to add a new product"""
        title = ttk.Label(self.main_content, text="Add New Product", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)
        
        form_frame = ttk.LabelFrame(self.main_content, text="Product Information", padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        fields = {}
        
        # Row 1: Product Code and Name
        ttk.Label(form_frame, text="Product Code *", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=10)
        code_entry = ttk.Entry(form_frame, width=30)
        code_entry.grid(row=0, column=1, padx=10, pady=10, ipady=6)
        fields['code'] = code_entry
        
        ttk.Label(form_frame, text="Product Name *", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky=tk.W, pady=10)
        name_entry = ttk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=3, padx=10, pady=10, ipady=6)
        fields['name'] = name_entry
        
        # Row 2: Category and Price
        ttk.Label(form_frame, text="Category", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=10)
        category_entry = ttk.Entry(form_frame, width=30)
        category_entry.grid(row=1, column=1, padx=10, pady=10, ipady=6)
        fields['category'] = category_entry
        
        ttk.Label(form_frame, text="Unit Price (LE) *", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, sticky=tk.W, pady=10)
        price_entry = ttk.Entry(form_frame, width=30)
        price_entry.grid(row=1, column=3, padx=10, pady=10, ipady=6)
        fields['price'] = price_entry
        
        # Row 3: Stock and Description
        ttk.Label(form_frame, text="Stock Quantity", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=10)
        stock_entry = ttk.Entry(form_frame, width=30)
        stock_entry.insert(0, "0")
        stock_entry.grid(row=2, column=1, padx=10, pady=10, ipady=6)
        fields['stock'] = stock_entry
        
        ttk.Label(form_frame, text="Description", font=("Segoe UI", 10, "bold")).grid(row=2, column=2, sticky=tk.NW, pady=10)
        desc_text = tk.Text(form_frame, height=4, width=30)
        desc_text.grid(row=2, column=3, padx=10, pady=10, ipady=6)
        fields['description'] = desc_text
        
        # Button frame
        button_frame = ttk.Frame(self.main_content)
        button_frame.pack(fill=tk.X, pady=10)
        
        def save_product():
            code = fields['code'].get().strip()
            name = fields['name'].get().strip()
            price = fields['price'].get()
            
            if not all([code, name, price]):
                messagebox.showerror("Error", "Product Code, Name, and Price are required!")
                return
            
            try:
                unit_price = float(price)
                stock = int(fields['stock'].get())
                
                self.cursor.execute('''
                    INSERT INTO products (user_id, product_code, product_name, category, unit_price, stock_quantity, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (self.current_user['id'], code, name, fields['category'].get(),
                      unit_price, stock, fields['description'].get("1.0", tk.END).strip()))
                
                self.conn.commit()
                messagebox.showinfo("Success", "Product added successfully!")
                self.show_page("view_products")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price and stock!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Product code already exists!")
        
        save_btn = ttk.Button(button_frame, text="Save Product", command=save_product, width=20)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=lambda: self.show_page("dashboard"), width=20)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def show_products_list(self):
        """Display all products"""
        title = ttk.Label(self.main_content, text="Products", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)
        
        # Search frame
        search_frame = ttk.LabelFrame(self.main_content, text="Search", padding=10)
        search_frame.pack(fill=tk.X, pady=10)
        
        search_var = tk.StringVar()
        ttk.Label(search_frame, text="Search by name or code:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Table frame
        table_frame = ttk.LabelFrame(self.main_content, text="Products Table", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ('ID', 'Code', 'Name', 'Category', 'Unit Price', 'Stock', 'Date Added')
        tree = ttk.Treeview(table_frame, columns=columns, height=15, show='headings')
        
        col_widths = [40, 80, 120, 100, 100, 80, 100]
        for col, width in zip(columns, col_widths):
            tree.column(col, width=width, anchor=tk.W)
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        def load_data():
            for item in tree.get_children():
                tree.delete(item)
            
            search_term = search_var.get()
            if search_term:
                query = 'SELECT * FROM products WHERE user_id = ? AND (product_name LIKE ? OR product_code LIKE ?)'
                params = [self.current_user['id'], f'%{search_term}%', f'%{search_term}%']
            else:
                query = 'SELECT * FROM products WHERE user_id = ?'
                params = [self.current_user['id']]
            
            self.cursor.execute(query, params)
            for row in self.cursor.fetchall():
                tree.insert('', 'end', values=(row[0], row[2], row[3], row[4], f"${row[5]:.2f}", row[6], row[8][:10]))
        
        search_btn = ttk.Button(search_frame, text="Search", command=load_data)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        load_data()

    def show_reports_page(self):
        """Display reports and analytics"""
        title = ttk.Label(self.main_content, text="Sales Reports & Analytics", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)
        
        # Summary statistics
        stats_frame = ttk.LabelFrame(self.main_content, text="Summary Statistics", padding=15)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.cursor.execute('''
            SELECT 
                COUNT(*) as total_sales,
                SUM(total_amount) as total_revenue,
                AVG(total_amount) as avg_sale,
                MAX(total_amount) as max_sale
            FROM sales WHERE user_id = ?
        ''', (self.current_user['id'],))
        
        stats = self.cursor.fetchone()
        total_sales = stats[0] or 0
        total_revenue = stats[1] or 0
        avg_sale = stats[2] or 0
        max_sale = stats[3] or 0
        
        # Display statistics in cards
        stat_data = [
            ("Total Sales", str(total_sales)),
            ("Total Revenue", f"LE{total_revenue:.2f}"),
            ("Average Sale", f"LE{avg_sale:.2f}"),
            ("Highest Sale", f"LE{max_sale:.2f}")
        ]
        
        for stat_name, stat_value in stat_data:
            stat_card = ttk.Frame(stats_frame, relief=tk.SUNKEN, borderwidth=2)
            stat_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            name_label = ttk.Label(stat_card, text=stat_name, font=("Segoe UI", 10))
            name_label.pack(pady=(10, 5))
            
            value_label = ttk.Label(stat_card, text=stat_value, font=("Segoe UI", 14, "bold"))
            value_label.pack(pady=(5, 10))
        
        # Top products
        products_frame = ttk.LabelFrame(self.main_content, text="Top 5 Products by Sales", padding=10)
        products_frame.pack(fill=tk.X, pady=10)
        
        self.cursor.execute('''
            SELECT product_name, SUM(quantity) as total_qty, SUM(total_amount) as revenue
            FROM sales WHERE user_id = ?
            GROUP BY product_name
            ORDER BY revenue DESC LIMIT 5
        ''', (self.current_user['id'],))
        
        columns = ('Product', 'Quantity Sold', 'Revenue')
        tree = ttk.Treeview(products_frame, columns=columns, height=6, show='headings')
        
        for col in columns:
            tree.column(col, width=250, anchor=tk.W)
            tree.heading(col, text=col)
        
        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=(row[0], row[1], f"LE{row[2]:.2f}"))
        
        tree.pack(fill=tk.X)
        
        # Top customers
        customers_frame = ttk.LabelFrame(self.main_content, text="Top 5 Customers by Sales", padding=10)
        customers_frame.pack(fill=tk.X, pady=10)
        
        self.cursor.execute('''
            SELECT customer_name, COUNT(*) as orders, SUM(total_amount) as revenue
            FROM sales WHERE user_id = ?
            GROUP BY customer_name
            ORDER BY revenue DESC LIMIT 5
        ''', (self.current_user['id'],))
        
        columns = ('Customer', 'Orders', 'Revenue')
        tree = ttk.Treeview(customers_frame, columns=columns, height=6, show='headings')
        
        for col in columns:
            tree.column(col, width=250, anchor=tk.W)
            tree.heading(col, text=col)
        
        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=(row[0], row[1], f"LE{row[2]:.2f}"))
        
        tree.pack(fill=tk.X)
        
        # Payment status summary
        status_frame = ttk.LabelFrame(self.main_content, text="Payment Status Summary", padding=10)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.cursor.execute('''
            SELECT payment_status, COUNT(*) as count, SUM(total_amount) as amount
            FROM sales WHERE user_id = ?
            GROUP BY payment_status
        ''', (self.current_user['id'],))
        
        columns = ('Status', 'Count', 'Amount')
        tree = ttk.Treeview(status_frame, columns=columns, height=4, show='headings')
        
        for col in columns:
            tree.column(col, width=250, anchor=tk.W)
            tree.heading(col, text=col)
        
        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=(row[0], row[1], f"LE{row[2]:.2f}"))
        
        tree.pack(fill=tk.X)

    def export_sales_csv(self):
        """Export sales data to CSV"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"sales_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if not file_path:
            return
        
        try:
            self.cursor.execute('''
                SELECT id, product_name, customer_name, quantity, unit_price, discount, 
                       tax, total_amount, payment_status, sale_date
                FROM sales WHERE user_id = ? ORDER BY sale_date DESC
            ''', (self.current_user['id'],))
            
            rows = self.cursor.fetchall()
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Sale ID', 'Product', 'Customer', 'Quantity', 'Unit Price', 
                               'Discount', 'Tax', 'Total Amount', 'Payment Status', 'Date'])
                writer.writerows(rows)
            
            messagebox.showinfo("Success", f"Data exported successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")

    def show_about(self):
        """Display about dialog"""
        about_text = """
Sales Management System
Professional Edition v1.0

A comprehensive sales management solution with:
• User Authentication
• Sales Tracking
• Customer Management
• Product Inventory
• Sales Analytics & Reports
• Data Export

© 2026- All Rights Reserved
        """
        messagebox.showinfo("About", about_text)

    def logout_user(self):
        """Logout current user"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.show_login_window()

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SalesManagementSystem(root)
    root.mainloop()
