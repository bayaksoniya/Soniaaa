# 04_password_reset.py
"""
PART 4/5 - Password Reset Pages (Forgot Password, Reset Code, New Password)
Run Order: Fourth
"""
from config import tk, messagebox, random, string, LOGIN_BG, LOGIN_CARD_BG, LOGIN_ACCENT, LOGIN_BUTTON, LOGIN_BG, BORDER, TEXT_MAIN, TEXT_MUTED, FONT_NORMAL, FONT_SMALL
from Authbase import Authbase

class PasswordResetPages(Authbase):
    def __init__(self, app):
        super().__init__(app)

    # ------------- FORGOT PASSWORD PAGE -------------
    def show_forgot_password_page(self):
        self.clear_window()

        main_container = tk.Frame(self.app, bg=LOGIN_BG)
        main_container.pack(fill="both", expand=True)

        card_inner = self.create_card(main_container)
        self.create_logo_header(card_inner)

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

        def send_reset():
            email = email_entry.get().strip()
            
            if not email:
                messagebox.showerror("Error", "Please enter your email address")
                return

            username = self.app.find_user_by_email(email)

            if username:
                reset_code = ''.join(random.choices(string.digits, k=6))
                self.app.reset_codes[email] = reset_code
                
                messagebox.showinfo(
                    "Reset Code", 
                    f"DEMO MODE - Reset code: {reset_code}\n\nIn a real application, this would be sent to your email."
                )
                
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

        # Back to login
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
        back_link.bind("<Button-1>", lambda e: self.app.show_login_page())

    # ------------- RESET CODE PAGE -------------
    def show_reset_code_page(self, email, username):
        self.clear_window()

        main_container = tk.Frame(self.app, bg=LOGIN_BG)
        main_container.pack(fill="both", expand=True)

        card_inner = self.create_card(main_container)
        self.create_logo_header(card_inner)

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

        def verify_code():
            entered_code = code_entry.get().strip()
            stored_code = self.app.reset_codes.get(email)
            
            if not entered_code:
                messagebox.showerror("Error", "Please enter the reset code")
                return
            
            if stored_code and entered_code == stored_code:
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

        # Resend code
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
            new_code = ''.join(random.choices(string.digits, k=6))
            self.app.reset_codes[email] = new_code
            messagebox.showinfo("Code Resent", f"DEMO MODE - New code: {new_code}")
        
        resend_link.bind("<Button-1>", lambda e: resend_code())

        back_link = tk.Label(
            card_inner,
            text="← Back to Login",
            font=FONT_SMALL,
            bg=LOGIN_CARD_BG,
            fg=LOGIN_ACCENT,
            cursor="hand2"
        )
        back_link.pack()
        back_link.bind("<Button-1>", lambda e: self.app.show_login_page())

    # ------------- NEW PASSWORD PAGE -------------
    def show_new_password_page(self, email, username):
        self.clear_window()

        main_container = tk.Frame(self.app, bg=LOGIN_BG)
        main_container.pack(fill="both", expand=True)

        card_inner = self.create_card(main_container)
        self.create_logo_header(card_inner)

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

            if not self.app.update_user_password(username, newpass):
                messagebox.showerror("Error", "Unable to update password for this user")
                return
            
            if email in self.app.reset_codes:
                del self.app.reset_codes[email]
            
            messagebox.showinfo("Success", "Password reset successful! Please login with your new password.")
            self.app.show_login_page()

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

        back_link = tk.Label(
            card_inner,
            text="← Back to Login",
            font=FONT_SMALL,
            bg=LOGIN_CARD_BG,
            fg=LOGIN_ACCENT,
            cursor="hand2"
        )
        back_link.pack()
        back_link.bind("<Button-1>", lambda e: self.app.show_login_page())
if __name__ == "__main__":
    from main_app import HospitalApp

    app = HospitalApp()
    app.show_forgot_password_page()
    app.mainloop()
