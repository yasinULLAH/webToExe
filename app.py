import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


APP_TITLE = "KioskForge Pro - Enterprise Client Web App & Portable EXE Builder"
APP_VERSION = "2.4.0"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "kiosk_clients_db.json")


PRESETS = {
    "POS & Thermal Receipt Terminal": {
        "launch_mode": "kiosk",
        "kiosk_printing": True,
        "isolated_profile": True,
        "incognito": False,
        "disable_pinch": True,
        "disable_swipe_nav": True,
        "no_first_run": True,
        "suppress_dialogs": True,
        "autoplay_media": True,
        "disable_translate": True,
        "start_maximized": False,
        "start_fullscreen": False,
        "disable_extensions": True,
        "ignore_cert_errors": False,
        "clear_cache_on_launch": False,
        "clear_session_on_exit": False,
        "scale_factor": "1.0",
        "extra_flags": "--disable-print-preview --disable-features=PrintCompositorLPAC"
    },
    "Standalone Desktop Web App (--app)": {
        "launch_mode": "app",
        "kiosk_printing": False,
        "isolated_profile": True,
        "incognito": False,
        "disable_pinch": False,
        "disable_swipe_nav": True,
        "no_first_run": True,
        "suppress_dialogs": True,
        "autoplay_media": True,
        "disable_translate": True,
        "start_maximized": True,
        "start_fullscreen": False,
        "disable_extensions": False,
        "ignore_cert_errors": False,
        "clear_cache_on_launch": False,
        "clear_session_on_exit": False,
        "scale_factor": "1.0",
        "extra_flags": ""
    },
    "Locked Public Self-Service Kiosk": {
        "launch_mode": "kiosk",
        "kiosk_printing": False,
        "isolated_profile": True,
        "incognito": True,
        "disable_pinch": True,
        "disable_swipe_nav": True,
        "no_first_run": True,
        "suppress_dialogs": True,
        "autoplay_media": False,
        "disable_translate": True,
        "start_maximized": False,
        "start_fullscreen": False,
        "disable_extensions": True,
        "ignore_cert_errors": False,
        "clear_cache_on_launch": True,
        "clear_session_on_exit": True,
        "scale_factor": "1.0",
        "extra_flags": "--disable-background-networking --disable-sync"
    },
    "Hospital / School Queue Display Screen": {
        "launch_mode": "kiosk",
        "kiosk_printing": False,
        "isolated_profile": True,
        "incognito": False,
        "disable_pinch": True,
        "disable_swipe_nav": True,
        "no_first_run": True,
        "suppress_dialogs": True,
        "autoplay_media": True,
        "disable_translate": True,
        "start_maximized": False,
        "start_fullscreen": False,
        "disable_extensions": True,
        "ignore_cert_errors": False,
        "clear_cache_on_launch": False,
        "clear_session_on_exit": False,
        "scale_factor": "1.1",
        "extra_flags": "--disable-gpu-vsync"
    },
    "Local Intranet / Self-Signed HTTPS App": {
        "launch_mode": "app",
        "kiosk_printing": True,
        "isolated_profile": True,
        "incognito": False,
        "disable_pinch": False,
        "disable_swipe_nav": True,
        "no_first_run": True,
        "suppress_dialogs": True,
        "autoplay_media": True,
        "disable_translate": True,
        "start_maximized": True,
        "start_fullscreen": False,
        "disable_extensions": True,
        "ignore_cert_errors": True,
        "clear_cache_on_launch": False,
        "clear_session_on_exit": False,
        "scale_factor": "1.0",
        "extra_flags": "--allow-insecure-localhost"
    }
}


class ToolTip:
    def __init__(self, widget, text, delay=350):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window = None
        self.after_id = None
        self.widget.bind("<Enter>", self.schedule_show, add="+")
        self.widget.bind("<Leave>", self.hide, add="+")
        self.widget.bind("<ButtonPress>", self.hide, add="+")

    def schedule_show(self, event=None):
        self.cancel_schedule()
        self.after_id = self.widget.after(self.delay, self.show)

    def cancel_schedule(self):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

    def show(self):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 18
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_attributes("-topmost", True)
        tw.wm_geometry(f"+{x}+{y}")

        outer = tk.Frame(tw, bg="#cbd5e1", bd=1)
        outer.pack()
        inner = tk.Frame(outer, bg="#0f172a", padx=10, pady=6)
        inner.pack()
        lbl = tk.Label(
            inner,
            text=self.text,
            justify="left",
            bg="#0f172a",
            fg="#f8fafc",
            font=("Segoe UI", 8),
            wraplength=340
        )
        lbl.pack()

    def hide(self, event=None):
        self.cancel_schedule()
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class KioskForgeApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_TITLE} v{APP_VERSION}")
        self.root.configure(bg="#f1f5f9")
        self.is_fullscreen = False
        self.is_building = False
        self.icon_preview_img = None
        self.clients_data = self.load_clients_data()

        self.maximize_window()
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        self.setup_styles()
        self.init_variables()
        self.build_ui()
        self.bind_live_preview()
        self.update_all_previews()
        self.refresh_dependency_status()
        self.audit_installed_browsers()

    def maximize_window(self):
        self.root.update_idletasks()
        try:
            self.root.state("zoomed")
        except Exception:
            w = self.root.winfo_screenwidth()
            h = self.root.winfo_screenheight()
            self.root.geometry(f"{w}x{h}+0+0")

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        if not self.is_fullscreen:
            self.maximize_window()
        if hasattr(self, "btn_fullscreen"):
            self.btn_fullscreen.configure(text="Exit Fullscreen (F11)" if self.is_fullscreen else "Fullscreen (F11)")

    def exit_fullscreen(self, event=None):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes("-fullscreen", False)
            self.maximize_window()
            if hasattr(self, "btn_fullscreen"):
                self.btn_fullscreen.configure(text="Fullscreen (F11)")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        bg_canvas = "#f1f5f9"
        bg_card = "#ffffff"
        bg_subtle = "#f8fafc"
        border_col = "#cbd5e1"
        fg_primary = "#0f172a"
        fg_secondary = "#475569"
        accent_blue = "#2563eb"
        accent_blue_hover = "#1d4ed8"

        style.configure(".", background=bg_canvas, foreground=fg_primary, font=("Segoe UI", 9))
        style.configure("Canvas.TFrame", background=bg_canvas)
        style.configure("TopBar.TFrame", background="#ffffff")
        style.configure("Card.TFrame", background=bg_card)
        style.configure("Subtle.TFrame", background=bg_subtle)

        style.configure("BrandTitle.TLabel", background="#ffffff", foreground="#0f172a", font=("Segoe UI", 13, "bold"))
        style.configure("BrandSub.TLabel", background="#ffffff", foreground="#64748b", font=("Segoe UI", 8))
        style.configure("SectionTitle.TLabel", background=bg_card, foreground="#1e40af", font=("Segoe UI", 10, "bold"))
        style.configure("Card.TLabel", background=bg_card, foreground=fg_primary, font=("Segoe UI", 9))
        style.configure("Muted.TLabel", background=bg_card, foreground=fg_secondary, font=("Segoe UI", 8))
        style.configure("BadgeOk.TLabel", background="#dcfce7", foreground="#166534", font=("Segoe UI", 8, "bold"), padding=(8, 3))
        style.configure("BadgeWarn.TLabel", background="#fef3c7", foreground="#92400e", font=("Segoe UI", 8, "bold"), padding=(8, 3))

        style.configure("TEntry", fieldbackground="#ffffff", foreground=fg_primary, insertcolor=fg_primary, bordercolor=border_col, lightcolor=border_col, darkcolor=border_col, padding=5)
        style.map("TEntry", bordercolor=[("focus", accent_blue)])

        style.configure("TSpinbox", fieldbackground="#ffffff", foreground=fg_primary, bordercolor=border_col, padding=4)

        style.configure("TCombobox", fieldbackground="#ffffff", background="#e2e8f0", foreground=fg_primary, arrowcolor=fg_primary, bordercolor=border_col, padding=4)
        style.map("TCombobox", fieldbackground=[("readonly", "#ffffff")], selectbackground=[("readonly", "#eff6ff")], selectforeground=[("readonly", fg_primary)])

        style.configure("Card.TCheckbutton", background=bg_card, foreground=fg_primary, font=("Segoe UI", 9))
        style.map("Card.TCheckbutton", background=[("active", "#f8fafc")], foreground=[("active", accent_blue)])

        style.configure("Card.TRadiobutton", background=bg_card, foreground=fg_primary, font=("Segoe UI", 9))
        style.map("Card.TRadiobutton", background=[("active", "#f8fafc")], foreground=[("active", accent_blue)])

        style.configure("Primary.TButton", background=accent_blue, foreground="#ffffff", font=("Segoe UI", 9, "bold"), padding=(12, 6), borderwidth=0)
        style.map("Primary.TButton", background=[("active", accent_blue_hover), ("disabled", "#94a3b8")])

        style.configure("Success.TButton", background="#059669", foreground="#ffffff", font=("Segoe UI", 10, "bold"), padding=(16, 8), borderwidth=0)
        style.map("Success.TButton", background=[("active", "#047857"), ("disabled", "#94a3b8")])

        style.configure("Secondary.TButton", background="#e2e8f0", foreground="#0f172a", font=("Segoe UI", 9), padding=(10, 6), borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#cbd5e1")])

        style.configure("Danger.TButton", background="#fee2e2", foreground="#b91c1c", font=("Segoe UI", 9, "bold"), padding=(10, 6), borderwidth=0)
        style.map("Danger.TButton", background=[("active", "#fecaca")])

        style.configure("TNotebook", background=bg_canvas, borderwidth=0)
        style.configure("TNotebook.Tab", background="#e2e8f0", foreground="#334155", font=("Segoe UI", 9, "bold"), padding=(14, 7))
        style.map("TNotebook.Tab", background=[("selected", "#ffffff")], foreground=[("selected", accent_blue)])

    def init_variables(self):
        self.var_client_name = tk.StringVar(value="Al-Falah Medical Center")
        self.var_app_name = tk.StringVar(value="Hospital Management Portal")
        self.var_url = tk.StringVar(value="https://example.com")
        self.var_output_name = tk.StringVar(value="Hospital_Management_Portal_Launcher")
        self.var_output_dir = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Desktop", "Client_Kiosk_Deliverables"))
        self.var_icon_path = tk.StringVar(value="")
        self.var_preset = tk.StringVar(value="POS & Thermal Receipt Terminal")
        self.var_browser_target = tk.StringVar(value="Auto (Chrome -> Edge -> Brave)")

        self.var_launch_mode = tk.StringVar(value="kiosk")
        self.var_kiosk_printing = tk.BooleanVar(value=True)
        self.var_isolated_profile = tk.BooleanVar(value=True)
        self.var_profile_folder = tk.StringVar(value="Hospital_Management_Portal_Profile")
        self.var_incognito = tk.BooleanVar(value=False)
        self.var_disable_pinch = tk.BooleanVar(value=True)
        self.var_disable_swipe_nav = tk.BooleanVar(value=True)
        self.var_no_first_run = tk.BooleanVar(value=True)
        self.var_suppress_dialogs = tk.BooleanVar(value=True)
        self.var_autoplay_media = tk.BooleanVar(value=True)
        self.var_disable_translate = tk.BooleanVar(value=True)
        self.var_start_maximized = tk.BooleanVar(value=False)
        self.var_start_fullscreen = tk.BooleanVar(value=False)
        self.var_disable_extensions = tk.BooleanVar(value=True)
        self.var_custom_geometry = tk.BooleanVar(value=False)
        self.var_win_width = tk.StringVar(value="1366")
        self.var_win_height = tk.StringVar(value="768")
        self.var_win_x = tk.StringVar(value="0")
        self.var_win_y = tk.StringVar(value="0")
        self.var_scale_factor = tk.StringVar(value="1.0")
        self.var_extra_flags = tk.StringVar(value="--disable-print-preview")

        self.var_health_check = tk.BooleanVar(value=True)
        self.var_health_retries = tk.StringVar(value="3")
        self.var_offline_fallback = tk.BooleanVar(value=True)
        self.var_support_phone = tk.StringVar(value="+92-336-1593533")
        self.var_ignore_cert_errors = tk.BooleanVar(value=False)
        self.var_clear_cache_on_launch = tk.BooleanVar(value=False)
        self.var_clear_session_on_exit = tk.BooleanVar(value=False)
        self.var_proxy_server = tk.StringVar(value="")
        self.var_user_agent = tk.StringVar(value="")

        self.var_exe_company = tk.StringVar(value="Bannu Software Solutions (SSTS)")
        self.var_exe_product = tk.StringVar(value="Hospital Management Portal Kiosk")
        self.var_exe_desc = tk.StringVar(value="Dedicated Desktop Kiosk Client Launcher")
        self.var_exe_version = tk.StringVar(value="1.0.0.0")
        self.var_exe_copyright = tk.StringVar(value="Copyright (c) 2026 Bannu Software Solutions")
        self.var_uac_admin = tk.BooleanVar(value=False)

        self.var_gen_exe = tk.BooleanVar(value=True)
        self.var_gen_bat = tk.BooleanVar(value=True)
        self.var_gen_cmd = tk.BooleanVar(value=False)
        self.var_gen_vbs = tk.BooleanVar(value=True)
        self.var_gen_shortcut_helper = tk.BooleanVar(value=True)
        self.var_add_startup_helper = tk.BooleanVar(value=True)
        self.var_add_kill_helper = tk.BooleanVar(value=True)
        self.var_gen_zip = tk.BooleanVar(value=True)
        self.var_kill_existing = tk.BooleanVar(value=True)

        self.var_saved_profile = tk.StringVar(value="")
        self.var_preview_type = tk.StringVar(value="CLI Command")

    def create_card(self, parent):
        wrapper = tk.Frame(parent, bg="#cbd5e1", bd=0)
        card = ttk.Frame(wrapper, style="Card.TFrame")
        card.pack(fill="both", expand=True, padx=1, pady=1)
        return wrapper, card

    def build_ui(self):
        top_border = tk.Frame(self.root, bg="#cbd5e1")
        top_border.pack(fill="x")
        top_bar = ttk.Frame(top_border, style="TopBar.TFrame")
        top_bar.pack(fill="x", pady=(0, 1))

        brand_left = ttk.Frame(top_bar, style="TopBar.TFrame")
        brand_left.pack(side="left", padx=18, pady=10)
        ttk.Label(brand_left, text="KioskForge Pro", style="BrandTitle.TLabel").pack(anchor="w")
        ttk.Label(brand_left, text="Enterprise Client Web App Launcher, Kiosk Configurator & Portable EXE Compiler", style="BrandSub.TLabel").pack(anchor="w")

        top_right = ttk.Frame(top_bar, style="TopBar.TFrame")
        top_right.pack(side="right", padx=18, pady=10)

        self.lbl_dep_status = ttk.Label(top_right, text="Checking Tools...", style="BadgeWarn.TLabel")
        self.lbl_dep_status.pack(side="left", padx=(0, 8))
        ToolTip(self.lbl_dep_status, "Displays installation status of PyInstaller (required for .exe compilation) and Pillow (required for PNG/JPG to .ico icon conversion).")

        self.btn_install_deps = ttk.Button(top_right, text="Install Build Tools", style="Secondary.TButton", command=self.install_dependencies)
        self.btn_install_deps.pack(side="left", padx=(0, 8))
        ToolTip(self.btn_install_deps, "Automatically installs or upgrades PyInstaller and Pillow in your active Python environment via pip.")

        self.btn_fullscreen = ttk.Button(top_right, text="Fullscreen (F11)", style="Secondary.TButton", command=self.toggle_fullscreen)
        self.btn_fullscreen.pack(side="left")
        ToolTip(self.btn_fullscreen, "Toggle distraction-free borderless fullscreen mode (Shortcut: F11, Esc to exit).")

        toolbar_wrap, toolbar = self.create_card(self.root)
        toolbar_wrap.pack(fill="x", padx=16, pady=(10, 8))
        tb_inner = ttk.Frame(toolbar, style="Card.TFrame")
        tb_inner.pack(fill="x", padx=14, pady=8)

        ttk.Label(tb_inner, text="Client Profile:", style="SectionTitle.TLabel").pack(side="left", padx=(0, 8))
        self.cmb_saved = ttk.Combobox(tb_inner, textvariable=self.var_saved_profile, state="readonly", width=34)
        self.cmb_saved.pack(side="left", padx=(0, 6))
        ToolTip(self.cmb_saved, "Select a previously saved client configuration to load, update, or include in batch builds.")
        self.refresh_saved_profiles_dropdown()

        btn_load = ttk.Button(tb_inner, text="Load", style="Secondary.TButton", command=self.load_selected_profile)
        btn_load.pack(side="left", padx=2)
        ToolTip(btn_load, "Load the selected client profile settings into the editor.")

        btn_save = ttk.Button(tb_inner, text="Save Profile", style="Primary.TButton", command=self.save_current_profile)
        btn_save.pack(side="left", padx=2)
        ToolTip(btn_save, "Save or update the current configuration in your local client database (kiosk_clients_db.json).")

        btn_del = ttk.Button(tb_inner, text="Delete", style="Danger.TButton", command=self.delete_selected_profile)
        btn_del.pack(side="left", padx=2)
        ToolTip(btn_del, "Permanently delete the currently selected client profile from your database.")

        btn_import = ttk.Button(tb_inner, text="Import JSON", style="Secondary.TButton", command=self.import_profiles_json)
        btn_import.pack(side="left", padx=(10, 2))
        ToolTip(btn_import, "Import client profiles from an external JSON backup file.")

        btn_export = ttk.Button(tb_inner, text="Export JSON", style="Secondary.TButton", command=self.export_profiles_json)
        btn_export.pack(side="left", padx=2)
        ToolTip(btn_export, "Export all saved client profiles to a JSON file for backup or migration.")

        ttk.Label(tb_inner, text="Deployment Preset:", style="SectionTitle.TLabel").pack(side="left", padx=(20, 8))
        cmb_preset = ttk.Combobox(tb_inner, textvariable=self.var_preset, values=list(PRESETS.keys()), state="readonly", width=32)
        cmb_preset.pack(side="left")
        cmb_preset.bind("<<ComboboxSelected>>", self.apply_selected_preset)
        ToolTip(cmb_preset, "Quickly configure optimal Chromium kiosk flags for common client scenarios (POS thermal receipt printing, standalone desktop web app, public kiosk, etc.).")

        workspace = ttk.Frame(self.root, style="Canvas.TFrame")
        workspace.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        workspace.columnconfigure(0, weight=5)
        workspace.columnconfigure(1, weight=6)
        workspace.rowconfigure(0, weight=1)

        left_host = ttk.Frame(workspace, style="Canvas.TFrame")
        left_host.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        canvas = tk.Canvas(left_host, bg="#f1f5f9", highlightthickness=0)
        v_scroll = ttk.Scrollbar(left_host, orient="vertical", command=canvas.yview)
        self.left_scroll_frame = ttk.Frame(canvas, style="Canvas.TFrame")

        self.left_scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        win_id = canvas.create_window((0, 0), window=self.left_scroll_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
        canvas.configure(yscrollcommand=v_scroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")

        def _on_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_wheel)

        self.build_left_inspector(self.left_scroll_frame)

        right_host = ttk.Frame(workspace, style="Canvas.TFrame")
        right_host.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        self.build_right_workspace(right_host)

    def build_left_inspector(self, parent):
        w1, c1_box = self.create_card(parent)
        w1.pack(fill="x", pady=(0, 10))
        c1 = ttk.Frame(c1_box, style="Card.TFrame")
        c1.pack(fill="x", padx=14, pady=12)
        c1.columnconfigure(1, weight=1)

        ttk.Label(c1, text="1. Client Identity & Target Web Application", style="SectionTitle.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

        ttk.Label(c1, text="Client / Organization:", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=4, padx=(0, 10))
        e_client = ttk.Entry(c1, textvariable=self.var_client_name)
        e_client.grid(row=1, column=1, columnspan=2, sticky="ew", pady=4)
        ToolTip(e_client, "Name of the client business, hospital, school, or organization receiving this launcher.")

        ttk.Label(c1, text="Web App Title:", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 10))
        e_app = ttk.Entry(c1, textvariable=self.var_app_name)
        e_app.grid(row=2, column=1, columnspan=2, sticky="ew", pady=4)
        e_app.bind("<KeyRelease>", self.auto_sync_names)
        ToolTip(e_app, "Display name of your web application. Automatically updates output filename, isolated profile folder, and offline screen title.")

        ttk.Label(c1, text="Web Application URL:", style="Card.TLabel").grid(row=3, column=0, sticky="w", pady=4, padx=(0, 10))
        e_url = ttk.Entry(c1, textvariable=self.var_url)
        e_url.grid(row=3, column=1, columnspan=2, sticky="ew", pady=4)
        ToolTip(e_url, "Full URL of your hosted or local web app (e.g., https://hms.clientdomain.com or http://localhost:8080).")

        ttk.Label(c1, text="Target Browser Engine:", style="Card.TLabel").grid(row=4, column=0, sticky="w", pady=4, padx=(0, 10))
        cmb_br = ttk.Combobox(
            c1,
            textvariable=self.var_browser_target,
            values=[
                "Auto (Chrome -> Edge -> Brave)",
                "Google Chrome Only",
                "Microsoft Edge Only",
                "Brave Browser Only"
            ],
            state="readonly"
        )
        cmb_br.grid(row=4, column=1, columnspan=2, sticky="ew", pady=4)
        ToolTip(cmb_br, "Auto mode checks for Google Chrome first, then falls back to Microsoft Edge (pre-installed on Windows 10/11) or Brave if Chrome is missing.")

        ttk.Label(c1, text="Launcher Icon (.ico/.png):", style="Card.TLabel").grid(row=5, column=0, sticky="w", pady=4, padx=(0, 10))
        icon_row = ttk.Frame(c1, style="Card.TFrame")
        icon_row.grid(row=5, column=1, columnspan=2, sticky="ew", pady=4)
        e_icon = ttk.Entry(icon_row, textvariable=self.var_icon_path)
        e_icon.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ToolTip(e_icon, "Path to a custom .ico, .png, .jpg, or .webp logo. PNG/JPG files are automatically converted into multi-resolution Windows .ico icons.")

        self.lbl_icon_thumb = tk.Label(icon_row, text="No Icon", bg="#f1f5f9", fg="#64748b", font=("Segoe UI", 7), width=7, height=2, relief="solid", bd=1)
        self.lbl_icon_thumb.pack(side="left", padx=(0, 6))
        ToolTip(self.lbl_icon_thumb, "Live preview thumbnail of the icon that will be embedded into the client's .exe file.")

        btn_icon = ttk.Button(icon_row, text="Browse", style="Secondary.TButton", command=self.browse_icon)
        btn_icon.pack(side="left")
        ToolTip(btn_icon, "Select a logo image or .ico file from your computer.")

        ttk.Label(c1, text="Output Base Filename:", style="Card.TLabel").grid(row=6, column=0, sticky="w", pady=4, padx=(0, 10))
        e_out = ttk.Entry(c1, textvariable=self.var_output_name)
        e_out.grid(row=6, column=1, columnspan=2, sticky="ew", pady=4)
        ToolTip(e_out, "Base filename (without extension) for generated .exe, .bat, .cmd, .vbs, and .zip deliverables.")

        ttk.Label(c1, text="Deliverables Folder:", style="Card.TLabel").grid(row=7, column=0, sticky="w", pady=4, padx=(0, 10))
        e_dir = ttk.Entry(c1, textvariable=self.var_output_dir)
        e_dir.grid(row=7, column=1, sticky="ew", pady=4, padx=(0, 6))
        ToolTip(e_dir, "Destination folder where all generated client executables, scripts, and ZIP packages will be saved.")

        btn_dir = ttk.Button(c1, text="Browse", style="Secondary.TButton", command=self.browse_output_dir)
        btn_dir.pack_forget()
        btn_dir = ttk.Button(c1, text="Browse", style="Secondary.TButton", command=self.browse_output_dir)
        btn_dir.grid(row=7, column=2, sticky="e", pady=4)
        ToolTip(btn_dir, "Choose an output folder for generated files.")

        w2, c2_box = self.create_card(parent)
        w2.pack(fill="x", pady=(0, 10))
        c2 = ttk.Frame(c2_box, style="Card.TFrame")
        c2.pack(fill="x", padx=14, pady=12)
        c2.columnconfigure(0, weight=1)
        c2.columnconfigure(1, weight=1)

        ttk.Label(c2, text="2. Window Mode & Chromium Kiosk Attributes", style="SectionTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        mode_row = ttk.Frame(c2, style="Card.TFrame")
        mode_row.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        rb_kiosk = ttk.Radiobutton(mode_row, text="Full Kiosk (--kiosk)", variable=self.var_launch_mode, value="kiosk", style="Card.TRadiobutton")
        rb_kiosk.pack(side="left", padx=(0, 16))
        ToolTip(rb_kiosk, "Locks the browser into borderless fullscreen without address bar, tabs, or window controls. Ideal for POS counters and public terminals.")

        rb_app = ttk.Radiobutton(mode_row, text="Standalone App Window (--app)", variable=self.var_launch_mode, value="app", style="Card.TRadiobutton")
        rb_app.pack(side="left", padx=(0, 16))
        ToolTip(rb_app, "Opens the site in a clean native-looking window with titlebar/minimize/close buttons but no URL bar or browser tabs.")

        rb_norm = ttk.Radiobutton(mode_row, text="Standard Browser Window", variable=self.var_launch_mode, value="normal", style="Card.TRadiobutton")
        rb_norm.pack(side="left")
        ToolTip(rb_norm, "Opens the URL in a standard browser window while still applying your selected profile, proxy, or startup flags.")

        left_checks = [
            ("Silent POS Printing (--kiosk-printing)", self.var_kiosk_printing, "Bypasses the Chrome print preview dialog and prints immediately to the Windows default thermal/laser printer. Essential for POS & hospital token receipts."),
            ("Isolated App Profile (--user-data-dir)", self.var_isolated_profile, "Creates a dedicated browser data folder for this web app so --kiosk flags work even when the client already has regular Chrome windows open."),
            ("Incognito / Ephemeral Mode (--incognito)", self.var_incognito, "Starts in private mode so cookies, form history, and login sessions are never retained between runs."),
            ("Disable Touch Pinch-Zoom (--disable-pinch)", self.var_disable_pinch, "Prevents accidental zooming on touchscreen POS monitors and kiosks."),
            ("Disable Swipe Back/Forward Navigation", self.var_disable_swipe_nav, "Blocks two-finger touchpad or touchscreen edge swipes from accidentally navigating backward out of your app."),
            ("Skip First-Run & Default Browser Prompts", self.var_no_first_run, "Suppresses 'Welcome to Chrome' and 'Set as default browser' popups on fresh profiles.")
        ]

        right_checks = [
            ("Suppress Crash & Restore Bubbles", self.var_suppress_dialogs, "Hides 'Chrome didn't shut down correctly - Restore pages?' popups after power outages."),
            ("Allow Sound & Alert Autoplay", self.var_autoplay_media, "Permits notification chimes, queue token voice announcements, and audio alerts without requiring a prior click."),
            ("Disable Translate Page Popup", self.var_disable_translate, "Stops Google Translate bar from popping up on multilingual or local-language interfaces."),
            ("Disable All Browser Extensions", self.var_disable_extensions, "Prevents third-party adblockers or extensions from interfering with your web app scripts."),
            ("Start Maximized (--start-maximized)", self.var_start_maximized, "Launches App Window mode maximized to fill the desktop work area."),
            ("Start Fullscreen (--start-fullscreen)", self.var_start_fullscreen, "Starts in F11-style fullscreen while still allowing F11 toggle.")
        ]

        for idx, (text, var, tip) in enumerate(left_checks):
            chk = ttk.Checkbutton(c2, text=text, variable=var, style="Card.TCheckbutton")
            chk.grid(row=idx + 2, column=0, sticky="w", pady=2, padx=(0, 8))
            ToolTip(chk, tip)

        for idx, (text, var, tip) in enumerate(right_checks):
            chk = ttk.Checkbutton(c2, text=text, variable=var, style="Card.TCheckbutton")
            chk.grid(row=idx + 2, column=1, sticky="w", pady=2)
            ToolTip(chk, tip)

        prof_frame = ttk.Frame(c2, style="Card.TFrame")
        prof_frame.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(8, 4))
        ttk.Label(prof_frame, text="Isolated Profile Folder:", style="Card.TLabel").pack(side="left", padx=(0, 8))
        e_prof = ttk.Entry(prof_frame, textvariable=self.var_profile_folder, width=28)
        e_prof.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ToolTip(e_prof, "Subfolder name inside %LOCALAPPDATA%\\WebAppKiosks\\ where cookies, localStorage, and IndexedDB for this client app are stored.")

        ttk.Label(prof_frame, text="UI Scale:", style="Card.TLabel").pack(side="left", padx=(0, 4))
        sp_scale = ttk.Spinbox(prof_frame, textvariable=self.var_scale_factor, values=("0.75", "0.85", "0.9", "1.0", "1.1", "1.25", "1.5"), width=6)
        sp_scale.pack(side="left")
        ToolTip(sp_scale, "Forces Chromium DPI zoom scaling (--force-device-scale-factor). Helpful for high-DPI screens or compact POS displays.")

        geom_frame = ttk.Frame(c2, style="Card.TFrame")
        geom_frame.grid(row=9, column=0, columnspan=2, sticky="ew", pady=4)
        chk_geom = ttk.Checkbutton(geom_frame, text="Custom Window Bounds:", variable=self.var_custom_geometry, style="Card.TCheckbutton")
        chk_geom.pack(side="left", padx=(0, 6))
        ToolTip(chk_geom, "Set explicit pixel dimensions and screen X/Y coordinates (useful for positioning on a second monitor, e.g., X=1920, Y=0).")

        for lbl_txt, var_obj, tip_txt in [
            ("W:", self.var_win_width, "Window width in pixels."),
            ("H:", self.var_win_height, "Window height in pixels."),
            ("X:", self.var_win_x, "Horizontal screen offset in pixels (use primary monitor width for 2nd display)."),
            ("Y:", self.var_win_y, "Vertical screen offset in pixels.")
        ]:
            ttk.Label(geom_frame, text=lbl_txt, style="Card.TLabel").pack(side="left")
            ent_g = ttk.Entry(geom_frame, textvariable=var_obj, width=6)
            ent_g.pack(side="left", padx=(2, 6))
            ToolTip(ent_g, tip_txt)

        extra_frame = ttk.Frame(c2, style="Card.TFrame")
        extra_frame.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(6, 2))
        ttk.Label(extra_frame, text="Custom CLI Flags:", style="Card.TLabel").pack(side="left", padx=(0, 8))
        e_extra = ttk.Entry(extra_frame, textvariable=self.var_extra_flags)
        e_extra.pack(side="left", fill="x", expand=True)
        ToolTip(e_extra, "Append any advanced Chromium command-line switches separated by spaces (e.g., --disable-print-preview --ash-no-nudges).")

        w3, c3_box = self.create_card(parent)
        w3.pack(fill="x", pady=(0, 6))
        c3 = ttk.Frame(c3_box, style="Card.TFrame")
        c3.pack(fill="x", padx=14, pady=12)
        c3.columnconfigure(0, weight=1)
        c3.columnconfigure(1, weight=1)

        ttk.Label(c3, text="3. Deliverable Package Formats & Runtime Behavior", style="SectionTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        deliverables = [
            ("Portable Single-File .EXE (PyInstaller)", self.var_gen_exe, 1, 0, "Compiles a standalone, console-free Windows executable with your custom icon and embedded metadata."),
            ("Windows Batch Script (.bat)", self.var_gen_bat, 1, 1, "Generates a lightweight, zero-dependency .bat launcher that auto-detects Chrome/Edge/Brave."),
            ("Windows Command Script (.cmd)", self.var_gen_cmd, 2, 0, "Generates a .cmd script variant for enterprise Windows environments."),
            ("Silent VBScript Launcher (.vbs)", self.var_gen_vbs, 2, 1, "Generates a silent .vbs wrapper that launches the batch file with zero black command-prompt flash."),
            ("Desktop Shortcut Creator (.bat)", self.var_gen_shortcut_helper, 3, 0, "Includes a helper script that creates a proper Windows Desktop shortcut (.lnk) with your icon."),
            ("Windows Auto-Start Installer (.bat)", self.var_add_startup_helper, 3, 1, "Includes a 1-click installer script to register the kiosk app in Windows Startup on boot."),
            ("Emergency Kiosk Exit/Reset Tool (.bat)", self.var_add_kill_helper, 4, 0, "Includes a support utility script that cleanly terminates stuck kiosk processes without closing regular Chrome."),
            ("Bundle Client Delivery .ZIP + Guide", self.var_gen_zip, 4, 1, "Packages all generated launchers, helper scripts, and a formatted client README into a ready-to-send ZIP archive.")
        ]

        for label, var, r, c, tip in deliverables:
            chk = ttk.Checkbutton(c3, text=label, variable=var, style="Card.TCheckbutton")
            chk.grid(row=r, column=c, sticky="w", pady=2, padx=(0, 8))
            ToolTip(chk, tip)

        chk_kill = ttk.Checkbutton(c3, text="Close Previous Instance of This App Before Launching", variable=self.var_kill_existing, style="Card.TCheckbutton")
        chk_kill.grid(row=5, column=0, columnspan=2, sticky="w", pady=(6, 0))
        ToolTip(chk_kill, "If the client double-clicks the icon while this kiosk app is already running, closes the old instance of this isolated profile before launching fresh.")

    def build_right_workspace(self, parent):
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=0)
        parent.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        self.tab_preview = ttk.Frame(self.notebook, style="Card.TFrame")
        self.tab_network = ttk.Frame(self.notebook, style="Card.TFrame")
        self.tab_branding = ttk.Frame(self.notebook, style="Card.TFrame")
        self.tab_batch = ttk.Frame(self.notebook, style="Card.TFrame")
        self.tab_console = ttk.Frame(self.notebook, style="Card.TFrame")

        self.notebook.add(self.tab_preview, text="  Code & Script Preview  ")
        self.notebook.add(self.tab_network, text="  Network & Offline Guard  ")
        self.notebook.add(self.tab_branding, text="  EXE Metadata & Security  ")
        self.notebook.add(self.tab_batch, text="  Multi-Client Batch Build  ")
        self.notebook.add(self.tab_console, text="  Build Log & Diagnostics  ")

        self.build_tab_preview(self.tab_preview)
        self.build_tab_network(self.tab_network)
        self.build_tab_branding(self.tab_branding)
        self.build_tab_batch(self.tab_batch)
        self.build_tab_console(self.tab_console)

        action_wrap, action_card = self.create_card(parent)
        action_wrap.grid(row=1, column=0, sticky="ew")
        act = ttk.Frame(action_card, style="Card.TFrame")
        act.pack(fill="x", padx=14, pady=10)

        self.btn_test = ttk.Button(act, text="Test Launch on This PC", style="Secondary.TButton", command=self.test_launch_now)
        self.btn_test.pack(side="left", padx=(0, 8))
        ToolTip(self.btn_test, "Immediately test-launch the configured web app on your own machine using your exact kiosk flags and isolated profile.")

        btn_open_out = ttk.Button(act, text="Open Output Folder", style="Secondary.TButton", command=self.open_output_folder)
        btn_open_out.pack(side="left", padx=(0, 8))
        ToolTip(btn_open_out, "Open the destination folder containing your compiled .exe, .bat, and .zip deliverables.")

        self.btn_generate = ttk.Button(act, text="Build & Package Client Launcher(s)", style="Success.TButton", command=self.start_generation)
        self.btn_generate.pack(side="right", fill="x", expand=True)
        ToolTip(self.btn_generate, "Compile and generate all selected client executables, scripts, helper utilities, and ZIP delivery package.")

    def build_tab_preview(self, parent):
        inner = ttk.Frame(parent, style="Card.TFrame")
        inner.pack(fill="both", expand=True, padx=14, pady=12)

        hdr = ttk.Frame(inner, style="Card.TFrame")
        hdr.pack(fill="x", pady=(0, 8))

        ttk.Label(hdr, text="Inspect Generated Output:", style="SectionTitle.TLabel").pack(side="left", padx=(0, 10))
        cmb_view = ttk.Combobox(
            hdr,
            textvariable=self.var_preview_type,
            values=["CLI Command", "Windows Batch (.bat / .cmd)", "Portable EXE Python Source", "Silent VBScript (.vbs)"],
            state="readonly",
            width=28
        )
        cmb_view.pack(side="left")
        cmb_view.bind("<<ComboboxSelected>>", lambda e: self.update_all_previews())
        ToolTip(cmb_view, "Switch between live previews of the raw browser command, .bat script, compiled .exe source, or .vbs silent wrapper.")

        btn_copy = ttk.Button(hdr, text="Copy Code", style="Primary.TButton", command=self.copy_current_preview)
        btn_copy.pack(side="right")
        ToolTip(btn_copy, "Copy the currently displayed script or command to the clipboard.")

        code_frame = tk.Frame(inner, bg="#cbd5e1", bd=1)
        code_frame.pack(fill="both", expand=True)

        self.txt_preview = tk.Text(
            code_frame,
            bg="#f8fafc",
            fg="#0f172a",
            insertbackground="#0f172a",
            font=("Consolas", 9),
            relief="flat",
            wrap="word",
            padx=10,
            pady=10
        )
        scroll = ttk.Scrollbar(code_frame, orient="vertical", command=self.txt_preview.yview)
        self.txt_preview.configure(yscrollcommand=scroll.set)
        self.txt_preview.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def build_tab_network(self, parent):
        inner = ttk.Frame(parent, style="Card.TFrame")
        inner.pack(fill="both", expand=True, padx=14, pady=12)
        inner.columnconfigure(1, weight=1)

        ttk.Label(inner, text="Pre-Launch Connectivity Guard & Offline Fallback", style="SectionTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        chk_hc = ttk.Checkbutton(inner, text="Verify Server / Internet Reachability Before Launching Browser", variable=self.var_health_check, style="Card.TCheckbutton")
        chk_hc.grid(row=1, column=0, columnspan=2, sticky="w", pady=3)
        ToolTip(chk_hc, "Checks if the target URL responds before opening the kiosk, preventing Chrome 'No Internet' error screens on slow boot Wi-Fi.")

        retry_row = ttk.Frame(inner, style="Card.TFrame")
        retry_row.grid(row=2, column=0, columnspan=2, sticky="ew", pady=4)
        ttk.Label(retry_row, text="Connection Retry Attempts (2s interval):", style="Card.TLabel").pack(side="left", padx=(0, 8))
        sp_ret = ttk.Spinbox(retry_row, textvariable=self.var_health_retries, from_=1, to=20, width=6)
        sp_ret.pack(side="left", padx=(0, 16))
        ToolTip(sp_ret, "Number of connection checks (2 seconds apart) to wait for the client's router or local server to come online.")

        chk_fb = ttk.Checkbutton(inner, text="Show Branded Offline / Auto-Reconnect Screen if Unreachable", variable=self.var_offline_fallback, style="Card.TCheckbutton")
        chk_fb.grid(row=3, column=0, columnspan=2, sticky="w", pady=3)
        ToolTip(chk_fb, "If the server is still unreachable after retries, opens a clean branded HTML status page that automatically retries every 5 seconds until online.")

        ttk.Label(inner, text="Support Contact on Offline Screen:", style="Card.TLabel").grid(row=4, column=0, sticky="w", pady=4, padx=(0, 10))
        e_sup = ttk.Entry(inner, textvariable=self.var_support_phone)
        e_sup.grid(row=4, column=1, sticky="ew", pady=4)
        ToolTip(e_sup, "Your technical support phone number or email displayed on the client's offline fallback screen.")

        ttk.Separator(inner, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", pady=12)
        ttk.Label(inner, text="SSL, Session Hygiene & Custom Network Overrides", style="SectionTitle.TLabel").grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 8))

        chk_ssl = ttk.Checkbutton(inner, text="Ignore Self-Signed SSL Certificate Warnings (--ignore-certificate-errors)", variable=self.var_ignore_cert_errors, style="Card.TCheckbutton")
        chk_ssl.grid(row=7, column=0, columnspan=2, sticky="w", pady=3)
        ToolTip(chk_ssl, "Bypasses HTTPS certificate warnings for local hospital/school LAN servers using self-signed SSL certificates.")

        chk_cc = ttk.Checkbutton(inner, text="Purge Browser Disk Cache Before Each Launch", variable=self.var_clear_cache_on_launch, style="Card.TCheckbutton")
        chk_cc.grid(row=8, column=0, columnspan=2, sticky="w", pady=3)
        ToolTip(chk_cc, "Clears cached JS/CSS assets inside the isolated profile on startup so clients always load your latest web app updates.")

        chk_cs = ttk.Checkbutton(inner, text="Wipe Cookies & Login Session After Kiosk Closes", variable=self.var_clear_session_on_exit, style="Card.TCheckbutton")
        chk_cs.grid(row=9, column=0, columnspan=2, sticky="w", pady=3)
        ToolTip(chk_cs, "Deletes session cookies and storage after the window exits—ideal for shared shift terminals.")

        ttk.Label(inner, text="Custom Proxy Server (Optional):", style="Card.TLabel").grid(row=10, column=0, sticky="w", pady=4, padx=(0, 10))
        e_prx = ttk.Entry(inner, textvariable=self.var_proxy_server)
        e_prx.grid(row=10, column=1, sticky="ew", pady=4)
        ToolTip(e_prx, "Optional proxy server address (e.g., http://192.168.1.1:8080 or socks5://127.0.0.1:1080). Leave blank for direct connection.")

        ttk.Label(inner, text="Custom User-Agent (Optional):", style="Card.TLabel").grid(row=11, column=0, sticky="w", pady=4, padx=(0, 10))
        e_ua = ttk.Entry(inner, textvariable=self.var_user_agent)
        e_ua.grid(row=11, column=1, sticky="ew", pady=4)
        ToolTip(e_ua, "Override browser User-Agent string if your backend checks for a custom client identifier.")

    def build_tab_branding(self, parent):
        inner = ttk.Frame(parent, style="Card.TFrame")
        inner.pack(fill="both", expand=True, padx=14, pady=12)
        inner.columnconfigure(1, weight=1)

        ttk.Label(inner, text="Windows Executable (.EXE) Version & Publisher Metadata", style="SectionTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))
        ttk.Label(inner, text="Embedded directly into the compiled .exe Windows File Properties -> Details tab.", style="Muted.TLabel").grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        fields = [
            ("Company / Studio Name:", self.var_exe_company, "Your software company or studio name shown as Publisher in Windows file properties."),
            ("Product Name:", self.var_exe_product, "Official product title embedded in the executable metadata."),
            ("File Description:", self.var_exe_desc, "Description shown in Windows Task Manager and File Explorer tooltips."),
            ("File & Product Version:", self.var_exe_version, "Four-part Windows version number (e.g., 1.0.0.0)."),
            ("Copyright Notice:", self.var_exe_copyright, "Legal copyright string embedded into the compiled binary.")
        ]

        for idx, (lbl, var, tip) in enumerate(fields):
            ttk.Label(inner, text=lbl, style="Card.TLabel").grid(row=idx + 2, column=0, sticky="w", pady=5, padx=(0, 12))
            ent = ttk.Entry(inner, textvariable=var)
            ent.grid(row=idx + 2, column=1, sticky="ew", pady=5)
            ToolTip(ent, tip)

        ttk.Separator(inner, orient="horizontal").grid(row=7, column=0, columnspan=2, sticky="ew", pady=12)
        ttk.Label(inner, text="Windows Privilege & Manifest Settings", style="SectionTitle.TLabel").grid(row=8, column=0, columnspan=2, sticky="w", pady=(0, 6))

        chk_uac = ttk.Checkbutton(inner, text="Request Administrator Elevation on Launch (--uac-admin)", variable=self.var_uac_admin, style="Card.TCheckbutton")
        chk_uac.grid(row=9, column=0, columnspan=2, sticky="w", pady=4)
        ToolTip(chk_uac, "Adds a Windows UAC manifest requiring Administrator rights when double-clicked. Keep unchecked for standard desktop user accounts.")

    def build_tab_batch(self, parent):
        inner = ttk.Frame(parent, style="Card.TFrame")
        inner.pack(fill="both", expand=True, padx=14, pady=12)

        ttk.Label(inner, text="Batch Multi-Client Launcher Compiler", style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 4))
        ttk.Label(inner, text="Select multiple saved client profiles below to compile all their launchers and ZIP packages in one automated run.", style="Muted.TLabel").pack(anchor="w", pady=(0, 8))

        list_frame = tk.Frame(inner, bg="#cbd5e1", bd=1)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.lst_batch = tk.Listbox(
            list_frame,
            selectmode="multiple",
            bg="#f8fafc",
            fg="#0f172a",
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            font=("Segoe UI", 9),
            relief="flat",
            bd=6
        )
        b_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.lst_batch.yview)
        self.lst_batch.configure(yscrollcommand=b_scroll.set)
        self.lst_batch.pack(side="left", fill="both", expand=True)
        b_scroll.pack(side="right", fill="y")
        ToolTip(self.lst_batch, "Click to select or deselect multiple saved client profiles for batch compilation.")
        self.refresh_batch_listbox()

        btn_row = ttk.Frame(inner, style="Card.TFrame")
        btn_row.pack(fill="x")

        b_all = ttk.Button(btn_row, text="Select All", style="Secondary.TButton", command=lambda: self.lst_batch.select_set(0, "end"))
        b_all.pack(side="left", padx=(0, 6))
        ToolTip(b_all, "Select all saved client profiles in the list.")

        b_none = ttk.Button(btn_row, text="Clear Selection", style="Secondary.TButton", command=lambda: self.lst_batch.selection_clear(0, "end"))
        b_none.pack(side="left", padx=(0, 6))
        ToolTip(b_none, "Deselect all profiles.")

        self.btn_batch_build = ttk.Button(btn_row, text="Compile Selected Client Profiles", style="Primary.TButton", command=self.start_batch_generation)
        self.btn_batch_build.pack(side="right")
        ToolTip(self.btn_batch_build, "Sequentially loads each selected client profile and compiles its configured executables and delivery packages.")

    def build_tab_console(self, parent):
        inner = ttk.Frame(parent, style="Card.TFrame")
        inner.pack(fill="both", expand=True, padx=14, pady=12)

        diag_hdr = ttk.Frame(inner, style="Card.TFrame")
        diag_hdr.pack(fill="x", pady=(0, 6))
        ttk.Label(diag_hdr, text="Local Browser Engine Audit & Build Console", style="SectionTitle.TLabel").pack(side="left")

        btn_audit = ttk.Button(diag_hdr, text="Re-Scan Browsers", style="Secondary.TButton", command=self.audit_installed_browsers)
        btn_audit.pack(side="right", padx=(6, 0))
        ToolTip(btn_audit, "Scan this Windows machine for installed Chromium browsers (Chrome, Edge, Brave).")

        btn_clear_log = ttk.Button(diag_hdr, text="Clear Log", style="Secondary.TButton", command=self.clear_console_log)
        btn_clear_log.pack(side="right")
        ToolTip(btn_clear_log, "Clear the build console output.")

        log_frame = tk.Frame(inner, bg="#cbd5e1", bd=1)
        log_frame.pack(fill="both", expand=True)

        self.txt_log = tk.Text(
            log_frame,
            bg="#f8fafc",
            fg="#1e293b",
            font=("Consolas", 9),
            relief="flat",
            wrap="word",
            padx=10,
            pady=10,
            state="disabled"
        )
        l_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.txt_log.yview)
        self.txt_log.configure(yscrollcommand=l_scroll.set)
        self.txt_log.pack(side="left", fill="both", expand=True)
        l_scroll.pack(side="right", fill="y")

    def bind_live_preview(self):
        tracked_vars = [
            self.var_client_name, self.var_app_name, self.var_url, self.var_output_name,
            self.var_browser_target, self.var_launch_mode, self.var_kiosk_printing,
            self.var_isolated_profile, self.var_profile_folder, self.var_incognito,
            self.var_disable_pinch, self.var_disable_swipe_nav, self.var_no_first_run,
            self.var_suppress_dialogs, self.var_autoplay_media, self.var_disable_translate,
            self.var_start_maximized, self.var_start_fullscreen, self.var_disable_extensions,
            self.var_custom_geometry, self.var_win_width, self.var_win_height,
            self.var_win_x, self.var_win_y, self.var_scale_factor, self.var_extra_flags,
            self.var_health_check, self.var_health_retries, self.var_offline_fallback,
            self.var_support_phone, self.var_ignore_cert_errors, self.var_clear_cache_on_launch,
            self.var_clear_session_on_exit, self.var_proxy_server, self.var_user_agent,
            self.var_kill_existing
        ]
        for v in tracked_vars:
            v.trace_add("write", lambda *args: self.update_all_previews())

    def sanitize_slug(self, text):
        cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", text.strip())
        return cleaned.strip("_") or "Client_WebApp"

    def auto_sync_names(self, event=None):
        slug = self.sanitize_slug(self.var_app_name.get())
        self.var_output_name.set(f"{slug}_Launcher")
        self.var_profile_folder.set(f"{slug}_Profile")
        self.var_exe_product.set(f"{self.var_app_name.get().strip()} Kiosk")

    def apply_selected_preset(self, event=None):
        preset_name = self.var_preset.get()
        data = PRESETS.get(preset_name)
        if not data:
            return
        self.var_launch_mode.set(data["launch_mode"])
        self.var_kiosk_printing.set(data["kiosk_printing"])
        self.var_isolated_profile.set(data["isolated_profile"])
        self.var_incognito.set(data["incognito"])
        self.var_disable_pinch.set(data["disable_pinch"])
        self.var_disable_swipe_nav.set(data["disable_swipe_nav"])
        self.var_no_first_run.set(data["no_first_run"])
        self.var_suppress_dialogs.set(data["suppress_dialogs"])
        self.var_autoplay_media.set(data["autoplay_media"])
        self.var_disable_translate.set(data["disable_translate"])
        self.var_start_maximized.set(data["start_maximized"])
        self.var_start_fullscreen.set(data["start_fullscreen"])
        self.var_disable_extensions.set(data["disable_extensions"])
        self.var_ignore_cert_errors.set(data["ignore_cert_errors"])
        self.var_clear_cache_on_launch.set(data["clear_cache_on_launch"])
        self.var_clear_session_on_exit.set(data["clear_session_on_exit"])
        self.var_scale_factor.set(data["scale_factor"])
        self.var_extra_flags.set(data["extra_flags"])
        self.log(f"Applied preset profile: {preset_name}")

    def build_flag_list(self, profile_dir_token=None, target_url_override=None):
        url = target_url_override or self.var_url.get().strip() or "https://example.com"
        if not re.match(r"^(https?|file)://", url, re.IGNORECASE):
            url = "https://" + url

        flags = []
        mode = self.var_launch_mode.get()

        if mode == "kiosk":
            flags.append("--kiosk")
        elif mode == "app":
            flags.append(f"--app={url}")

        if self.var_kiosk_printing.get():
            flags.append("--kiosk-printing")

        if self.var_isolated_profile.get():
            folder = self.sanitize_slug(self.var_profile_folder.get())
            if profile_dir_token:
                flags.append(f'--user-data-dir="{profile_dir_token}"')
            else:
                flags.append(f'--user-data-dir="%LOCALAPPDATA%\\WebAppKiosks\\{folder}"')

        if self.var_incognito.get():
            flags.append("--incognito")
        if self.var_disable_pinch.get():
            flags.append("--disable-pinch")
        if self.var_disable_swipe_nav.get():
            flags.append("--overscroll-history-navigation=0")
        if self.var_no_first_run.get():
            flags.append("--no-first-run")
            flags.append("--no-default-browser-check")
        if self.var_suppress_dialogs.get():
            flags.append("--noerrdialogs")
            flags.append("--disable-session-crashed-bubble")
            flags.append("--disable-infobars")
        if self.var_autoplay_media.get():
            flags.append("--autoplay-policy=no-user-gesture-required")
        if self.var_disable_translate.get():
            flags.append("--disable-features=Translate")
        if self.var_disable_extensions.get():
            flags.append("--disable-extensions")
        if self.var_start_maximized.get():
            flags.append("--start-maximized")
        if self.var_start_fullscreen.get():
            flags.append("--start-fullscreen")
        if self.var_ignore_cert_errors.get():
            flags.append("--ignore-certificate-errors")

        scale = self.var_scale_factor.get().strip()
        if scale and scale != "1.0":
            flags.append(f"--force-device-scale-factor={scale}")

        proxy = self.var_proxy_server.get().strip()
        if proxy:
            flags.append(f"--proxy-server={proxy}")

        ua = self.var_user_agent.get().strip()
        if ua:
            flags.append(f'--user-agent="{ua}"')

        if self.var_custom_geometry.get():
            w = self.var_win_width.get().strip()
            h = self.var_win_height.get().strip()
            x = self.var_win_x.get().strip()
            y = self.var_win_y.get().strip()
            if w.isdigit() and h.isdigit():
                flags.append(f"--window-size={w},{h}")
            if x.lstrip("-").isdigit() and y.lstrip("-").isdigit():
                flags.append(f"--window-position={x},{y}")

        extra = self.var_extra_flags.get().strip()
        if extra:
            flags.extend(extra.split())

        if mode in ("kiosk", "normal"):
            flags.append(f'"{url}"')

        return flags, url

    def update_all_previews(self):
        view = self.var_preview_type.get()
        if view == "CLI Command":
            flags, _ = self.build_flag_list()
            content = f'chrome.exe {" ".join(flags)}'
        elif view == "Windows Batch (.bat / .cmd)":
            content = self.generate_batch_content()
        elif view == "Portable EXE Python Source":
            content = self.generate_embedded_python_source()
        else:
            base_name = self.sanitize_slug(self.var_output_name.get())
            content = self.generate_vbs_content(f"{base_name}.bat")

        self.txt_preview.delete("1.0", "end")
        self.txt_preview.insert("1.0", content)

    def copy_current_preview(self):
        text = self.txt_preview.get("1.0", "end").strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.log(f"Copied {self.var_preview_type.get()} to clipboard.")

    def log(self, message):
        def _append():
            self.txt_log.configure(state="normal")
            ts = time.strftime("%H:%M:%S")
            self.txt_log.insert("end", f"[{ts}] {message}\n")
            self.txt_log.see("end")
            self.txt_log.configure(state="disabled")
        self.root.after(0, _append)

    def clear_console_log(self):
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.configure(state="disabled")

    def browse_icon(self):
        path = filedialog.askopenfilename(
            title="Select Application Logo or Icon",
            filetypes=[("Image & Icon Files", "*.ico *.png *.jpg *.jpeg *.bmp *.webp"), ("All Files", "*.*")]
        )
        if path:
            self.var_icon_path.set(path)
            self.update_icon_thumbnail(path)

    def update_icon_thumbnail(self, path):
        if not path or not os.path.isfile(path):
            self.lbl_icon_thumb.configure(image="", text="No Icon")
            self.icon_preview_img = None
            return
        try:
            from PIL import Image, ImageTk
            img = Image.open(path)
            img.thumbnail((32, 32))
            self.icon_preview_img = ImageTk.PhotoImage(img)
            self.lbl_icon_thumb.configure(image=self.icon_preview_img, text="", width=34, height=34)
        except Exception:
            self.lbl_icon_thumb.configure(image="", text=os.path.splitext(path)[1].upper())

    def browse_output_dir(self):
        path = filedialog.askdirectory(title="Select Deliverables Folder")
        if path:
            self.var_output_dir.set(path)

    def open_output_folder(self):
        out_dir = self.var_output_dir.get().strip()
        if os.path.isdir(out_dir):
            if os.name == "nt":
                os.startfile(out_dir)
            else:
                subprocess.Popen(["xdg-open", out_dir])
        else:
            messagebox.showinfo("Folder Not Found", "Generate a launcher first or choose an existing output directory.")

    def check_dependencies(self):
        has_pyinstaller = shutil.which("pyinstaller") is not None
        if not has_pyinstaller:
            try:
                import PyInstaller
                has_pyinstaller = True
            except ImportError:
                has_pyinstaller = False

        try:
            import PIL
            has_pillow = True
        except ImportError:
            has_pillow = False

        return has_pyinstaller, has_pillow

    def refresh_dependency_status(self):
        has_pyi, has_pil = self.check_dependencies()
        if has_pyi and has_pil:
            self.lbl_dep_status.configure(text="Build Engine Ready (PyInstaller + Pillow)", style="BadgeOk.TLabel")
            self.btn_install_deps.configure(state="disabled", text="Tools Installed")
        else:
            missing = []
            if not has_pyi:
                missing.append("PyInstaller")
            if not has_pil:
                missing.append("Pillow")
            self.lbl_dep_status.configure(text=f"Missing: {', '.join(missing)}", style="BadgeWarn.TLabel")
            self.btn_install_deps.configure(state="normal", text="Install Build Tools")

    def install_dependencies(self):
        def _worker():
            self.root.after(0, lambda: self.btn_install_deps.configure(state="disabled", text="Installing..."))
            self.notebook.select(self.tab_console)
            self.log("Installing pyinstaller and pillow via pip...")
            try:
                proc = subprocess.Popen(
                    [sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller", "pillow"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                for line in proc.stdout:
                    clean = line.strip()
                    if clean:
                        self.log(clean)
                proc.wait()
                self.log("Build tools installation finished.")
            except Exception as exc:
                self.log(f"Installation error: {exc}")
            finally:
                self.root.after(0, self.refresh_dependency_status)

        threading.Thread(target=_worker, daemon=True).start()

    def get_browser_candidates(self):
        target = self.var_browser_target.get()
        chrome_paths = [
            r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
            r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
            r"%LocalAppData%\Google\Chrome\Application\chrome.exe"
        ]
        edge_paths = [
            r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
            r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
        ]
        brave_paths = [
            r"%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"%ProgramFiles(x86)%\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"%LocalAppData%\BraveSoftware\Brave-Browser\Application\brave.exe"
        ]
        if target == "Google Chrome Only":
            return chrome_paths
        if target == "Microsoft Edge Only":
            return edge_paths
        if target == "Brave Browser Only":
            return brave_paths
        return chrome_paths + edge_paths + brave_paths

    def audit_installed_browsers(self):
        self.log("Scanning local Windows environment for Chromium browser engines...")
        found = 0
        for raw_path in self.get_browser_candidates():
            expanded = os.path.expandvars(raw_path)
            if os.path.isfile(expanded):
                found += 1
                self.log(f"  [FOUND] {expanded}")
        if found == 0:
            self.log("  [WARNING] No Chromium browsers detected in standard installation directories.")

    def find_local_browser_exe(self):
        for raw_path in self.get_browser_candidates():
            expanded = os.path.expandvars(raw_path)
            if os.path.isfile(expanded):
                return expanded
        return None

    def test_launch_now(self):
        browser_exe = self.find_local_browser_exe()
        if not browser_exe:
            messagebox.showerror("Browser Not Found", "Could not locate the selected Chromium browser on this PC.")
            return

        folder = self.sanitize_slug(self.var_profile_folder.get())
        local_profile = os.path.join(os.path.expandvars("%LOCALAPPDATA%"), "WebAppKiosks", folder)
        flags, url = self.build_flag_list(profile_dir_token=local_profile)

        raw_args = []
        for f in flags:
            if f.startswith('--user-data-dir="'):
                raw_args.append(f"--user-data-dir={local_profile}")
            elif f.startswith("--user-agent=\""):
                raw_args.append("--user-agent=" + f[len('--user-agent="'):-1])
            elif f.startswith('"') and f.endswith('"'):
                raw_args.append(f[1:-1])
            else:
                raw_args.append(f)

        self.log(f"Test launching {os.path.basename(browser_exe)} -> {url}")
        try:
            subprocess.Popen([browser_exe] + raw_args)
        except Exception as exc:
            self.log(f"Test launch failed: {exc}")
            messagebox.showerror("Launch Error", str(exc))

    def prepare_ico_file(self, work_dir):
        src_icon = self.var_icon_path.get().strip()
        if not src_icon or not os.path.isfile(src_icon):
            return None

        ext = os.path.splitext(src_icon)[1].lower()
        dest_ico = os.path.join(work_dir, "app_icon.ico")
        if ext == ".ico":
            shutil.copy2(src_icon, dest_ico)
            return dest_ico

        try:
            from PIL import Image
            img = Image.open(src_icon).convert("RGBA")
            img.save(dest_ico, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
            self.log("Converted logo image to multi-resolution Windows .ICO file.")
            return dest_ico
        except Exception as exc:
            self.log(f"Icon conversion skipped (install Pillow for image-to-ICO): {exc}")
            return None

    def generate_version_info_file(self, work_dir):
        ver_raw = self.var_exe_version.get().strip()
        parts = [int(x) for x in re.findall(r"\d+", ver_raw)[:4]]
        while len(parts) < 4:
            parts.append(0)
        v_tuple = f"({parts[0]}, {parts[1]}, {parts[2]}, {parts[3]})"
        v_str = f"{parts[0]}.{parts[1]}.{parts[2]}.{parts[3]}"

        company = self.var_exe_company.get().strip().replace("'", "")
        product = self.var_exe_product.get().strip().replace("'", "")
        desc = self.var_exe_desc.get().strip().replace("'", "")
        copy_str = self.var_exe_copyright.get().strip().replace("'", "")
        internal = self.sanitize_slug(self.var_output_name.get())

        content = f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={v_tuple},
    prodvers={v_tuple},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{company}'),
        StringStruct(u'FileDescription', u'{desc}'),
        StringStruct(u'FileVersion', u'{v_str}'),
        StringStruct(u'InternalName', u'{internal}'),
        StringStruct(u'LegalCopyright', u'{copy_str}'),
        StringStruct(u'OriginalFilename', u'{internal}.exe'),
        StringStruct(u'ProductName', u'{product}'),
        StringStruct(u'ProductVersion', u'{v_str}')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
        ver_file = os.path.join(work_dir, "version_info.txt")
        with open(ver_file, "w", encoding="utf-8") as f:
            f.write(content)
        return ver_file

    def build_offline_fallback_html(self, target_url):
        app_title = self.var_app_name.get().strip() or "Web Application"
        client_name = self.var_client_name.get().strip() or "Client Terminal"
        support = self.var_support_phone.get().strip() or "Technical Support"
        safe_url = json.dumps(target_url)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{app_title} - Connection Status</title>
<style>
  body {{ margin: 0; font-family: 'Segoe UI', system-ui, sans-serif; background: #f1f5f9; color: #0f172a; display: flex; align-items: center; justify-content: center; height: 100vh; }}
  .card {{ background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 36px 42px; max-width: 480px; text-align: center; box-shadow: 0 10px 25px rgba(15,23,42,0.08); }}
  .badge {{ display: inline-block; background: #fef3c7; color: #92400e; font-weight: 700; font-size: 12px; padding: 4px 12px; border-radius: 999px; margin-bottom: 14px; }}
  h1 {{ margin: 0 0 8px; font-size: 22px; }}
  p {{ color: #475569; font-size: 14px; line-height: 1.5; margin: 0 0 20px; }}
  .meta {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; font-size: 12px; color: #334155; margin-bottom: 20px; }}
  button {{ background: #2563eb; color: #fff; border: none; border-radius: 8px; padding: 10px 22px; font-size: 14px; font-weight: 600; cursor: pointer; }}
  button:hover {{ background: #1d4ed8; }}
</style>
</head>
<body>
  <div class="card">
    <div class="badge">WAITING FOR NETWORK / SERVER</div>
    <h1>{app_title}</h1>
    <p>Unable to reach the application server right now. Check your internet or local network cable. This terminal will reconnect automatically.</p>
    <div class="meta">
      <div><strong>Terminal:</strong> {client_name}</div>
      <div><strong>Support:</strong> {support}</div>
      <div id="status" style="margin-top:6px;color:#2563eb;font-weight:600;">Retrying connection in 5s...</div>
    </div>
    <button onclick="retryNow()">Reconnect Now</button>
  </div>
<script>
  const TARGET_URL = {safe_url};
  let sec = 5;
  function retryNow() {{
    document.getElementById('status').innerText = 'Connecting...';
    window.location.href = TARGET_URL;
  }}
  setInterval(() => {{
    sec--;
    if (sec <= 0) {{
      retryNow();
      sec = 5;
    }} else {{
      document.getElementById('status').innerText = 'Retrying connection in ' + sec + 's...';
    }}
  }}, 1000);
</script>
</body>
</html>"""
        return html

    def generate_batch_content(self):
        flags, url = self.build_flag_list()
        candidates = self.get_browser_candidates()
        app_title = self.var_app_name.get().strip() or "Web App Kiosk"
        folder = self.sanitize_slug(self.var_profile_folder.get())
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname or ""

        lines = [
            "@echo off",
            "setlocal EnableDelayedExpansion",
            f"title {app_title}",
            'set "BROWSER_EXE="'
        ]

        for p in candidates:
            lines.append(f'if not defined BROWSER_EXE if exist "{p}" set "BROWSER_EXE={p}"')

        lines.extend([
            'if not defined BROWSER_EXE (',
            '    echo Google Chrome or Microsoft Edge was not found on this computer.',
            '    pause',
            '    exit /b 1',
            ')'
        ])

        if self.var_kill_existing.get() and self.var_isolated_profile.get():
            lines.append(f'powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object {{ $_.CommandLine -like \'*{folder}*\' }} | ForEach-Object {{ Stop-Process -Id $_.ProcessId -Force }}" >nul 2>&1')

        if self.var_isolated_profile.get():
            lines.append(f'set "PROFILE_DIR=%LOCALAPPDATA%\\WebAppKiosks\\{folder}"')
            lines.append('if not exist "%PROFILE_DIR%" mkdir "%PROFILE_DIR%"')
            if self.var_clear_cache_on_launch.get():
                lines.append('if exist "%PROFILE_DIR%\\Default\\Cache" rmdir /s /q "%PROFILE_DIR%\\Default\\Cache" >nul 2>&1')
                lines.append('if exist "%PROFILE_DIR%\\Default\\Code Cache" rmdir /s /q "%PROFILE_DIR%\\Default\\Code Cache" >nul 2>&1')

        if self.var_health_check.get() and host:
            retries = max(1, int(self.var_health_retries.get() or 3))
            lines.extend([
                f'set /a RETRIES={retries}',
                ':CHECK_NET',
                f'powershell -NoProfile -Command "try {{ $r = Invoke-WebRequest -Uri \'{url}\' -UseBasicParsing -TimeoutSec 3; exit 0 }} catch {{ exit 1 }}" >nul 2>&1',
                'if %errorlevel% equ 0 goto LAUNCH_APP',
                'set /a RETRIES-=1',
                'if %RETRIES% gtr 0 (',
                '    timeout /t 2 /nobreak >nul',
                '    goto CHECK_NET',
                ')'
            ])

        lines.append(":LAUNCH_APP")
        flag_str = " ".join(flags)
        lines.append(f'start "" "%BROWSER_EXE%" {flag_str}')
        lines.append("exit /b 0")
        return "\r\n".join(lines) + "\r\n"

    def generate_vbs_content(self, bat_filename):
        lines = [
            'Set WshShell = CreateObject("WScript.Shell")',
            'Set FSO = CreateObject("Scripting.FileSystemObject")',
            'ScriptDir = FSO.GetParentFolderName(WScript.ScriptFullName)',
            f'BatPath = ScriptDir & "\\{bat_filename}"',
            'If FSO.FileExists(BatPath) Then',
            '    WshShell.Run Chr(34) & BatPath & Chr(34), 0, False',
            'Else',
            f'    MsgBox "Missing launcher script: {bat_filename}", 16, "Launcher Error"',
            'End If'
        ]
        return "\r\n".join(lines) + "\r\n"

    def generate_embedded_python_source(self):
        flags, url = self.build_flag_list(profile_dir_token="__PROFILE_DIR__")
        candidates = self.get_browser_candidates()
        folder = self.sanitize_slug(self.var_profile_folder.get())
        use_isolated = self.var_isolated_profile.get()
        kill_existing = self.var_kill_existing.get()
        app_title = self.var_app_name.get().strip() or "Web App Kiosk"
        health_check = self.var_health_check.get()
        retries = max(1, int(self.var_health_retries.get() or 3))
        use_fallback = self.var_offline_fallback.get()
        clear_cache = self.var_clear_cache_on_launch.get()
        clear_session = self.var_clear_session_on_exit.get()
        fallback_b64 = base64.b64encode(self.build_offline_fallback_html(url).encode("utf-8")).decode("ascii")

        clean_args = []
        for f in flags:
            if f.startswith("--user-agent=\""):
                clean_args.append("--user-agent=" + f[len('--user-agent="'):-1])
            elif f.startswith('"') and f.endswith('"'):
                clean_args.append(f[1:-1])
            else:
                clean_args.append(f)

        source = f"""import base64
import ctypes
import os
import shutil
import ssl
import subprocess
import sys
import time
import urllib.request

CANDIDATES = {json.dumps(candidates)}
RAW_ARGS = {json.dumps(clean_args)}
TARGET_URL = {json.dumps(url)}
PROFILE_FOLDER = {json.dumps(folder)}
USE_ISOLATED = {repr(use_isolated)}
KILL_EXISTING = {repr(kill_existing)}
APP_TITLE = {json.dumps(app_title)}
HEALTH_CHECK = {repr(health_check)}
MAX_RETRIES = {retries}
USE_FALLBACK = {repr(use_fallback)}
CLEAR_CACHE = {repr(clear_cache)}
CLEAR_SESSION = {repr(clear_session)}
FALLBACK_B64 = {json.dumps(fallback_b64)}

def find_browser():
    for raw in CANDIDATES:
        expanded = os.path.expandvars(raw)
        if os.path.isfile(expanded):
            return expanded
    return None

def is_url_reachable(target):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    for _ in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(target, headers={{"User-Agent": "Mozilla/5.0"}})
            with urllib.request.urlopen(req, timeout=3, context=ctx):
                return True
        except Exception:
            time.sleep(2)
    return False

def kill_previous_instances():
    try:
        ps_cmd = f"Get-CimInstance Win32_Process | Where-Object {{ $_.CommandLine -like '*{{PROFILE_FOLDER}}*' }} | ForEach-Object {{ Stop-Process -Id $_.ProcessId -Force }}"
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=0x08000000
        )
    except Exception:
        pass

def clean_profile_cache(profile_dir):
    for sub in ["Cache", "Code Cache", "GPUCache"]:
        target = os.path.join(profile_dir, "Default", sub)
        if os.path.isdir(target):
            shutil.rmtree(target, ignore_errors=True)

def clean_profile_session(profile_dir):
    for item in ["Cookies", "Cookies-journal", "Session Storage", "Local Storage"]:
        target = os.path.join(profile_dir, "Default", item)
        if os.path.isfile(target):
            try:
                os.remove(target)
            except Exception:
                pass
        elif os.path.isdir(target):
            shutil.rmtree(target, ignore_errors=True)

def main():
    browser = find_browser()
    if not browser:
        ctypes.windll.user32.MessageBoxW(
            0,
            "Google Chrome or Microsoft Edge was not found on this computer.\\nPlease install Google Chrome to launch " + APP_TITLE + ".",
            APP_TITLE + " - Browser Missing",
            0x10
        )
        sys.exit(1)

    base_app_dir = os.path.join(os.path.expandvars("%LOCALAPPDATA%"), "WebAppKiosks", PROFILE_FOLDER)
    os.makedirs(base_app_dir, exist_ok=True)

    if USE_ISOLATED:
        if KILL_EXISTING:
            kill_previous_instances()
        if CLEAR_CACHE:
            clean_profile_cache(base_app_dir)

    launch_target = TARGET_URL
    if HEALTH_CHECK and not TARGET_URL.lower().startswith("file://"):
        if not is_url_reachable(TARGET_URL) and USE_FALLBACK:
            fallback_path = os.path.join(base_app_dir, "offline_guard.html")
            with open(fallback_path, "wb") as f:
                f.write(base64.b64decode(FALLBACK_B64))
            launch_target = "file:///" + fallback_path.replace("\\\\", "/")

    final_args = []
    for arg in RAW_ARGS:
        if "__PROFILE_DIR__" in arg:
            final_args.append(arg.replace("__PROFILE_DIR__", base_app_dir))
        elif arg == TARGET_URL:
            final_args.append(launch_target)
        elif arg.startswith("--app="):
            final_args.append("--app=" + launch_target)
        else:
            final_args.append(arg)

    proc = subprocess.Popen([browser] + final_args)
    if CLEAR_SESSION and USE_ISOLATED:
        proc.wait()
        clean_profile_session(base_app_dir)

if __name__ == "__main__":
    main()
"""
        return source

    def generate_desktop_shortcut_bat(self, target_filename):
        app_title = self.var_app_name.get().strip() or "Web App Kiosk"
        safe_title = re.sub(r'[\\/:*?"<>|]+', "", app_title)
        lines = [
            "@echo off",
            f'title Create Desktop Shortcut for {safe_title}',
            f'set "TARGET=%~dp0{target_filename}"',
            'if not exist "%TARGET%" (',
            f'    echo Error: Place this script in the same folder as {target_filename}',
            '    pause',
            '    exit /b 1',
            ')',
            f'powershell -NoProfile -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut([Environment]::GetFolderPath(\'Desktop\') + \'\\{safe_title}.lnk\'); $s.TargetPath = \'%TARGET%\'; $s.WorkingDirectory = \'%~dp0\'; $s.Save()"',
            f'echo Desktop shortcut created: {safe_title}',
            'pause'
        ]
        return "\r\n".join(lines) + "\r\n"

    def generate_startup_helper_bat(self, target_filename):
        app_title = self.var_app_name.get().strip() or "Web App Kiosk"
        lines = [
            "@echo off",
            f"title Configure Auto-Start on Boot - {app_title}",
            'set "STARTUP_DIR=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"',
            f'set "SOURCE_FILE=%~dp0{target_filename}"',
            'if not exist "%SOURCE_FILE%" (',
            f'    echo Error: Place this installer in the same folder as {target_filename}',
            '    pause',
            '    exit /b 1',
            ')',
            f'copy /y "%SOURCE_FILE%" "%STARTUP_DIR%\\{target_filename}" >nul',
            f'echo {app_title} has been installed to Windows Startup.',
            'pause'
        ]
        return "\r\n".join(lines) + "\r\n"

    def generate_kill_helper_bat(self):
        app_title = self.var_app_name.get().strip() or "Web App Kiosk"
        folder = self.sanitize_slug(self.var_profile_folder.get())
        lines = [
            "@echo off",
            f"title Close {app_title} Kiosk",
            f'powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object {{ $_.CommandLine -like \'*{folder}*\' }} | ForEach-Object {{ Stop-Process -Id $_.ProcessId -Force }}"',
            f"echo Closed all active instances of {app_title}.",
            "timeout /t 2 /nobreak >nul"
        ]
        return "\r\n".join(lines) + "\r\n"

    def generate_readme_text(self, generated_files):
        client = self.var_client_name.get().strip() or "Valued Client"
        app = self.var_app_name.get().strip() or "Web Application"
        url = self.var_url.get().strip()
        mode = self.var_launch_mode.get().upper()
        support = self.var_support_phone.get().strip()
        files_list = "\n".join([f"  * {os.path.basename(f)}" for f in generated_files])
        return (
            f"====================================================================\n"
            f"  {app} - Desktop Client Launcher Package\n"
            f"  Prepared Exclusively For: {client}\n"
            f"====================================================================\n\n"
            f"Application URL : {url}\n"
            f"Display Mode    : {mode}\n"
            f"Technical Desk  : {support}\n\n"
            f"Included Files:\n{files_list}\n\n"
            f"Quick Deployment Guide:\n"
            f"  1. Extract all files to a permanent folder (e.g., C:\\{self.sanitize_slug(app)}\\).\n"
            f"  2. Double-click the .exe (or .bat) file to launch {app}.\n"
            f"  3. Optional: Run 'Create_Desktop_Shortcut.bat' to place an icon on Desktop.\n"
            f"  4. Optional: Run 'Install_AutoStart.bat' to launch automatically on Windows boot.\n"
            f"  5. To exit Full Kiosk mode at any time, press Alt + F4 on your keyboard.\n"
        )

    def start_generation(self):
        if self.is_building:
            return
        if not (self.var_gen_exe.get() or self.var_gen_bat.get() or self.var_gen_cmd.get()):
            messagebox.showwarning("No Launcher Selected", "Select at least one primary launcher format (.exe, .bat, or .cmd).")
            return

        if self.var_gen_exe.get():
            has_pyi, _ = self.check_dependencies()
            if not has_pyi:
                messagebox.showerror(
                    "PyInstaller Required",
                    "PyInstaller is required to build a portable .exe.\nClick 'Install Build Tools' in the top bar or uncheck .EXE."
                )
                return

        self.is_building = True
        self.notebook.select(self.tab_console)
        self.btn_generate.configure(state="disabled", text="Compiling Deliverables...")
        threading.Thread(target=self.build_single_client_worker, args=(True,), daemon=True).start()

    def start_batch_generation(self):
        if self.is_building:
            return
        selected_indices = self.lst_batch.curselection()
        if not selected_indices:
            messagebox.showwarning("No Profiles Selected", "Select one or more saved client profiles from the list first.")
            return

        keys = [self.lst_batch.get(i) for i in selected_indices]
        self.is_building = True
        self.notebook.select(self.tab_console)
        self.btn_generate.configure(state="disabled", text="Batch Building...")
        self.btn_batch_build.configure(state="disabled")

        def _batch_worker():
            try:
                self.log("====================================================")
                self.log(f"STARTING BATCH BUILD FOR {len(keys)} CLIENT PROFILE(S)")
                for idx, key in enumerate(keys, start=1):
                    self.log(f"\n[{idx}/{len(keys)}] Loading profile: {key}")
                    self.root.after(0, lambda k=key: self.apply_profile_dict(self.clients_data[k]))
                    time.sleep(0.25)
                    self.build_single_client_worker(show_popup=False)
                self.log("\nALL BATCH BUILDS COMPLETED SUCCESSFULLY!")
                self.root.after(0, lambda: messagebox.showinfo("Batch Build Complete", f"Successfully compiled {len(keys)} client launcher packages!"))
            except Exception as exc:
                self.log(f"BATCH BUILD ERROR: {exc}")
            finally:
                self.is_building = False
                self.root.after(0, lambda: self.btn_generate.configure(state="normal", text="Build & Package Client Launcher(s)"))
                self.root.after(0, lambda: self.btn_batch_build.configure(state="normal"))

        threading.Thread(target=_batch_worker, daemon=True).start()

    def build_single_client_worker(self, show_popup=True):
        generated_files = []
        work_dir = None
        try:
            out_dir = self.var_output_dir.get().strip()
            os.makedirs(out_dir, exist_ok=True)
            base_name = self.sanitize_slug(self.var_output_name.get())

            self.log("----------------------------------------------------")
            self.log(f"Building launcher set for: {self.var_client_name.get()} -> {self.var_app_name.get()}")

            bat_filename = f"{base_name}.bat"
            if self.var_gen_bat.get() or self.var_gen_vbs.get():
                bat_path = os.path.join(out_dir, bat_filename)
                with open(bat_path, "w", encoding="utf-8", newline="") as f:
                    f.write(self.generate_batch_content())
                if self.var_gen_bat.get():
                    generated_files.append(bat_path)
                    self.log(f"  + Created Batch Launcher: {bat_path}")

            if self.var_gen_cmd.get():
                cmd_path = os.path.join(out_dir, f"{base_name}.cmd")
                with open(cmd_path, "w", encoding="utf-8", newline="") as f:
                    f.write(self.generate_batch_content())
                generated_files.append(cmd_path)
                self.log(f"  + Created CMD Launcher: {cmd_path}")

            if self.var_gen_vbs.get():
                vbs_path = os.path.join(out_dir, f"{base_name}_Silent.vbs")
                with open(vbs_path, "w", encoding="utf-8", newline="") as f:
                    f.write(self.generate_vbs_content(bat_filename))
                generated_files.append(vbs_path)
                self.log(f"  + Created Silent VBS Wrapper: {vbs_path}")

            primary_target = os.path.basename(generated_files[0]) if generated_files else bat_filename

            if self.var_gen_exe.get():
                work_dir = tempfile.mkdtemp(prefix="kioskforge_")
                stub_py = os.path.join(work_dir, f"{base_name}.py")
                with open(stub_py, "w", encoding="utf-8") as f:
                    f.write(self.generate_embedded_python_source())

                ico_path = self.prepare_ico_file(work_dir)
                ver_path = self.generate_version_info_file(work_dir)
                dist_dir = os.path.join(work_dir, "dist")
                build_dir = os.path.join(work_dir, "build")

                pyi_cmd = [
                    sys.executable,
                    "-m",
                    "PyInstaller",
                    "--noconfirm",
                    "--onefile",
                    "--noconsole",
                    "--clean",
                    "--distpath", dist_dir,
                    "--workpath", build_dir,
                    "--specpath", work_dir,
                    "--version-file", ver_path,
                    "--name", base_name
                ]
                if ico_path:
                    pyi_cmd.extend(["--icon", ico_path])
                if self.var_uac_admin.get():
                    pyi_cmd.append("--uac-admin")
                pyi_cmd.append(stub_py)

                self.log("  * Compiling portable single-file .EXE with PyInstaller...")
                proc = subprocess.Popen(
                    pyi_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=0x08000000 if os.name == "nt" else 0
                )
                for line in proc.stdout:
                    clean = line.strip()
                    if clean and ("INFO:" in clean or "ERROR:" in clean or "WARNING:" in clean):
                        self.log(f"    {clean}")
                proc.wait()

                built_exe = os.path.join(dist_dir, f"{base_name}.exe")
                if proc.returncode == 0 and os.path.isfile(built_exe):
                    final_exe = os.path.join(out_dir, f"{base_name}.exe")
                    shutil.copy2(built_exe, final_exe)
                    generated_files.insert(0, final_exe)
                    primary_target = os.path.basename(final_exe)
                    self.log(f"  + Compiled Portable EXE: {final_exe}")
                else:
                    raise RuntimeError("PyInstaller failed to build the executable. Review console logs.")

            if self.var_gen_shortcut_helper.get():
                sc_bat = os.path.join(out_dir, f"Create_{base_name}_Desktop_Shortcut.bat")
                with open(sc_bat, "w", encoding="utf-8", newline="") as f:
                    f.write(self.generate_desktop_shortcut_bat(primary_target))
                generated_files.append(sc_bat)
                self.log(f"  + Created Desktop Shortcut Helper: {sc_bat}")

            if self.var_add_startup_helper.get():
                st_bat = os.path.join(out_dir, f"Install_{base_name}_AutoStart.bat")
                with open(st_bat, "w", encoding="utf-8", newline="") as f:
                    f.write(self.generate_startup_helper_bat(primary_target))
                generated_files.append(st_bat)
                self.log(f"  + Created Windows Auto-Start Installer: {st_bat}")

            if self.var_add_kill_helper.get():
                kl_bat = os.path.join(out_dir, f"Close_{base_name}_Kiosk.bat")
                with open(kl_bat, "w", encoding="utf-8", newline="") as f:
                    f.write(self.generate_kill_helper_bat())
                generated_files.append(kl_bat)
                self.log(f"  + Created Emergency Kiosk Close Utility: {kl_bat}")

            if self.var_gen_zip.get() and generated_files:
                zip_path = os.path.join(out_dir, f"{base_name}_Client_Deliverable.zip")
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for item in generated_files:
                        zf.write(item, arcname=os.path.basename(item))
                    zf.writestr("README_Client_Instructions.txt", self.generate_readme_text(generated_files))
                self.log(f"  + Packaged Client Delivery ZIP: {zip_path}")

            self.log("Build completed cleanly!")
            if show_popup:
                self.root.after(0, lambda: messagebox.showinfo("Build Successful", f"Generated {len(generated_files)} deliverable file(s) in:\n{out_dir}"))

        except Exception as exc:
            self.log(f"BUILD ERROR: {exc}")
            if show_popup:
                self.root.after(0, lambda: messagebox.showerror("Build Failed", str(exc)))
        finally:
            if work_dir and os.path.isdir(work_dir):
                shutil.rmtree(work_dir, ignore_errors=True)
            if show_popup:
                self.is_building = False
                self.root.after(0, lambda: self.btn_generate.configure(state="normal", text="Build & Package Client Launcher(s)"))

    def load_clients_data(self):
        if os.path.isfile(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_clients_data(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.clients_data, f, indent=2)
        except Exception as exc:
            self.log(f"Error saving database: {exc}")

    def refresh_saved_profiles_dropdown(self):
        keys = sorted(self.clients_data.keys())
        self.cmb_saved["values"] = keys
        if keys and self.var_saved_profile.get() not in keys:
            self.var_saved_profile.set(keys[0])
        if hasattr(self, "lst_batch"):
            self.refresh_batch_listbox()

    def refresh_batch_listbox(self):
        self.lst_batch.delete(0, "end")
        for key in sorted(self.clients_data.keys()):
            self.lst_batch.insert("end", key)

    def save_current_profile(self):
        client = self.var_client_name.get().strip() or "Client"
        app = self.var_app_name.get().strip() or "WebApp"
        key = f"{client} - {app}"

        self.clients_data[key] = {
            "client_name": self.var_client_name.get(),
            "app_name": self.var_app_name.get(),
            "url": self.var_url.get(),
            "output_name": self.var_output_name.get(),
            "output_dir": self.var_output_dir.get(),
            "icon_path": self.var_icon_path.get(),
            "browser_target": self.var_browser_target.get(),
            "launch_mode": self.var_launch_mode.get(),
            "kiosk_printing": self.var_kiosk_printing.get(),
            "isolated_profile": self.var_isolated_profile.get(),
            "profile_folder": self.var_profile_folder.get(),
            "incognito": self.var_incognito.get(),
            "disable_pinch": self.var_disable_pinch.get(),
            "disable_swipe_nav": self.var_disable_swipe_nav.get(),
            "no_first_run": self.var_no_first_run.get(),
            "suppress_dialogs": self.var_suppress_dialogs.get(),
            "autoplay_media": self.var_autoplay_media.get(),
            "disable_translate": self.var_disable_translate.get(),
            "start_maximized": self.var_start_maximized.get(),
            "start_fullscreen": self.var_start_fullscreen.get(),
            "disable_extensions": self.var_disable_extensions.get(),
            "custom_geometry": self.var_custom_geometry.get(),
            "win_width": self.var_win_width.get(),
            "win_height": self.var_win_height.get(),
            "win_x": self.var_win_x.get(),
            "win_y": self.var_win_y.get(),
            "scale_factor": self.var_scale_factor.get(),
            "extra_flags": self.var_extra_flags.get(),
            "health_check": self.var_health_check.get(),
            "health_retries": self.var_health_retries.get(),
            "offline_fallback": self.var_offline_fallback.get(),
            "support_phone": self.var_support_phone.get(),
            "ignore_cert_errors": self.var_ignore_cert_errors.get(),
            "clear_cache_on_launch": self.var_clear_cache_on_launch.get(),
            "clear_session_on_exit": self.var_clear_session_on_exit.get(),
            "proxy_server": self.var_proxy_server.get(),
            "user_agent": self.var_user_agent.get(),
            "exe_company": self.var_exe_company.get(),
            "exe_product": self.var_exe_product.get(),
            "exe_desc": self.var_exe_desc.get(),
            "exe_version": self.var_exe_version.get(),
            "exe_copyright": self.var_exe_copyright.get(),
            "uac_admin": self.var_uac_admin.get(),
            "gen_exe": self.var_gen_exe.get(),
            "gen_bat": self.var_gen_bat.get(),
            "gen_cmd": self.var_gen_cmd.get(),
            "gen_vbs": self.var_gen_vbs.get(),
            "gen_shortcut_helper": self.var_gen_shortcut_helper.get(),
            "add_startup_helper": self.var_add_startup_helper.get(),
            "add_kill_helper": self.var_add_kill_helper.get(),
            "gen_zip": self.var_gen_zip.get(),
            "kill_existing": self.var_kill_existing.get()
        }
        self.save_clients_data()
        self.var_saved_profile.set(key)
        self.refresh_saved_profiles_dropdown()
        self.log(f"Saved client profile: {key}")

    def apply_profile_dict(self, data):
        self.var_client_name.set(data.get("client_name", ""))
        self.var_app_name.set(data.get("app_name", ""))
        self.var_url.set(data.get("url", ""))
        self.var_output_name.set(data.get("output_name", ""))
        self.var_output_dir.set(data.get("output_dir", self.var_output_dir.get()))
        icon_p = data.get("icon_path", "")
        self.var_icon_path.set(icon_p)
        self.update_icon_thumbnail(icon_p)
        self.var_browser_target.set(data.get("browser_target", "Auto (Chrome -> Edge -> Brave)"))
        self.var_launch_mode.set(data.get("launch_mode", "kiosk"))
        self.var_kiosk_printing.set(data.get("kiosk_printing", False))
        self.var_isolated_profile.set(data.get("isolated_profile", True))
        self.var_profile_folder.set(data.get("profile_folder", ""))
        self.var_incognito.set(data.get("incognito", False))
        self.var_disable_pinch.set(data.get("disable_pinch", False))
        self.var_disable_swipe_nav.set(data.get("disable_swipe_nav", False))
        self.var_no_first_run.set(data.get("no_first_run", True))
        self.var_suppress_dialogs.set(data.get("suppress_dialogs", True))
        self.var_autoplay_media.set(data.get("autoplay_media", True))
        self.var_disable_translate.set(data.get("disable_translate", True))
        self.var_start_maximized.set(data.get("start_maximized", False))
        self.var_start_fullscreen.set(data.get("start_fullscreen", False))
        self.var_disable_extensions.set(data.get("disable_extensions", False))
        self.var_custom_geometry.set(data.get("custom_geometry", False))
        self.var_win_width.set(data.get("win_width", "1366"))
        self.var_win_height.set(data.get("win_height", "768"))
        self.var_win_x.set(data.get("win_x", "0"))
        self.var_win_y.set(data.get("win_y", "0"))
        self.var_scale_factor.set(data.get("scale_factor", "1.0"))
        self.var_extra_flags.set(data.get("extra_flags", ""))
        self.var_health_check.set(data.get("health_check", True))
        self.var_health_retries.set(data.get("health_retries", "3"))
        self.var_offline_fallback.set(data.get("offline_fallback", True))
        self.var_support_phone.set(data.get("support_phone", ""))
        self.var_ignore_cert_errors.set(data.get("ignore_cert_errors", False))
        self.var_clear_cache_on_launch.set(data.get("clear_cache_on_launch", False))
        self.var_clear_session_on_exit.set(data.get("clear_session_on_exit", False))
        self.var_proxy_server.set(data.get("proxy_server", ""))
        self.var_user_agent.set(data.get("user_agent", ""))
        self.var_exe_company.set(data.get("exe_company", ""))
        self.var_exe_product.set(data.get("exe_product", ""))
        self.var_exe_desc.set(data.get("exe_desc", ""))
        self.var_exe_version.set(data.get("exe_version", "1.0.0.0"))
        self.var_exe_copyright.set(data.get("exe_copyright", ""))
        self.var_uac_admin.set(data.get("uac_admin", False))
        self.var_gen_exe.set(data.get("gen_exe", True))
        self.var_gen_bat.set(data.get("gen_bat", True))
        self.var_gen_cmd.set(data.get("gen_cmd", False))
        self.var_gen_vbs.set(data.get("gen_vbs", True))
        self.var_gen_shortcut_helper.set(data.get("gen_shortcut_helper", True))
        self.var_add_startup_helper.set(data.get("add_startup_helper", True))
        self.var_add_kill_helper.set(data.get("add_kill_helper", True))
        self.var_gen_zip.set(data.get("gen_zip", True))
        self.var_kill_existing.set(data.get("kill_existing", True))

    def load_selected_profile(self):
        key = self.var_saved_profile.get()
        data = self.clients_data.get(key)
        if not data:
            return
        self.apply_profile_dict(data)
        self.log(f"Loaded client profile: {key}")

    def delete_selected_profile(self):
        key = self.var_saved_profile.get()
        if key in self.clients_data:
            del self.clients_data[key]
            self.save_clients_data()
            self.var_saved_profile.set("")
            self.refresh_saved_profiles_dropdown()
            self.log(f"Deleted profile: {key}")

    def import_profiles_json(self):
        path = filedialog.askopenfilename(title="Import Client Profiles JSON", filetypes=[("JSON Files", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                imported = json.load(f)
            if isinstance(imported, dict):
                self.clients_data.update(imported)
                self.save_clients_data()
                self.refresh_saved_profiles_dropdown()
                self.log(f"Imported {len(imported)} client profile(s) from {path}")
        except Exception as exc:
            messagebox.showerror("Import Error", str(exc))

    def export_profiles_json(self):
        path = filedialog.asksaveasfilename(title="Export Client Profiles JSON", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.clients_data, f, indent=2)
            self.log(f"Exported {len(self.clients_data)} client profile(s) to {path}")
        except Exception as exc:
            messagebox.showerror("Export Error", str(exc))


if __name__ == "__main__":
    root = tk.Tk()
    app = KioskForgeApp(root)
    root.mainloop()