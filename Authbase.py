# 02_auth_base.py
"""
PART 2/5 - Authentication Base Classes and Helper Functions
Run Order: Second
"""
import tkinter as tk
import sqlite3
from config import LOGIN_BG, LOGIN_CARD_BG, LOGIN_ACCENT, BORDER, TEXT_MAIN, TEXT_MUTED, FONT_NORMAL

class Authbase:
    def __init__(self, app):
        self.app = app

    def clear_window(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    def create_logo_header(self, parent):
        logo_frame = tk.Frame(parent, bg=LOGIN_CARD_BG)
        logo_frame.pack(pady=(0, 20))

        if self.app.images.get("logo"):
            logo_lbl = tk.Label(logo_frame, image=self.app.images["logo"], bg=LOGIN_CARD_BG)
            logo_lbl.pack(side="left", padx=(0, 10))

        title_label = tk.Label(
            logo_frame,
            text="NIMA HOSPITAL",
            font=("Segoe UI", 24, "bold"),
            bg=LOGIN_CARD_BG,
            fg=LOGIN_BG
        )
        title_label.pack(side="left")
        return logo_frame

    def create_entry_field(self, parent, label_text, show=None):
        frame = tk.Frame(parent, bg=LOGIN_CARD_BG)
        frame.pack(fill="x", pady=(0, 15))

        label = tk.Label(
            frame,
            text=label_text,
            font=FONT_NORMAL,
            bg=LOGIN_CARD_BG,
            fg=TEXT_MAIN,
            anchor="w"
        )
        label.pack(fill="x")

        entry = tk.Entry(
            frame,
            font=FONT_NORMAL,
            show=show,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=LOGIN_ACCENT,
            highlightbackground=BORDER
        )
        entry.pack(fill="x", ipady=8, pady=(5, 0))
        return entry

    def create_card(self, container):
        card = tk.Frame(container, bg=LOGIN_CARD_BG, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card_inner = tk.Frame(card, bg=LOGIN_CARD_BG, padx=40, pady=40)
        card_inner.pack()
        return card_inner


if __name__ == "__main__":
    print("Authbase.py is a support module. Run main_app.py for the full application.")
