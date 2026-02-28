# 03_login_register.py
"""
PART 3/5 - Login and Register Pages
Run Order: Third
"""
from config import tk, messagebox, LOGIN_BG, LOGIN_CARD_BG, LOGIN_ACCENT, LOGIN_BUTTON, LOGIN_BG, BORDER, TEXT_MAIN, TEXT_MUTED, FONT_NORMAL, FONT_SMALL, ACCENT
from Authbase import Authbase

class LoginRegisterPages(Authbase):
    def __init__(self, app):
        super().__init__(app)

    # ------------- LOGIN PAGE -------------
    def show_login_page(self):
        self.clear_window()

        main_container = tk.Frame(self.app, bg=LOGIN_BG)
        main_container.pack(fill="both", expand=True)

        card_inner = self.create_card(main_container)
        self.create_logo_header(card_inner)

        # Welcome text
        welcome_label = tk.Label(
            card_inner,
            text="Welcome Back!",
            font=("Segoe UI", 20, "bold"),
            bg=LOGIN_CARD_BG,
            fg=LOGIN_BG
        )
        welcome_label.pack(pady=(0, 10))

        subtitle_label = tk.Label(
            card_inner,
            text="Please login to your account",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MUTED
        )
        subtitle_label.pack(pady=(0, 25))

        # Username field
        username_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        username_frame.pack(fill="x", pady=(0, 15))

        username_label = tk.Label(
            username_frame,
            text="Username",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MAIN,
            anchor="w"
        )
        username_label.pack(fill="x")

        username_entry = tk.Entry(
            username_frame,
            font=FONT_NORMAL,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=LOGIN_ACCENT,
            highlightbackground=BORDER
        )
        username_entry.pack(fill="x", ipady=8, pady=(5, 0))

        # Password field
        password_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        password_frame.pack(fill="x", pady=(0, 20))

        password_label = tk.Label(
            password_frame,
            text="Password",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MAIN,
            anchor="w"
        )
        password_label.pack(fill="x")

        password_entry = tk.Entry(
            password_frame,
            font=FONT_NORMAL,
            show="•",
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=LOGIN_ACCENT,
            highlightbackground=BORDER
        )
        password_entry.pack(fill="x", ipady=8, pady=(5, 0))

        # Options
        options_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        options_frame.pack(fill="x", pady=(0, 25))

        remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(
            options_frame,
            text="Remember me",
            variable=remember_var,
            bg=LOGIN_CARD_BG,
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            selectcolor=LOGIN_CARD_BG
        )
        remember_check.pack(side="left")

        forgot_label = tk.Label(
            options_frame,
            text="Forgot Password?",
            font=FONT_SMALL,
            bg=LOGIN_CARD_BG,
            fg=LOGIN_ACCENT,
            cursor="hand2"
        )
        forgot_label.pack(side="right")
        forgot_label.bind("<Button-1>", lambda e: self.app.show_forgot_password_page())

        # Login button
        def login_click():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if self.app.validate_login(username, password):
                messagebox.showinfo("Success", "Login successful!")
                self.app.show_main_app()
            else:
                messagebox.showerror("Error", "Invalid username or password")

        login_button = tk.Button(
            card_inner,
            text="LOGIN",
            font=("Segoe UI", 12, "bold"),
            bg=LOGIN_BUTTON,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=login_click,
            padx=30,
            pady=10
        )
        login_button.pack(fill="x", pady=(0, 20))

        # Register link
        register_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        register_frame.pack(fill="x")

        no_account_label = tk.Label(
            register_frame,
            text="Don't have an account? ",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MUTED
        )
        no_account_label.pack(side="left")

        register_link = tk.Label(
            register_frame,
            text="Register",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=LOGIN_ACCENT,
            cursor="hand2"
        )
        register_link.pack(side="left")
        register_link.bind("<Button-1>", lambda e: self.app.show_register_page())

    # ------------- REGISTER PAGE -------------
    def show_register_page(self):
        self.clear_window()

        main_container = tk.Frame(self.app, bg=LOGIN_BG)
        main_container.pack(fill="both", expand=True)

        card_inner = self.create_card(main_container)
        self.create_logo_header(card_inner)

        welcome_label = tk.Label(
            card_inner,
            text="Create Account",
            font=("Segoe UI", 20, "bold"),
            bg=LOGIN_CARD_BG,
            fg=LOGIN_BG
        )
        welcome_label.pack(pady=(0, 10))

        subtitle_label = tk.Label(
            card_inner,
            text="Register as a new user",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MUTED
        )
        subtitle_label.pack(pady=(0, 25))

        # Form fields
        name_entry = self.create_entry_field(card_inner, "Full Name")
        email_entry = self.create_entry_field(card_inner, "Email")
        username_entry = self.create_entry_field(card_inner, "Username")
        password_entry = self.create_entry_field(card_inner, "Password", show="•")
        confirm_entry = self.create_entry_field(card_inner, "Confirm Password", show="•")

        # Terms
        terms_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        terms_frame.pack(fill="x", pady=(0, 25))

        terms_var = tk.BooleanVar()
        terms_check = tk.Checkbutton(
            terms_frame,
            text="I agree to the Terms and Conditions",
            variable=terms_var,
            bg=LOGIN_CARD_BG,
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            selectcolor=LOGIN_CARD_BG
        )
        terms_check.pack(side="left")

        def register_click():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()
            
            if not all([name, email, username, password, confirm]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            if len(password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters")
                return
            
            if not terms_var.get():
                messagebox.showerror("Error", "Please accept the Terms and Conditions")
                return
            
            created, error_message = self.app.create_user(name, email, username, password)
            if not created:
                messagebox.showerror("Error", error_message or "Registration failed")
                return
            
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login_page()

        register_button = tk.Button(
            card_inner,
            text="REGISTER",
            font=("Segoe UI", 12, "bold"),
            bg=LOGIN_ACCENT,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=register_click,
            padx=30,
            pady=10
        )
        register_button.pack(fill="x", pady=(0, 20))

        # Login link
        login_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        login_frame.pack(fill="x")

        have_account_label = tk.Label(
            login_frame,
            text="Already have an account? ",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MUTED
        )
        have_account_label.pack(side="left")

        login_link = tk.Label(
            login_frame,
            text="Login",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=LOGIN_ACCENT,
            cursor="hand2"
        )
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.show_login_page())
if __name__ == "__main__":
    from main_app import HospitalApp

    app = HospitalApp()
    app.show_login_page()
    app.mainloop()
