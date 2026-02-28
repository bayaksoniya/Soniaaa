# 01_config.py
"""
PART 1/5 - Configuration, Constants, and Imports
Run Order: First
"""
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import random
import sqlite3
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
LOGIN_BG = "#1a2b3c"
LOGIN_CARD_BG = "#ffffff"
LOGIN_ACCENT = "#2ecc71"
LOGIN_BUTTON = "#3498db"
LOGIN_BUTTON_HOVER = "#2980b9"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUBTITLE = ("Segoe UI", 13, "bold")
FONT_NORMAL = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)
