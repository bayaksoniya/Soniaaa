import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import random
import string

# ------------- Global colors / fonts -------------
BG_MAIN = "#f3e9ef"
BG_SIDEBAR = "#f5f7f2"
BG_TOPBAR = "#ffffff"
BG_CARD = "#ffffff"
BG_PRIMARY = "#1fb6ff"
BG_SOFT_BLUE = "#e4f1ff"
BORDER = "#d0d0d0"
TEXT_MAIN = "#222222"
TEXT_MUTED = "#555555"
ACCENT = "#f97373"

# Login/Register theme colors
LOGIN_BG = "#1a2b3c"  # Dark blue-gray background
LOGIN_CARD_BG = "#ffffff"
LOGIN_ACCENT = "#2ecc71"  # Green accent
LOGIN_BUTTON = "#3498db"  # Blue button
LOGIN_BUTTON_HOVER = "#2980b9"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUBTITLE = ("Segoe UI", 13, "bold")
FONT_NORMAL = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)


class HospitalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NIMA Hospital - Login")
        self.geometry("1080x650")
        self.configure(bg=LOGIN_BG)
        self.resizable(True, True)

        # Store user data (simulated database)
        self.users = {
            "admin": {
                "password": "password",
                "email": "admin@nima-hospital.com",
                "name": "Administrator"
            }
        }
        
        # Temporary storage for password reset codes
        self.reset_codes = {}

        # notifications data
        self.notifications = [
            "2 new patients registered.",
            "Lab report ready for Patient #1021.",
            "Staff meeting at 3:00 PM.",
        ]

        # image storage
        self.images = {}
        self.load_images()

        # Start with login page
        self.show_login_page()

    # ------------- IMAGE LOADING -------------
    def load_images(self):
        def load(name, filename, size=None):
            path = os.path.join(os.path.dirname(__file__), filename)
            if not os.path.exists(path):
                self.images[name] = None
                return
            img = Image.open(path)
            if size:
                img = img.resize(size, Image.ANTIALIAS)
            self.images[name] = ImageTk.PhotoImage(img)

        load("logo", "logo.png", (42, 42))
        load("doctor_best", "doctor1.png", (120, 140))
        load("login_illustration", "login_illustration.png", (300, 300))

        load("icon_dashboard", "icon_dashboard.png", (20, 20))
        load("icon_doctors", "icon_doctors.png", (20, 20))
        load("icon_message", "icon_message.png", (20, 20))
        load("icon_schedule", "icon_schedule.png", (20, 20))
        load("icon_settings", "icon_settings.png", (20, 20))
        load("icon_logout", "icon_logout.png", (20, 20))

    # ------------- FORGOT PASSWORD PAGE -------------
    def show_forgot_password_page(self):
        # Clear existing content
        for widget in self.winfo_children():
            widget.destroy()

        # Main container
        main_container = tk.Frame(self, bg=LOGIN_BG)
        main_container.pack(fill="both", expand=True)

        # Center card
        card = tk.Frame(main_container, bg=LOGIN_CARD_BG, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Create card with shadow effect
        card_inner = tk.Frame(card, bg=LOGIN_CARD_BG, padx=40, pady=40)
        card_inner.pack()

        # Logo and title
        logo_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        logo_frame.pack(pady=(0, 20))

        if self.images.get("logo"):
            logo_lbl = tk.Label(logo_frame, image=self.images["logo"], bg=LOGIN_CARD_BG)
            logo_lbl.pack(side="left", padx=(0, 10))

        title_label = tk.Label(
            logo_frame,
            text="NIMA HOSPITAL",
            font=("Segoe UI", 24, "bold"),
            bg=LOGIN_CARD_BG,
            fg=LOGIN_BG
        )
        title_label.pack(side="left")

        # Title
        reset_label = tk.Label(
            card_inner,
            text="Reset Password",
            font=("Segoe UI", 20, "bold"),
            bg=LOGIN_CARD_BG,
            fg=LOGIN_BG
        )
        reset_label.pack(pady=(0, 10))

        subtitle_label = tk.Label(
            card_inner,
            text="Enter your email to receive reset instructions",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MUTED
        )
        subtitle_label.pack(pady=(0, 25))

        # Email field
        email_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        email_frame.pack(fill="x", pady=(0, 20))

        email_label = tk.Label(
            email_frame,
            text="Email Address",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MAIN,
            anchor="w"
        )
        email_label.pack(fill="x")

        email_entry = tk.Entry(
            email_frame,
            font=FONT_NORMAL,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=LOGIN_ACCENT,
            highlightbackground=BORDER
        )
        email_entry.pack(fill="x", ipady=8, pady=(5, 0))

        # Send reset button
        def send_reset():
            email = email_entry.get().strip()
            
            if not email:
                messagebox.showerror("Error", "Please enter your email address")
                return
            
            # Check if email exists in our "database"
            user_found = False
            username = None
            for uname, user_data in self.users.items():
                if user_data["email"] == email:
                    user_found = True
                    username = uname
                    break
            
            if user_found:
                # Generate a random reset code
                reset_code = ''.join(random.choices(string.digits, k=6))
                self.reset_codes[email] = reset_code
                
                # In a real app, you would send an email here
                # For demo, we'll show the code in a messagebox
                messagebox.showinfo(
                    "Reset Code", 
                    f"DEMO MODE - Reset code: {reset_code}\n\nIn a real application, this would be sent to your email."
                )
                
                # Show reset code entry page
                self.show_reset_code_page(email, username)
            else:
                messagebox.showerror("Error", "Email not found in our records")

        send_button = tk.Button(
            card_inner,
            text="SEND RESET LINK",
            font=("Segoe UI", 12, "bold"),
            bg=LOGIN_BUTTON,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=send_reset,
            padx=30,
            pady=10
        )
        send_button.pack(fill="x", pady=(0, 20))

        # Back to login link
        back_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        back_frame.pack(fill="x")

        back_link = tk.Label(
            back_frame,
            text="← Back to Login",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=LOGIN_ACCENT,
            cursor="hand2"
        )
        back_link.pack()
        back_link.bind("<Button-1>", lambda e: self.show_login_page())

    # ------------- RESET CODE PAGE -------------
    def show_reset_code_page(self, email, username):
        # Clear existing content
        for widget in self.winfo_children():
            widget.destroy()

        # Main container
        main_container = tk.Frame(self, bg=LOGIN_BG)
        main_container.pack(fill="both", expand=True)

        # Center card
        card = tk.Frame(main_container, bg=LOGIN_CARD_BG, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Create card with shadow effect
        card_inner = tk.Frame(card, bg=LOGIN_CARD_BG, padx=40, pady=40)
        card_inner.pack()

        # Logo and title
        logo_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        logo_frame.pack(pady=(0, 20))

        if self.images.get("logo"):
            logo_lbl = tk.Label(logo_frame, image=self.images["logo"], bg=LOGIN_CARD_BG)
            logo_lbl.pack(side="left", padx=(0, 10))

        title_label = tk.Label(
            logo_frame,
            text="NIMA HOSPITAL",
            font=("Segoe UI", 24, "bold"),
            bg=LOGIN_CARD_BG,
            fg=LOGIN_BG
        )
        title_label.pack(side="left")

        # Title
        code_label = tk.Label(
            card_inner,
            text="Enter Reset Code",
            font=("Segoe UI", 20, "bold"),
            bg=LOGIN_CARD_BG,
            fg=LOGIN_BG
        )
        code_label.pack(pady=(0, 10))

        subtitle_label = tk.Label(
            card_inner,
            text=f"Enter the 6-digit code sent to {email}",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MUTED
        )
        subtitle_label.pack(pady=(0, 25))

        # Code field
        code_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        code_frame.pack(fill="x", pady=(0, 20))

        code_label = tk.Label(
            code_frame,
            text="Reset Code",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MAIN,
            anchor="w"
        )
        code_label.pack(fill="x")

        code_entry = tk.Entry(
            code_frame,
            font=FONT_NORMAL,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=LOGIN_ACCENT,
            highlightbackground=BORDER
        )
        code_entry.pack(fill="x", ipady=8, pady=(5, 0))

        # Verify code button
        def verify_code():
            entered_code = code_entry.get().strip()
            stored_code = self.reset_codes.get(email)
            
            if not entered_code:
                messagebox.showerror("Error", "Please enter the reset code")
                return
            
            if stored_code and entered_code == stored_code:
                # Code correct, show new password page
                self.show_new_password_page(email, username)
            else:
                messagebox.showerror("Error", "Invalid reset code")

        verify_button = tk.Button(
            card_inner,
            text="VERIFY CODE",
            font=("Segoe UI", 12, "bold"),
            bg=LOGIN_BUTTON,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=verify_code,
            padx=30,
            pady=10
        )
        verify_button.pack(fill="x", pady=(0, 15))

        # Resend code link
        resend_link = tk.Label(
            card_inner,
            text="Resend Code",
            font=FONT_SMALL,
            bg=LOGIN_CARD_BG,
            fg=LOGIN_ACCENT,
            cursor="hand2"
        )
        resend_link.pack(pady=(0, 15))
        
        def resend_code():
            # Generate new code
            new_code = ''.join(random.choices(string.digits, k=6))
            self.reset_codes[email] = new_code
            messagebox.showinfo("Code Resent", f"DEMO MODE - New code: {new_code}")
        
        resend_link.bind("<Button-1>", lambda e: resend_code())

        # Back to login link
        back_link = tk.Label(
            card_inner,
            text="← Back to Login",
            font=FONT_SMALL,
            bg=LOGIN_CARD_BG,
            fg=LOGIN_ACCENT,
            cursor="hand2"
        )
        back_link.pack()
        back_link.bind("<Button-1>", lambda e: self.show_login_page())

    # ------------- NEW PASSWORD PAGE -------------
    def show_new_password_page(self, email, username):
        # Clear existing content
        for widget in self.winfo_children():
            widget.destroy()

        # Main container
        main_container = tk.Frame(self, bg=LOGIN_BG)
        main_container.pack(fill="both", expand=True)

        # Center card
        card = tk.Frame(main_container, bg=LOGIN_CARD_BG, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Create card with shadow effect
        card_inner = tk.Frame(card, bg=LOGIN_CARD_BG, padx=40, pady=40)
        card_inner.pack()

        # Logo and title
        logo_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        logo_frame.pack(pady=(0, 20))

        if self.images.get("logo"):
            logo_lbl = tk.Label(logo_frame, image=self.images["logo"], bg=LOGIN_CARD_BG)
            logo_lbl.pack(side="left", padx=(0, 10))

        title_label = tk.Label(
            logo_frame,
            text="NIMA HOSPITAL",
            font=("Segoe UI", 24, "bold"),
            bg=LOGIN_CARD_BG,
            fg=LOGIN_BG
        )
        title_label.pack(side="left")

        # Title
        newpass_label = tk.Label(
            card_inner,
            text="Create New Password",
            font=("Segoe UI", 20, "bold"),
            bg=LOGIN_CARD_BG,
            fg=LOGIN_BG
        )
        newpass_label.pack(pady=(0, 10))

        subtitle_label = tk.Label(
            card_inner,
            text="Enter your new password below",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MUTED
        )
        subtitle_label.pack(pady=(0, 25))

        # New Password field
        newpass_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        newpass_frame.pack(fill="x", pady=(0, 15))

        newpass_label = tk.Label(
            newpass_frame,
            text="New Password",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MAIN,
            anchor="w"
        )
        newpass_label.pack(fill="x")

        newpass_entry = tk.Entry(
            newpass_frame,
            font=FONT_NORMAL,
            show="•",
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=LOGIN_ACCENT,
            highlightbackground=BORDER
        )
        newpass_entry.pack(fill="x", ipady=8, pady=(5, 0))

        # Confirm Password field
        confirm_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        confirm_frame.pack(fill="x", pady=(0, 20))

        confirm_label = tk.Label(
            confirm_frame,
            text="Confirm Password",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MAIN,
            anchor="w"
        )
        confirm_label.pack(fill="x")

        confirm_entry = tk.Entry(
            confirm_frame,
            font=FONT_NORMAL,
            show="•",
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=LOGIN_ACCENT,
            highlightbackground=BORDER
        )
        confirm_entry.pack(fill="x", ipady=8, pady=(5, 0))

        # Reset password button
        def reset_password():
            newpass = newpass_entry.get().strip()
            confirm = confirm_entry.get().strip()
            
            if not newpass or not confirm:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            if newpass != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            if len(newpass) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters")
                return
            
            # Update password in our "database"
            self.users[username]["password"] = newpass
            
            # Clear the reset code
            if email in self.reset_codes:
                del self.reset_codes[email]
            
            messagebox.showinfo("Success", "Password reset successful! Please login with your new password.")
            self.show_login_page()

        reset_button = tk.Button(
            card_inner,
            text="RESET PASSWORD",
            font=("Segoe UI", 12, "bold"),
            bg=LOGIN_ACCENT,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=reset_password,
            padx=30,
            pady=10
        )
        reset_button.pack(fill="x", pady=(0, 20))

        # Back to login link
        back_link = tk.Label(
            card_inner,
            text="← Back to Login",
            font=FONT_SMALL,
            bg=LOGIN_CARD_BG,
            fg=LOGIN_ACCENT,
            cursor="hand2"
        )
        back_link.pack()
        back_link.bind("<Button-1>", lambda e: self.show_login_page())

    # ------------- LOGIN PAGE -------------
    def show_login_page(self):
        # Clear existing content
        for widget in self.winfo_children():
            widget.destroy()

        # Main container with gradient effect
        main_container = tk.Frame(self, bg=LOGIN_BG)
        main_container.pack(fill="both", expand=True)

        # Center card
        card = tk.Frame(main_container, bg=LOGIN_CARD_BG, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Create card with shadow effect
        card_inner = tk.Frame(card, bg=LOGIN_CARD_BG, padx=40, pady=40)
        card_inner.pack()

        # Logo and title
        logo_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        logo_frame.pack(pady=(0, 20))

        if self.images.get("logo"):
            logo_lbl = tk.Label(logo_frame, image=self.images["logo"], bg=LOGIN_CARD_BG)
            logo_lbl.pack(side="left", padx=(0, 10))

        title_label = tk.Label(
            logo_frame,
            text="NIMA HOSPITAL",
            font=("Segoe UI", 24, "bold"),
            bg=LOGIN_CARD_BG,
            fg=LOGIN_BG
        )
        title_label.pack(side="left")

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
        username_entry.insert(0, "admin")  # Demo value

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
        password_entry.insert(0, "password")  # Demo value

        # Remember me and forgot password
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
        forgot_label.bind("<Button-1>", lambda e: self.show_forgot_password_page())

        # Login button
        def login_click():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            # Check credentials
            if username in self.users and self.users[username]["password"] == password:
                messagebox.showinfo("Success", "Login successful!")
                self.show_main_app()
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
        register_link.bind("<Button-1>", lambda e: self.show_register_page())

    # ------------- REGISTER PAGE -------------
    def show_register_page(self):
        # Clear existing content
        for widget in self.winfo_children():
            widget.destroy()

        # Main container
        main_container = tk.Frame(self, bg=LOGIN_BG)
        main_container.pack(fill="both", expand=True)

        # Center card
        card = tk.Frame(main_container, bg=LOGIN_CARD_BG, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Create card with shadow effect
        card_inner = tk.Frame(card, bg=LOGIN_CARD_BG, padx=40, pady=40)
        card_inner.pack()

        # Logo and title
        logo_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        logo_frame.pack(pady=(0, 20))

        if self.images.get("logo"):
            logo_lbl = tk.Label(logo_frame, image=self.images["logo"], bg=LOGIN_CARD_BG)
            logo_lbl.pack(side="left", padx=(0, 10))

        title_label = tk.Label(
            logo_frame,
            text="NIMA HOSPITAL",
            font=("Segoe UI", 24, "bold"),
            bg=LOGIN_CARD_BG,
            fg=LOGIN_BG
        )
        title_label.pack(side="left")

        # Welcome text
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

        # Full Name field
        name_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        name_frame.pack(fill="x", pady=(0, 15))

        name_label = tk.Label(
            name_frame,
            text="Full Name",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MAIN,
            anchor="w"
        )
        name_label.pack(fill="x")

        name_entry = tk.Entry(
            name_frame,
            font=FONT_NORMAL,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=LOGIN_ACCENT,
            highlightbackground=BORDER
        )
        name_entry.pack(fill="x", ipady=8, pady=(5, 0))

        # Email field
        email_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        email_frame.pack(fill="x", pady=(0, 15))

        email_label = tk.Label(
            email_frame,
            text="Email",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MAIN,
            anchor="w"
        )
        email_label.pack(fill="x")

        email_entry = tk.Entry(
            email_frame,
            font=FONT_NORMAL,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=LOGIN_ACCENT,
            highlightbackground=BORDER
        )
        email_entry.pack(fill="x", ipady=8, pady=(5, 0))

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
        password_frame.pack(fill="x", pady=(0, 15))

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

        # Confirm Password field
        confirm_frame = tk.Frame(card_inner, bg=LOGIN_CARD_BG)
        confirm_frame.pack(fill="x", pady=(0, 20))

        confirm_label = tk.Label(
            confirm_frame,
            text="Confirm Password",
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MAIN,
            anchor="w"
        )
        confirm_label.pack(fill="x")

        confirm_entry = tk.Entry(
            confirm_frame,
            font=FONT_NORMAL,
            show="•",
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=LOGIN_ACCENT,
            highlightbackground=BORDER
        )
        confirm_entry.pack(fill="x", ipady=8, pady=(5, 0))

        # Terms and conditions
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

        # Register button
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
            
            if username in self.users:
                messagebox.showerror("Error", "Username already exists")
                return
            
            # Add new user to our "database"
            self.users[username] = {
                "password": password,
                "email": email,
                "name": name
            }
            
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

    # ------------- MAIN APP -------------
    def show_main_app(self):
        # Clear existing content
        for widget in self.winfo_children():
            widget.destroy()

        self.title("NIMA Hospital Dashboard")
        self.configure(bg=BG_MAIN)

        self.create_layout()
        self.show_dashboard()

    # ------------- LAYOUT -------------
    def create_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=BG_SIDEBAR, width=210, bd=1, relief="solid")
        self.sidebar.pack(side="left", fill="y")

        logo_frame = tk.Frame(self.sidebar, bg=BG_SIDEBAR)
        logo_frame.pack(pady=(15, 10), padx=18, anchor="w")

        if self.images.get("logo"):
            logo_lbl = tk.Label(logo_frame, image=self.images["logo"], bg=BG_SIDEBAR)
            logo_lbl.pack(side="left", padx=(0, 8))

        text_logo = tk.Label(
            logo_frame,
            text="NIMA\nHOSPITAL",
            font=("Segoe UI", 16, "bold"),
            bg=BG_SIDEBAR,
            fg="#111111",
            justify="left",
        )
        text_logo.pack(side="left")

        # menu
        self.menu_buttons = {}
        menu_items = [
            ("Dashboard", self.show_dashboard, "icon_dashboard"),
            ("Doctors", self.show_doctors, "icon_doctors"),
            ("Message", self.show_messages, "icon_message"),
            ("Schedule", self.show_schedule, "icon_schedule"),
            ("Setting", self.show_settings, "icon_settings"),
            ("Logout", self.logout, "icon_logout"),
        ]

        for text, cmd, icon_key in menu_items:
            frame = tk.Frame(self.sidebar, bg=BG_SIDEBAR)
            frame.pack(fill="x", padx=10, pady=2)

            img = self.images.get(icon_key)

            btn = tk.Button(
                frame,
                text="  " + text,
                font=("Segoe UI", 11, "bold"),
                relief="flat",
                bd=0,
                fg="#222222",
                bg=BG_SIDEBAR,
                activebackground="#dde2d4",
                activeforeground="#111111",
                anchor="w",
                compound="left",
                cursor="hand2",
                command=cmd,
                image=img if img else None
            )
            btn.pack(fill="x", ipady=6)
            self.menu_buttons[text] = btn

        # Right area
        self.right_area = tk.Frame(self, bg=BG_MAIN)
        self.right_area.pack(side="left", fill="both", expand=True)

        # Top bar
        self.topbar = tk.Frame(self.right_area, bg=BG_TOPBAR, height=60, bd=1, relief="solid")
        self.topbar.pack(side="top", fill="x")

        self.create_topbar()

        # Content
        self.content = tk.Frame(self.right_area, bg=BG_MAIN)
        self.content.pack(fill="both", expand=True)

    def create_topbar(self):
        # Title
        tk.Label(
            self.topbar,
            text="Dashboard",
            font=("Segoe UI", 14, "bold"),
            bg=BG_TOPBAR,
            fg=TEXT_MAIN,
        ).place(x=15, y=8)

        # search
        search_box = tk.Entry(self.topbar, font=FONT_NORMAL, relief="flat", bg="#f3f3f3")
        search_box.place(x=65, y=30, width=220, height=22)
        tk.Label(self.topbar, text="🔍", bg=BG_TOPBAR).place(x=45, y=30)

        # top buttons
        def upcoming():
            messagebox.showinfo("Upcoming", "Showing upcoming appointments (demo).")

        def support():
            messagebox.showinfo("Support", "Contact support@nima-hospital.com")

        btn_upcoming = tk.Button(
            self.topbar,
            text="Upcoming appointments",
            font=FONT_SMALL,
            relief="groove",
            bd=1,
            bg="#f7f7f7",
            activebackground="#e6e6e6",
            cursor="hand2",
            command=upcoming,
        )
        btn_upcoming.place(relx=0.52, y=16, width=160, height=28, anchor="n")

        btn_support = tk.Button(
            self.topbar,
            text="Support",
            font=FONT_SMALL,
            relief="groove",
            bd=1,
            bg="#f7f7f7",
            activebackground="#e6e6e6",
            cursor="hand2",
            command=support,
        )
        btn_support.place(relx=0.72, y=16, width=100, height=28, anchor="n")

        # ------- NOTIFICATION BUTTON (BELL) -------
        def open_notifications():
            # small popup window
            win = tk.Toplevel(self)
            win.title("Notifications")
            win.geometry("320x260")
            win.resizable(False, False)
            win.configure(bg=BG_CARD)

            tk.Label(
                win,
                text="Notifications",
                font=FONT_SUBTITLE,
                bg=BG_CARD,
                fg=TEXT_MAIN,
            ).pack(pady=(10, 5))

            frame_list = tk.Frame(win, bg=BG_CARD)
            frame_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

            listbox = tk.Listbox(
                frame_list,
                font=FONT_NORMAL,
                bg="#ffffff",
                height=8,
                bd=0,
                highlightthickness=1,
                highlightbackground=BORDER,
            )
            listbox.pack(fill="both", expand=True)

            if self.notifications:
                for n in self.notifications:
                    listbox.insert("end", "• " + n)
            else:
                listbox.insert("end", "No new notifications.")

            def clear_notifs():
                self.notifications.clear()
                listbox.delete(0, "end")
                listbox.insert("end", "No new notifications.")
                self.badge_label.config(text="0", bg="#cccccc")

            btn_clear = tk.Button(
                win,
                text="Clear all",
                font=FONT_SMALL,
                bg=ACCENT,
                fg="white",
                bd=0,
                relief="flat",
                cursor="hand2",
                command=clear_notifs,
            )
            btn_clear.pack(pady=(0, 10), ipadx=10, ipady=3)

        bell_frame = tk.Frame(self.topbar, bg=BG_TOPBAR)
        bell_frame.place(relx=0.83, rely=0.1)

        # THIS is the clickable bell
        bell_btn = tk.Button(
            bell_frame,
            text="🔔",
            font=("Segoe UI", 16),
            bg=BG_TOPBAR,
            bd=0,
            cursor="hand2",
            command=open_notifications,  # <--- important
        )
        bell_btn.pack(side="left")

        # badge
        self.badge_label = tk.Label(
            bell_frame,
            text=str(len(self.notifications)),
            bg=ACCENT if self.notifications else "#cccccc",
            fg="white",
            font=("Segoe UI", 8, "bold"),
            padx=4,
        )
        self.badge_label.place(x=20, y=0)

        # ------- Custom minimize & maximize -------
        def do_minimize():
            self.iconify()

        def do_maximize():
            if self.state() == "zoomed":
                self.state("normal")
            else:
                self.state("zoomed")

        btn_min = tk.Button(
            self.topbar,
            text="–",
            font=("Segoe UI", 10, "bold"),
            bg=BG_TOPBAR,
            bd=0,
            cursor="hand2",
            command=do_minimize,
        )
        btn_min.place(relx=0.93, rely=0.2, width=24, height=24)

        btn_max = tk.Button(
            self.topbar,
            text="□",
            font=("Segoe UI", 10, "bold"),
            bg=BG_TOPBAR,
            bd=0,
            cursor="hand2",
            command=do_maximize,
        )
        btn_max.place(relx=0.97, rely=0.2, width=24, height=24)

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ------------- PAGES -------------
    def show_dashboard(self):
        self.clear_content()

        stats_frame = tk.Frame(self.content, bg=BG_MAIN)
        stats_frame.pack(fill="x", pady=(15, 0), padx=25)

        def stat_card(parent, number, title, color):
            card = tk.Frame(
                parent,
                bg=BG_CARD,
                bd=0,
                highlightthickness=1,
                highlightbackground=BORDER,
            )
            card.pack(side="left", padx=10, ipadx=15, ipady=15)
            card.pack_propagate(False)
            card.config(width=210, height=90)

            badge = tk.Frame(card, bg=color, width=12, height=40)
            badge.pack(side="left", padx=(0, 8), fill="y")

            inner = tk.Frame(card, bg=BG_CARD)
            inner.pack(side="left", fill="both", expand=True)

            num_lbl = tk.Label(
                inner,
                text=str(number),
                font=("Segoe UI", 22, "bold"),
                bg=BG_CARD,
                fg="#111111",
            )
            num_lbl.pack(anchor="w")

            title_lbl = tk.Label(
                inner,
                text=title,
                font=FONT_NORMAL,
                bg=BG_CARD,
                fg=TEXT_MUTED,
            )
            title_lbl.pack(anchor="w")

        stat_card(stats_frame, 45, "New patients", "#ffafcc")
        stat_card(stats_frame, 17, "Doctors", "#9bf6ff")
        stat_card(stats_frame, 15, "Operations", "#caffbf")

        middle = tk.Frame(self.content, bg=BG_MAIN)
        middle.pack(fill="both", expand=True, padx=25, pady=20)

        # Patient journey
        pj = tk.Frame(
            middle,
            bg=BG_CARD,
            bd=0,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        pj.pack(side="left", fill="both", expand=True, padx=(0, 20))
        pj.pack_propagate(False)
        pj.config(height=260)

        tk.Label(
            pj,
            text="Patient Journey",
            font=FONT_SUBTITLE,
            bg=BG_CARD,
        ).pack(anchor="nw", padx=20, pady=15)

        journey_canvas = tk.Canvas(pj, bg=BG_CARD, highlightthickness=0)
        journey_canvas.pack(fill="both", expand=True, padx=40, pady=20)

        steps = ["Admitted", "Under\nObservation", "Recovered", "Discharged"]
        x = 40
        for i, step in enumerate(steps):
            journey_canvas.create_oval(
                x - 15,
                50 - 15,
                x + 15,
                50 + 15,
                fill=BG_SOFT_BLUE,
                outline="#4b8dd9",
                width=2,
            )
            journey_canvas.create_text(x, 90, text=step, font=FONT_SMALL)
            if i < len(steps) - 1:
                journey_canvas.create_line(
                    x + 15,
                    50,
                    x + 65 - 15,
                    50,
                    fill="#4b8dd9",
                    width=3,
                )
            x += 65

        # Best doctor
        bd = tk.Frame(
            middle,
            bg=BG_SOFT_BLUE,
            bd=0,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        bd.pack(side="left", fill="y", padx=(0, 0))
        bd.config(width=260)
        bd.pack_propagate(False)

        tk.Label(
            bd,
            text="Best Doctor of this Year",
            font=FONT_SUBTITLE,
            bg=BG_SOFT_BLUE,
        ).pack(anchor="nw", padx=15, pady=(15, 3))
        tk.Label(
            bd,
            text="Dr. Manish Thapa",
            font=("Segoe UI", 12, "bold"),
            bg=BG_SOFT_BLUE,
        ).pack(anchor="nw", padx=15)

        photo_frame = tk.Frame(bd, bg=BG_SOFT_BLUE)
        photo_frame.pack(pady=(10, 5), padx=10, anchor="center")

        if self.images.get("doctor_best"):
            lbl_photo = tk.Label(photo_frame, image=self.images["doctor_best"], bd=1, relief="ridge")
            lbl_photo.pack()
        else:
            photo_placeholder = tk.Frame(
                photo_frame,
                bg="#ffffff",
                width=120,
                height=130,
                bd=1,
                relief="ridge",
            )
            photo_placeholder.pack()
            tk.Label(photo_placeholder, text="Photo", bg="white", fg="#888").pack(expand=True)

        bottom = tk.Frame(bd, bg=BG_SOFT_BLUE)
        bottom.pack(side="bottom", fill="x", pady=12)

        def stat(label, value):
            f = tk.Frame(bottom, bg=BG_SOFT_BLUE)
            f.pack(side="left", expand=True, fill="x")
            tk.Label(
                f,
                text=label,
                font=FONT_SMALL,
                bg=BG_SOFT_BLUE,
                fg=TEXT_MUTED,
            ).pack()
            tk.Label(
                f,
                text=value,
                font=("Segoe UI", 10, "bold"),
                bg=BG_SOFT_BLUE,
            ).pack()

        stat("Experience", "10 years")
        stat("Patients", "2007")
        stat("Reviews", "6301")

    def show_doctors(self):
        self.clear_content()

        container = tk.Frame(self.content, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        def info_card(parent, title, text, color):
            card = tk.Frame(
                parent,
                bg=BG_CARD,
                bd=0,
                highlightbackground=BORDER,
                highlightthickness=1,
            )
            card.pack(side="left", fill="both", expand=True, padx=15)
            card.pack_propagate(False)
            card.config(width=300)
            header = tk.Frame(card, bg=color, height=6)
            header.pack(fill="x")
            tk.Label(
                card,
                text=title,
                font=FONT_SUBTITLE,
                bg=BG_CARD,
                fg="#111111",
                justify="left",
            ).pack(anchor="nw", padx=20, pady=(15, 10))
            lbl = tk.Label(
                card,
                text=text,
                font=FONT_NORMAL,
                bg=BG_CARD,
                fg=TEXT_MUTED,
                wraplength=300,
                justify="left",
            )
            lbl.pack(anchor="nw", padx=20, pady=(0, 20))

        text1 = (
            "Appointment reminders and updates notify patients and doctors "
            "about scheduled visits, cancellations, or reschedules. They "
            "improve communication, reduce missed appointments, enhance "
            "efficiency, and ensure better coordination between healthcare "
            "providers and patients."
        )
        text2 = (
            "Lab test results notifications inform patients and doctors when "
            "reports are ready. They ensure timely access, improve "
            "communication, support faster diagnosis, enhance treatment "
            "decisions, and strengthen overall hospital management efficiency."
        )

        info_card(container, "Appointment reminders/updates", text1, "#ffd6a5")
        info_card(container, "Lab test results available", text2, "#bdb2ff")

    def show_messages(self):
        self.clear_content()

        frame = tk.Frame(self.content, bg=BG_MAIN)
        frame.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(frame, text="Messages", font=FONT_TITLE, bg=BG_MAIN).pack(
            anchor="w", pady=(0, 10)
        )

        msg_list = tk.Listbox(
            frame,
            font=FONT_NORMAL,
            height=10,
            bg="#ffffff",
            activestyle="none",
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        msg_list.pack(fill="x")

        sample_msgs = [
            "Patient #1003: Requesting appointment reschedule.",
            "Lab: Blood report ready for Mr. Koirala.",
            "Admin: Staff meeting at 3:00 PM in Conference Room.",
        ]
        for m in sample_msgs:
            msg_list.insert("end", m)

        entry = tk.Entry(frame, font=FONT_NORMAL)
        entry.pack(fill="x", pady=(15, 5))

        def send():
            text = entry.get().strip()
            if text:
                msg_list.insert("end", "You: " + text)
                entry.delete(0, "end")

        btn = tk.Button(
            frame,
            text="Send",
            font=FONT_NORMAL,
            bg=BG_PRIMARY,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=send,
        )
        btn.pack(anchor="e", pady=(0, 10), ipadx=12, ipady=4)

    def show_schedule(self):
        self.clear_content()

        container = tk.Frame(self.content, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=35, pady=30)

        card = tk.Frame(
            container,
            bg=BG_CARD,
            bd=0,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        card.pack(fill="both", expand=True)
        card.pack_propagate(False)

        tk.Label(
            card,
            text="Doctor Schedule",
            font=FONT_SUBTITLE,
            bg=BG_CARD,
        ).pack(anchor="w", padx=15, pady=(8, 0))

        columns = ("Time", "Doctor Name", "Duty / Notes")
        tree = ttk.Treeview(
            card,
            columns=columns,
            show="headings",
            height=6,
        )
        tree.pack(fill="both", expand=True, padx=10, pady=(10, 10))

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=FONT_NORMAL, rowheight=28)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        data = [
            ("8:00-10:00", "Dr. Sharma", "Outpatient consultants"),
            ("10:00-12:00", "Dr. Koirala", "Routine checks, IP rounds"),
            ("12:00-2:00", "Dr. Singh", "Surgery / OT duty"),
            ("2:00-5:00", "Dr. Thapa", "Follow-up appointments"),
        ]

        for row in data:
            tree.insert("", "end", values=row)

    def show_settings(self):
        self.clear_content()

        container = tk.Frame(self.content, bg=BG_MAIN)
        container.pack(fill="both", expand=True)

        card = tk.Frame(
            container,
            bg=BG_CARD,
            bd=0,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=320)

        tk.Label(
            card,
            text="Update Password",
            font=FONT_SUBTITLE,
            bg=BG_CARD,
        ).pack(pady=(15, 10))

        form = tk.Frame(card, bg=BG_CARD)
        form.pack(fill="both", expand=True, padx=35, pady=(0, 10))

        def add_row(label_text):
            row = tk.Frame(form, bg=BG_CARD)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=label_text, font=FONT_NORMAL, bg=BG_CARD).pack(
                anchor="w"
            )
            entry = tk.Entry(
                row,
                font=FONT_NORMAL,
                show="*",
                relief="solid",
                bd=1,
            )
            entry.pack(fill="x", pady=(2, 0), ipady=4)
            return entry

        current = add_row("Current Password")
        new = add_row("New Password")
        confirm = add_row("Confirm Password")

        def save_changes():
            if new.get() != confirm.get():
                messagebox.showerror("Error", "New password and confirm do not match.")
                return
            if not new.get():
                messagebox.showwarning("Warning", "New password cannot be empty.")
                return
            messagebox.showinfo("Success", "Password updated successfully (demo).")
            current.delete(0, "end")
            new.delete(0, "end")
            confirm.delete(0, "end")

        btn = tk.Button(
            card,
            text="Save Changes",
            font=("Segoe UI", 11, "bold"),
            bg=BG_PRIMARY,
            fg="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=save_changes,
        )
        btn.pack(pady=(0, 20), ipadx=20, ipady=6)

    def logout(self):
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.show_login_page()


if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()