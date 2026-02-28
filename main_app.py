
"""
PART 5/5 - Main Application Class and Dashboard Pages
Run Order: Fifth (Last)
"""
import sqlite3
from config import tk, messagebox, ttk, Image, ImageTk, os, BG_MAIN, BG_SIDEBAR, BG_TOPBAR, BG_CARD, BG_PRIMARY, BG_SOFT_BLUE, BORDER, TEXT_MAIN, TEXT_MUTED, ACCENT, LOGIN_BG, LOGIN_BUTTON, FONT_TITLE, FONT_SUBTITLE, FONT_NORMAL, FONT_SMALL
from login_register import LoginRegisterPages
from password_reset import PasswordResetPages

class HospitalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NIMA Hospital - Login")
        self.geometry("1080x650")
        self.configure(bg=LOGIN_BG)
        self.resizable(True, True)

        self.db_path = os.path.join(os.path.dirname(__file__), "hospital.db")
        self.init_database()
        
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

        # Initialize page handlers
        self.login_register = LoginRegisterPages(self)
        self.password_reset = PasswordResetPages(self)

        # Start with login page
        self.show_login_page()

    # ------------- DATABASE -------------
    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def init_database(self):
        with self.get_db_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    full_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            cursor = conn.execute("SELECT 1 FROM users WHERE username = ?", ("admin",))
            if cursor.fetchone() is None:
                conn.execute(
                    """
                    INSERT INTO users (username, password, email, full_name)
                    VALUES (?, ?, ?, ?)
                    """,
                    ("admin", "password", "admin@nima-hospital.com", "Administrator"),
                )
            conn.commit()

    def validate_login(self, username, password):
        with self.get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM users WHERE username = ? AND password = ?",
                (username, password),
            )
            return cursor.fetchone() is not None

    def username_exists(self, username):
        with self.get_db_connection() as conn:
            cursor = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            return cursor.fetchone() is not None

    def create_user(self, full_name, email, username, password):
        try:
            with self.get_db_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO users (full_name, email, username, password)
                    VALUES (?, ?, ?, ?)
                    """,
                    (full_name, email, username, password),
                )
                conn.commit()
            return True, None
        except sqlite3.IntegrityError:
            return False, "Username or email already exists"

    def find_user_by_email(self, email):
        with self.get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT username FROM users WHERE email = ?",
                (email,),
            )
            row = cursor.fetchone()
            if row:
                return row[0]
            return None

    def update_user_password(self, username, new_password):
        with self.get_db_connection() as conn:
            cursor = conn.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (new_password, username),
            )
            conn.commit()
            return cursor.rowcount > 0

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

    # ------------- PAGE NAVIGATION -------------
    def show_login_page(self):
        self.login_register.show_login_page()

    def show_register_page(self):
        self.login_register.show_register_page()

    def show_forgot_password_page(self):
        self.password_reset.show_forgot_password_page()

    def show_reset_code_page(self, email, username):
        self.password_reset.show_reset_code_page(email, username)

    def show_new_password_page(self, email, username):
        self.password_reset.show_new_password_page(email, username)

    # ------------- MAIN APP -------------
    def show_main_app(self):
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
        tk.Label(
            self.topbar,
            text="Dashboard",
            font=("Segoe UI", 14, "bold"),
            bg=BG_TOPBAR,
            fg=TEXT_MAIN,
        ).place(x=15, y=8)

        search_box = tk.Entry(self.topbar, font=FONT_NORMAL, relief="flat", bg="#f3f3f3")
        search_box.place(x=65, y=30, width=220, height=22)
        tk.Label(self.topbar, text="🔍", bg=BG_TOPBAR).place(x=45, y=30)

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

        # Notification button
        def open_notifications():
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

        bell_btn = tk.Button(
            bell_frame,
            text="🔔",
            font=("Segoe UI", 16),
            bg=BG_TOPBAR,
            bd=0,
            cursor="hand2",
            command=open_notifications,
        )
        bell_btn.pack(side="left")

        self.badge_label = tk.Label(
            bell_frame,
            text=str(len(self.notifications)),
            bg=ACCENT if self.notifications else "#cccccc",
            fg="white",
            font=("Segoe UI", 8, "bold"),
            padx=4,
        )
        self.badge_label.place(x=20, y=0)

        # Minimize & maximize
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

    # ------------- DASHBOARD PAGE -------------
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
            self.title("NIMA Hospital - Login")
            self.configure(bg=LOGIN_BG)
            self.show_login_page()


if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()
