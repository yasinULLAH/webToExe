# KioskForge Pro

**Enterprise Client Web App & Portable EXE Builder**

Version **2.4.0** · Windows desktop application · Python + Tkinter

A single-window production studio that turns any hosted or local web application into a **locked-down, branded, double-clickable Windows launcher** — a portable `.exe`, a `.bat`/`.cmd` script, a silent `.vbs` wrapper, plus desktop-shortcut, auto-start, emergency-close helpers and a ready-to-send delivery ZIP — with a client profile database, deployment presets, a live code preview, a network/offline guard, EXE metadata branding and multi-client batch compilation.

### 📚 Documentation Set

| File | Audience | Language | Purpose |
|---|---|---|---|
| **`README.md`** *(this file)* | Developers & operators | English + اردو | Complete technical and operational manual |
| **`CLIENT-README.md`** | The client receiving the launcher | اردو only | Simple, non-technical end-user handbook |
| **`FEATURES.md`** | Management & pre-sales | English | Comprehensive feature, module and capability report |

> **Send which file to whom?** Give `CLIENT-README.md` to the client with the delivery ZIP. Keep `README.md` for your team and use `FEATURES.md` in proposals, quotations and scope documents.

---

## 📑 Table of Contents

**Part A — English Documentation**

1. [What Is KioskForge Pro?](#1-what-is-kioskforge-pro)
2. [Who Is It For?](#2-who-is-it-for)
3. [Problems It Solves](#3-problems-it-solves)
4. [Feature Matrix at a Glance](#4-feature-matrix-at-a-glance)
5. [System Requirements](#5-system-requirements)
6. [Installation](#6-installation)
7. [First Launch & Interface Map](#7-first-launch--interface-map)
8. [End-to-End Quick Start (5 Minutes)](#8-end-to-end-quick-start-5-minutes)
9. [Module Reference](#9-module-reference)
   - 9.1 [Top Bar — Build Engine Status](#91-top-bar--build-engine-status)
   - 9.2 [Toolbar — Client Profile Manager](#92-toolbar--client-profile-manager)
   - 9.3 [Toolbar — Deployment Presets](#93-toolbar--deployment-presets)
   - 9.4 [Card 1 — Client Identity & Target Web Application](#94-card-1--client-identity--target-web-application)
   - 9.5 [Card 2 — Window Mode & Chromium Kiosk Attributes](#95-card-2--window-mode--chromium-kiosk-attributes)
   - 9.6 [Card 3 — Deliverable Formats & Runtime Behaviour](#96-card-3--deliverable-formats--runtime-behaviour)
   - 9.7 [Tab — Code & Script Preview](#97-tab--code--script-preview)
   - 9.8 [Tab — Network & Offline Guard](#98-tab--network--offline-guard)
   - 9.9 [Tab — EXE Metadata & Security](#99-tab--exe-metadata--security)
   - 9.10 [Tab — Multi-Client Batch Build](#910-tab--multi-client-batch-build)
   - 9.11 [Tab — Build Log & Diagnostics](#911-tab--build-log--diagnostics)
   - 9.12 [Action Bar — Test, Open Folder, Build](#912-action-bar--test-open-folder-build)
10. [The Build Pipeline — Exact Order of Operations](#10-the-build-pipeline--exact-order-of-operations)
11. [Generated Files Reference](#11-generated-files-reference)
12. [Runtime Behaviour of the Generated Launchers](#12-runtime-behaviour-of-the-generated-launchers)
13. [The Branded Offline Guard Screen](#13-the-branded-offline-guard-screen)
14. [Data & Configuration Reference](#14-data--configuration-reference)
15. [Import, Export & Backup](#15-import-export--backup)
16. [Common Workflows](#16-common-workflows)
17. [Troubleshooting](#17-troubleshooting)
18. [Best Practices](#18-best-practices)
19. [Limitations & Things to Know](#19-limitations--things-to-know)
20. [FAQ](#20-faq)
21. [Glossary](#21-glossary)
22. [Repository Layout](#22-repository-layout)
23. [Changelog](#23-changelog)
24. [Support & Credits](#24-support--credits)

**Part B — اردو دستاویزات**

25. [اردو تعارف](#25-اردو-تعارف)
26. [یہ ایپ کس کے لیے ہے](#26-یہ-ایپ-کس-کے-لیے-ہے)
27. [اہم خصوصیات ایک نظر میں](#27-اہم-خصوصیات-ایک-نظر-میں)
28. [سسٹم کی ضروریات اور تنصیب](#28-سسٹم-کی-ضروریات-اور-تنصیب)
29. [انٹرفیس کا مکمل نقشہ](#29-انٹرفیس-کا-مکمل-نقشہ)
30. [ہر ماڈیول کی تفصیل](#30-ہر-ماڈیول-کی-تفصیل)
31. [بنانے کا مکمل طریقہ — قدم بہ قدم](#31-بنانے-کا-مکمل-طریقہ--قدم-بہ-قدم)
32. [بننے والی فائلیں](#32-بننے-والی-فائلیں)
33. [کلائنٹ کے کمپیوٹر پر پروگرام کیسے چلتا ہے](#33-کلائنٹ-کے-کمپیوٹر-پر-پروگرام-کیسے-چلتا-ہے)
34. [آف لائن اسکرین](#34-آف-لائن-اسکرین)
35. [پروفائلز، بیک اپ اور منتقلی](#35-پروفائلز-بیک-اپ-اور-منتقلی)
36. [عام استعمال کے منظرنامے](#36-عام-استعمال-کے-منظرنامے)
37. [مسائل اور ان کا حل](#37-مسائل-اور-ان-کا-حل)
38. [بہترین طریقے](#38-بہترین-طریقے)
39. [اکثر پوچھے جانے والے سوالات](#39-اکثر-پوچھے-جانے-والے-سوالات)
40. [آسان لغت](#40-آسان-لغت)

---

# PART A — ENGLISH

## 1. What Is KioskForge Pro?

KioskForge Pro is a Windows desktop **launcher factory**. You point it at a web application (for example `https://hms.yourclient.com`, `http://192.168.1.50/school`, or `http://localhost:8080`), describe how it should behave on the client's machine, choose which files you want to hand over, and press **Build**. The app produces a complete, professional delivery package.

It is **not** a website builder and it does **not** host or copy your web application. Your web app stays on your server exactly where it is. KioskForge Pro only creates the **client-side entry point** — the thing the client double-clicks — and configures *how* the Chromium browser engine (Google Chrome, Microsoft Edge or Brave) opens your web app on that specific machine.

In plain words:

> Your web app lives on a server. KioskForge Pro builds the branded "door" that the client clicks to walk into that web app — locked to full screen, printing without pop-ups, hiding the address bar, surviving power cuts, and reconnecting itself automatically.

Everything is generated locally on your development machine. No account, no cloud service, no telemetry, no internet dependency for the builder itself.

---

## 2. Who Is It For?

| User | How they use KioskForge Pro |
|---|---|
| **Software house / freelancer** | Deliver a professional Windows launcher instead of telling the client "open Chrome and paste this URL". |
| **POS / retail vendor** | Silent thermal-receipt printing terminals that never show a print dialog. |
| **Hospital / clinic IT** | Token queue display screens, reception counters, pharmacy terminals. |
| **School / college IT** | Fee counters, attendance kiosks, parent self-service terminals. |
| **System integrator** | Pre-configured terminals for local intranet apps with self-signed HTTPS certificates. |
| **Support engineer** | Ship an "Emergency Close" utility and a branded offline screen to reduce support calls. |
| **Agency building multiple clients** | Compile dozens of client launchers in one batch run. |

---

## 3. Problems It Solves

| Real-world problem | How KioskForge Pro solves it |
|---|---|
| Client keeps closing the app, opening new tabs, or browsing away | `--kiosk` mode with no address bar, tabs or window controls |
| "Print" shows a preview dialog at the POS counter and the cashier gets confused | `--kiosk-printing` prints instantly to the Windows default printer |
| Kiosk flags stop working because Chrome is already open on the PC | A dedicated isolated browser profile per client (`--user-data-dir`) |
| Client makes an honest mistake and hits the "no internet" dinosaur page on boot | Pre-launch connectivity guard with configurable retries |
| Server is down and the client panics | Branded offline screen with your support number that retries every 5 seconds |
| App opens with an ugly default Chrome icon | Custom `.ico` / PNG / JPG logo embedded into the `.exe` |
| Windows shows `chrome.exe` as publisher in Task Manager | Real Company / Product / Version / Copyright metadata embedded into the `.exe` |
| Client keeps an old cached version of the app after you deploy an update | Optional disk-cache purge before each launch |
| Shared shift terminal keeps the previous user logged in | Optional cookie / session wipe after the kiosk closes |
| Local server uses a self-signed certificate and Chrome blocks it | Optional certificate-warning bypass for intranet deployments |
| Client double-clicks the icon twice and two copies fight each other | Optional "close previous instance of this app" before launching |
| Client cannot find the program | Generated desktop-shortcut creator |
| Client forgets to open the app in the morning | Generated auto-start installer for Windows boot |
| A kiosk gets stuck full screen and nobody can exit it | Generated emergency close/reset utility |
| Delivering 20 files by email is messy | One ZIP with all launchers plus a formatted client instruction sheet |

---

## 4. Feature Matrix at a Glance

| Area | Highlights |
|---|---|
| **Client profile database** | Save / load / delete named profiles, import & export JSON, keys stored as `Client - App` |
| **Deployment presets** | 5 one-click presets (POS terminal, standalone desktop app, locked public kiosk, queue display, self-signed intranet) |
| **Launch modes** | Full kiosk, standalone app window, standard browser window |
| **Browser targeting** | Auto fallback chain Chrome → Edge → Brave, or force one engine |
| **12 runtime switches** | Silent printing, isolated profile, incognito, pinch lock, swipe-nav lock, first-run suppression, dialog suppression, autoplay, translate suppression, extension blocking, start maximized, start fullscreen |
| **Advanced browser control** | Custom profile folder, UI scale factor, custom window size/position, free-form extra CLI flags |
| **Deliverables** | Portable single-file `.exe`, `.bat`, `.cmd`, silent `.vbs`, desktop-shortcut creator, auto-start installer, emergency close tool, delivery ZIP |
| **Network guard** | Reachability pre-check, 1–20 retries at 2-second intervals, branded offline fallback page with support contact |
| **Session hygiene** | Cache purge on launch, cookie/storage wipe on exit, incognito mode, optional proxy, optional user-agent override |
| **EXE branding** | Company, product, description, 4-part version, copyright, custom icon (multi-resolution ICO), optional UAC elevation |
| **Live preview** | See the exact browser command, `.bat` script, embedded Python source and `.vbs` wrapper before building; copy to clipboard |
| **Diagnostics** | Dependency badge (PyInstaller + Pillow), one-click pip installer, browser audit, timestamped build log |
| **Batch build** | Multi-select saved profiles and compile all of them sequentially in one run |
| **UX** | Auto-maximised window, F11 fullscreen, tooltips on nearly every control, live filename/folder synchronisation, threaded builds that never freeze the UI |

---

## 5. System Requirements

### Builder machine (your PC)

| Requirement | Detail |
|---|---|
| **Operating system** | Windows 10 / 11 (recommended). The UI is Tkinter-based, but the expected deliverables and helper scripts are Windows targets. |
| **Python** | Python 3.8+ with the standard `tkinter` module (included in the official Windows installer). |
| **PyInstaller** | Required only if you want to compile the `.exe`. Installable from inside the app. |
| **Pillow** | Required only for automatic PNG/JPG/BMP/WEBP → ICO icon conversion. Installable from inside the app. |
| **Chromium browser** | At least one of Google Chrome, Microsoft Edge or Brave installed for **Test Launch** and browser auditing. |
| **Disk / RAM** | PyInstaller compilation is the heaviest step; allow a few hundred MB of temporary space. |

### Client machine (the recipient)

| Requirement | Detail |
|---|---|
| **Windows** | Windows 10 or 11 |
| **Browser** | Chrome, Edge or Brave installed (Edge ships with Windows) |
| **Network** | Access to the URL you configured (internet or the same LAN) |
| **Nothing else** | The generated `.exe` is a single portable file. No Python, no installer, no admin rights needed unless you deliberately enable UAC elevation. |

---

## 6. Installation

1. **Get the project files.**
   ```text
   app.py
   kiosk_clients.json      (optional sample profile export)
   ```
2. **Verify Python.**
   ```powershell
   python --version
   ```
3. **Run KioskForge Pro.**
   ```powershell
   python app.py
   ```
   The window opens maximised with the title `KioskForge Pro - Enterprise Client Web App & Portable EXE Builder v2.4.0`.

4. **Install the build tools** (first time only).
   Click **Install Build Tools** in the top-right corner. The app runs:
   ```text
   python -m pip install --upgrade pyinstaller pillow
   ```
   Output streams live into the **Build Log & Diagnostics** tab. When it finishes, the badge changes to `Build Engine Ready (PyInstaller + Pillow)` in green and the button disables itself.

> You can also install manually:
> ```powershell
> pip install --upgrade pyinstaller pillow
> ```

5. *(Optional)* Build your own distribution `.exe` of the tool itself:
   ```powershell
   pyinstaller --onefile --noconsole --name KioskForgePro app.py
   ```

---

## 7. First Launch & Interface Map

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│  TOP BAR     KioskForge Pro                                    [Tool Status] │
│              Enterprise Client Web App Launcher...   [Install] [Fullscreen] │
├──────────────────────────────────────────────────────────────────────────────┤
│  TOOLBAR   Client Profile: [ ▾ ] Load | Save | Delete      Deployment: [▾]  │
│            Import JSON | Export JSON                                        │
├────────────────────────────────┬─────────────────────────────────────────────┤
│  LEFT INSPECTOR (scrollable)    │  RIGHT WORKSPACE                            │
│                                │                                             │
│  1. Client Identity & Target   │  ┌ Code & Script Preview ──────────────┐   │
│     Web Application            │  │ Network & Offline Guard             │   │
│     • Client / Organization    │  │ EXE Metadata & Security             │   │
│     • Web App Title            │  │ Multi-Client Batch Build            │   │
│     • Web Application URL      │  │ Build Log & Diagnostics             │   │
│     • Target Browser Engine    │  │                                     │   │
│     • Launcher Icon            │  │   (tab content area)                │   │
│     • Output Base Filename     │  │                                     │   │
│     • Deliverables Folder      │  │                                     │   │
│                                │  └─────────────────────────────────────┘   │
│  2. Window Mode & Kiosk        │  [Test Launch] [Open Folder] [ BUILD ▶ ]   │
│     Attributes                 │                                             │
│                                │                                             │
│  3. Deliverable Formats &      │                                             │
│     Runtime Behaviour          │                                             │
└────────────────────────────────┴─────────────────────────────────────────────┘
```

**Global controls**

| Control | Behaviour |
|---|---|
| Window | Automatically maximised on start |
| `F11` | Toggle borderless fullscreen |
| `Esc` | Exit fullscreen |
| Mouse wheel over the left panel | Scrolls the inspector |
| Hover over any control | Tooltip appears after ~350 ms explaining exactly what it does |

---

## 8. End-to-End Quick Start (5 Minutes)

1. Click **Install Build Tools** (first run only) and wait for the green **Build Engine Ready** badge.
2. In **Client / Organization** type the client's business name, e.g. `Al-Falah Medical Center`.
3. In **Web App Title** type the product name, e.g. `Hospital Management Portal`.
   → The **Output Base Filename**, **Isolated Profile Folder** and **EXE Product Name** fill themselves automatically (`Hospital_Management_Portal_Launcher`, `Hospital_Management_Portal_Profile`, `Hospital Management Portal Kiosk`).
4. In **Web Application URL** paste the address, e.g. `https://hms.yourclient.com`.
5. Choose a **Deployment Preset** — for a reception/hospital counter choose `POS & Thermal Receipt Terminal`; for an office desktop app choose `Standalone Desktop Web App (--app)`.
6. *(Optional)* **Browse** for a logo in **Launcher Icon**.
7. **Browse** a **Deliverables Folder** (defaults to `Desktop\Client_Kiosk_Deliverables`).
8. Open the **Network & Offline Guard** tab and set **Support Contact** to your phone/email shown on the offline screen.
9. Open the **EXE Metadata & Security** tab and fill Company, Product, Description and Version.
10. Press **Test Launch on This PC** to confirm the app opens exactly as the client will see it.
11. Press **Build & Package Client Launcher(s)**.
12. When the log says `Build completed cleanly!`, click **Open Output Folder** and send the ZIP to the client.

---

## 9. Module Reference

### 9.1 Top Bar — Build Engine Status

| Element | Purpose | Details |
|---|---|---|
| **KioskForge Pro** title + subtitle | Branding | — |
| **Status badge** | Live dependency health | Green `Build Engine Ready (PyInstaller + Pillow)` when both are importable; amber `Missing: PyInstaller`, `Missing: Pillow`, or `Missing: PyInstaller, Pillow` otherwise |
| **Install Build Tools** | One-click dependency install | Runs pip in a background thread, streams every line into the log, then re-checks status. Disabled and relabelled `Tools Installed` when ready. |
| **Fullscreen (F11)** | Presentation mode | Toggles a borderless fullscreen window; button label switches to `Exit Fullscreen (F11)` |

Behaviour notes:
- If PyInstaller is missing, the `.exe` build is **blocked** with an explanatory dialog — but `.bat` / `.cmd` builds still work.
- If Pillow is missing, the build still succeeds; the icon is simply skipped (with a log line).

---

### 9.2 Toolbar — Client Profile Manager

Every configuration you build can be stored as a **named profile**. Profiles live in `kiosk_clients_db.json` next to `app.py`. The profile key is always `"{Client / Organization} - "{Web App Title}"`.

| Button | What it does | Important behaviour |
|---|---|---|
| **Client Profile** dropdown | Read-only list of saved profiles, alphabetical | Newly saved profiles appear immediately |
| **Load** | Applies the selected profile to every field on screen | Icon thumbnail refreshes too |
| **Save Profile** | Writes the current screen state into the database | Saving with the same client + app name **overwrites** the existing profile |
| **Delete** | Removes the selected profile permanently | No confirmation dialog — export a backup first if unsure |
| **Import JSON** | Loads a profile dictionary from an external file | **Merges**: same-named keys are replaced, other profiles are kept |
| **Export JSON** | Saves the entire profile database to a file | Use before reinstalling Windows or moving to another PC |

**What a saved profile stores (complete list)**

Client identity: `client_name`, `app_name`, `url`, `output_name`, `output_dir`, `icon_path`, `browser_target`

Launch behaviour: `launch_mode`, `kiosk_printing`, `isolated_profile`, `profile_folder`, `incognito`, `disable_pinch`, `disable_swipe_nav`, `no_first_run`, `suppress_dialogs`, `autoplay_media`, `disable_translate`, `start_maximized`, `start_fullscreen`, `disable_extensions`, `custom_geometry`, `win_width`, `win_height`, `win_x`, `win_y`, `scale_factor`, `extra_flags`, `kill_existing`

Network: `health_check`, `health_retries`, `offline_fallback`, `support_phone`, `ignore_cert_errors`, `clear_cache_on_launch`, `clear_session_on_exit`, `proxy_server`, `user_agent`

EXE metadata: `exe_company`, `exe_product`, `exe_desc`, `exe_version`, `exe_copyright`, `uac_admin`

Deliverables: `gen_exe`, `gen_bat`, `gen_cmd`, `gen_vbs`, `gen_shortcut_helper`, `add_startup_helper`, `add_kill_helper`, `gen_zip`

---

### 9.3 Toolbar — Deployment Presets

Choosing a preset instantly applies a tested combination of window mode and browser switches. Presets **do not** touch the client name, app name, URL, icon, output paths, network settings, EXE metadata or deliverable checkboxes — those remain yours to configure.

| Preset | Mode | What it configures | Best for |
|---|---|---|---|
| **POS & Thermal Receipt Terminal** | Full kiosk | Silent printing ON, isolated profile ON, pinch & swipe-lock ON, first-run & dialog suppression ON, autoplay ON, translate OFF, extensions blocked, scale `1.0`, extra flags `--disable-print-preview --disable-features=PrintCompositorLPAC` | Cash counters, pharmacy billing, token receipts |
| **Standalone Desktop Web App (--app)** | App window (`.exe`-like window with title bar, no URL bar) | Silent printing OFF, isolated profile ON, start maximised ON, extensions allowed, no extra flags | Office desktops, back-office admin panels |
| **Locked Public Self-Service Kiosk** | Full kiosk | Incognito ON, cache purge on launch ON, session wipe on exit ON, autoplay OFF, extensions blocked, extra flags `--disable-background-networking --disable-sync` | Walk-in self-service terminals, shared patient/parent kiosks |
| **Hospital / School Queue Display Screen** | Full kiosk | Autoplay ON, isolated profile ON, scale `1.1`, extra flag `--disable-gpu-vsync` | Waiting-area token/queue display TVs |
| **Local Intranet / Self-Signed HTTPS App** | App window | Silent printing ON, isolated profile ON, start maximised ON, **ignore certificate errors** ON, extensions blocked, extra flag `--allow-insecure-localhost` | LAN servers with self-signed certificates |

Selecting a preset also writes a log line `Applied preset profile: <name>` so the build log shows which baseline you started from. You may freely change any individual checkbox afterwards.

---

### 9.4 Card 1 — Client Identity & Target Web Application

| Field | Purpose | Notes |
|---|---|---|
| **Client / Organization** | The business receiving the launcher | Used in the delivery README, offline screen and profile key |
| **Web App Title** | Your product's display name | Auto-fills the output filename, profile folder and EXE product name while you type |
| **Web Application URL** | The address the launcher opens | If you omit the scheme, `https://` is added automatically. Accepts `http://`, `https://` and `file://` |
| **Target Browser Engine** | Which browser to use | `Auto (Chrome → Edge → Brave)` tries Chrome first, then Edge (pre-installed on Windows), then Brave. The other options force a single engine. |
| **Launcher Icon** | Brand logo | Accepts `.ico`, `.png`, `.jpg`, `.jpeg`, `.bmp`, `.webp`. A live thumbnail previews it. Non-ICO images are converted into a multi-resolution Windows ICO (256/128/64/48/32/16 px) using Pillow. |
| **Output Base Filename** | Root name of every generated file | Auto-generated but fully editable. Illegal characters become underscores |
| **Deliverables Folder** | Where files are written | Defaults to `%USERPROFILE%\Desktop\Client_Kiosk_Deliverables`; created automatically if missing |

**Auto-synchronisation rule:** typing in *Web App Title* regenerates `Output Base Filename` → `<Title>_Launcher`, `Isolated Profile Folder` → `<Title>_Profile`, AND `EXE Product Name` → `<Title> Kiosk`. Editing those fields afterwards is allowed and will not be overwritten unless you type in *Web App Title* again.

---

### 9.5 Card 2 — Window Mode & Chromium Kiosk Attributes

#### Launch modes

| Option | Generated switch | What the client sees | When to use |
|---|---|---|---|
| **Full Kiosk** | `--kiosk` | Borderless fullscreen, no address bar, no tabs, no window buttons, no right-click menus | POS counters, public terminals, queue displays |
| **Standalone App Window** | `--app=<url>` | Clean native-looking window with title bar and minimise/close buttons, but no URL bar or tabs | Office staff who still need to close the window normally |
| **Standard Browser Window** | *(no mode switch)* | A normal Chrome/Edge window at your URL, but with all your other flags applied | Internal testing, or when the client's IT insists on a normal browser |

> In kiosk mode the URL is passed as a separate argument; in app mode the URL is embedded inside `--app=`; in standard mode the URL is passed as a plain argument.

#### The 12 runtime switches

| UI label | Generated flag(s) | What it does | Turn it on when |
|---|---|---|---|
| **Silent POS Printing** | `--kiosk-printing` | Prints immediately to the Windows default printer, skipping the Chrome print-preview dialog | Thermal receipt printers, token slips |
| **Isolated App Profile** | `--user-data-dir=%LOCALAPPDATA%\WebAppKiosks\<folder>` | Gives this client a private browser data folder so kiosk flags work even if normal Chrome is already open | Almost always; required for cache/session hygiene and "close previous instance" |
| **Incognito / Ephemeral Mode** | `--incognito` | Nothing (cookies, history, form data) is kept between runs | Public walk-in kiosks |
| **Disable Touch Pinch-Zoom** | `--disable-pinch` | Stops accidental zooming on touchscreens | Touch POS monitors, kiosk panels |
| **Disable Swipe Back/Forward Navigation** | `--overscroll-history-navigation=0` | Blocks two-finger/edge swipes from navigating away from your app | Touchpads, touchscreens |
| **Skip First-Run & Default Browser Prompts** | `--no-first-run --no-default-browser-check` | Removes "Welcome to Chrome" and "Set as default browser" pop-ups on a fresh profile | Every deployment |
| **Suppress Crash & Restore Bubbles** | `--noerrdialogs --disable-session-crashed-bubble --disable-infobars` | Hides "Chrome didn't shut down correctly — Restore pages?" and infobars after a power cut | Unattended kiosks |
| **Allow Sound & Alert Autoplay** | `--autoplay-policy=no-user-gesture-required` | Notification chimes and voice announcements play without a click | Queue/token calling systems |
| **Disable Translate Page Popup** | `--disable-features=Translate` | Stops the Google Translate bar appearing on Urdu/local-language UIs | Multilingual deployments |
| **Disable All Browser Extensions** | `--disable-extensions` | Prevents adblockers or extensions from breaking your scripts | Controlled environments |
| **Start Maximized** | `--start-maximized` | App window fills the desktop work area on launch | Desktop-app style deployments |
| **Start Fullscreen** | `--start-fullscreen` | Starts in F11-style fullscreen but still allows F11 to exit | Presentations, dashboards |

#### Advanced browser control

| Control | Generated flag | Notes |
|---|---|---|
| **Isolated Profile Folder** | `--user-data-dir=...\WebAppKiosks\<folder>` | Subfolder name under `%LOCALAPPDATA%\WebAppKiosks\`. Auto-derived from the app title, editable, sanitised |
| **UI Scale** | `--force-device-scale-factor=<value>` | Choices `0.75, 0.85, 0.9, 1.0, 1.1, 1.25, 1.5`. Only emitted when value ≠ `1.0`. Useful for high-DPI laptops or compact POS panels |
| **Custom Window Bounds** | `--window-size=W,H` and `--window-position=X,Y` | Only applied when checked; non-numeric values are ignored |
| **Custom CLI Flags** | Appended verbatim | Space-separated. Example `--disable-print-preview --ash-no-nudges`. Values containing spaces can break argument parsing — keep flag values space-free |

---

### 9.6 Card 3 — Deliverable Formats & Runtime Behaviour

| Checkbox | Produces | What it is | When to hand it over |
|---|---|---|---|
| **Portable Single-File .EXE (PyInstaller)** | `<base>.exe` | One self-contained no-console Windows executable with your icon and metadata | Primary hand-over file — nothing to install |
| **Windows Batch Script (.bat)** | `<base>.bat` | Small plain-text launcher that finds the browser itself | Zero-dependency fallback, easy for IT to inspect/edit |
| **Windows Command Script (.cmd)** | `<base>.cmd` | Same content as the `.bat`, different extension for enterprise environments | When group policy blocks `.bat` but allows `.cmd` |
| **Silent VBScript Launcher (.vbs)** | `<base>_Silent.vbs` | Runs the `.bat` with window style `0`, so no black console window flashes | Clients who find the console flash unprofessional |
| **Desktop Shortcut Creator (.bat)** | `Create_<base>_Desktop_Shortcut.bat` | Creates a real Windows `.lnk` on the desktop via `WScript.Shell` | One-time convenience step for the client |
| **Windows Auto-Start Installer (.bat)** | `Install_<base>_AutoStart.bat` | Copies the primary launcher into the user's Startup folder | Terminals that must open by themselves every morning |
| **Emergency Kiosk Exit/Reset Tool (.bat)** | `Close_<base>_Kiosk.bat` | Force-closes only processes belonging to this app's profile, leaving normal Chrome alone | Support engineers, stuck kiosks |
| **Bundle Client Delivery .ZIP + Guide** | `<base>_Client_Deliverable.zip` | All generated files plus `README_Client_Instructions.txt` | The single file you email/WhatsApp to the client |
| **Close Previous Instance of This App Before Launching** | Runtime logic (not a file) | Terminates earlier instances of this same profile before opening | Prevents duplicate windows when the client double-clicks repeatedly |

**Important relationships**
- If `.vbs` is selected, the `.bat` is **always written** because the VBS wrapper calls it — but the `.bat` is only *listed/counted* if the `.bat` box is also checked.
- The desktop-shortcut helper and auto-start installer target the **primary** file: the `.exe` if built, otherwise the first generated script.
- The ZIP contains only the files listed as deliverables, plus the instruction sheet.
- At least one of `.exe`, `.bat`, `.cmd` must be selected or the build is refused with *"Select at least one primary launcher format"*.

---

### 9.7 Tab — Code & Script Preview

A live, read-only-in-spirit inspector for exactly what will be produced. It regenerates instantly as you change any identity, launch-mode, display or network option.

| View | Shows |
|---|---|
| **CLI Command** | `chrome.exe` followed by the complete computed switch list — the single best way to verify flags before building |
| **Windows Batch (.bat / .cmd)** | The full script: title, browser search chain, missing-browser message, kill-previous block, profile creation, optional cache purge, optional connectivity loop with labels `:CHECK_NET` / `:LAUNCH_APP`, and the final `start "" "%BROWSER_EXE%" ...` |
| **Portable EXE Python Source** | The complete embedded Python program that becomes the `.exe`: constants, `find_browser()`, `is_url_reachable()`, `kill_previous_instances()`, `clean_profile_cache()`, `clean_profile_session()`, `main()` |
| **Silent VBScript (.vbs)** | The wrapper that resolves its own folder, checks the `.bat` exists, and launches it hidden — otherwise shows a *"Missing launcher script"* message box |

**Copy Code** puts the currently displayed text on the clipboard (and logs the action) so you can paste it into a ticket, a client email, or your own notes.

---

### 9.8 Tab — Network & Offline Guard

| Control | Effect | Notes |
|---|---|---|
| **Verify Server / Internet Reachability Before Launching Browser** | Enables the pre-launch reachability loop | Skipped automatically for `file://` targets |
| **Connection Retry Attempts (2s interval)** | 1–20 attempts | Each attempt has a 3-second request timeout, then a 2-second pause |
| **Show Branded Offline / Auto-Reconnect Screen if Unreachable** | Uses the built-in fallback page instead of the browser's error page | **EXE only.** The `.bat`/`.cmd` scripts retry and then launch the URL anyway |
| **Support Contact on Offline Screen** | Your phone or email, displayed on the offline page | Default `+92-336-1593533` |
| **Ignore Self-Signed SSL Certificate Warnings** | `--ignore-certificate-errors` | Only for trusted local intranet servers |
| **Purge Browser Disk Cache Before Each Launch** | Deletes `Default\Cache`, `Default\Code Cache` (and `GPUCache` in the EXE) before opening | Guarantees the client loads your newest deployed assets |
| **Wipe Cookies & Login Session After Kiosk Closes** | Deletes `Cookies`, `Cookies-journal`, `Session Storage`, `Local Storage` after the process exits | Shared shift terminals. **EXE runtime only**; requires an isolated profile |
| **Custom Proxy Server** | `--proxy-server=<value>` | e.g. `http://192.168.1.1:8080` or `socks5://127.0.0.1:1080`. Blank = direct connection |
| **Custom User-Agent** | `--user-agent="<value>"` | Only if your backend inspects the user agent |

---

### 9.9 Tab — EXE Metadata & Security

These values are baked into the compiled executable and appear in **Windows File Properties → Details**, Task Manager, and Explorer tooltips.

| Field | Meaning | Example |
|---|---|---|
| **Company / Studio Name** | Publisher | `Bannu Software Solutions (SSTS)` |
| **Product Name** | Product title | `Hospital Management Portal Kiosk` |
| **File Description** | Tooltip / Task Manager description | `Dedicated Desktop Kiosk Client Launcher` |
| **File & Product Version** | Four-part version; non-digits are extracted and padded with zeros | `1.0.0.0` |
| **Copyright Notice** | Legal string | `Copyright (c) 2026 Bannu Software Solutions` |
| **Request Administrator Elevation (--uac-admin)** | Adds a UAC manifest so the `.exe` asks for admin rights | Keep **off** for normal user accounts |

The generated `version_info.txt` writes `CompanyName`, `FileDescription`, `FileVersion`, `InternalName`, `LegalCopyright`, `OriginalFilename`, `ProductName`, `ProductVersion`, and a `1033 / 1200` translation entry. Apostrophes are stripped automatically so the resource file stays valid.

---

### 9.10 Tab — Multi-Client Batch Build

Compile many saved profiles in one supervised run.

1. Select one or more profiles in the list (Ctrl/Shift click works — the list is multi-select).
2. Use **Select All** or **Clear Selection** for speed.
3. Press **Compile Selected Client Profiles**.
4. The builder switches to the log tab and processes profiles alphabetically, logging `[1/5] Loading profile: ...` before each one.
5. Each profile is built with **its own stored output folder** and its own deliverable choices.
6. A single summary dialog appears at the end: *"Successfully compiled N client launcher packages!"*
7. If one profile fails, the error is logged and the run continues with the remaining profiles.

The main **Build & Package** button is disabled during a batch run to prevent overlapping builds; batch builds suppress individual success pop-ups so you get one clean summary.

**Preparation checklist before a batch run:** every selected profile must have a valid URL, an existing output folder (created automatically), and — if `.exe` is enabled — PyInstaller must be installed.

---

### 9.11 Tab — Build Log & Diagnostics

| Element | Purpose |
|---|---|
| **Local Browser Engine Audit & Build Console** header | Section title |
| **Re-Scan Browsers** | Re-runs the audit and logs every found browser path, or a warning if none were found in the standard directories |
| **Clear Log** | Empties the console |
| **Log area** | Timestamped `[HH:MM:SS]` lines for every action: preset changes, profile loads/saves/deletes, imports/exports, clipboard copies, dependency installs, build steps, PyInstaller `INFO:/WARNING:/ERROR:` lines, and errors |

The audit at startup checks these standard locations (expanded with environment variables):

```text
%ProgramFiles%\Google\Chrome\Application\chrome.exe
%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe
%LocalAppData%\Google\Chrome\Application\chrome.exe
%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe
%ProgramFiles%\Microsoft\Edge\Application\msedge.exe
%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe
%ProgramFiles(x86)%\BraveSoftware\Brave-Browser\Application\brave.exe
%LocalAppData%\BraveSoftware\Brave-Browser\Application\brave.exe
```

> The audit reflects **your** PC, not the client's. The generated launchers perform their own search on the client machine at runtime.

---

### 9.12 Action Bar — Test, Open Folder, Build

| Button | Behaviour |
|---|---|
| **Test Launch on This PC** | Finds the selected browser locally and launches it with the exact computed flags, logging the browser and URL. Uses the real profile path under `%LOCALAPPDATA%\WebAppKiosks\<folder>`. Does not generate any files. |
| **Open Output Folder** | Opens the deliverables folder in Explorer; if it does not exist yet, shows *"Generate a launcher first or choose an existing output directory."* |
| **Build & Package Client Launcher(s)** | Validates the selection, checks PyInstaller if `.exe` is requested, disables itself, switches to the log tab, and starts the build thread. Label changes to `Compiling Deliverables...` while running. |

---

## 10. The Build Pipeline — Exact Order of Operations

```text
1. VALIDATE
   • is a build already running?  → stop
   • is at least one of .exe / .bat / .cmd selected? → else warn & stop
   • if .exe selected, is PyInstaller available? → else error & stop

2. PREPARE
   • create the deliverables folder if missing
   • sanitise the base filename (illegal characters → underscore,
     empty result falls back to "Client_WebApp")
   • log the client / app being built

3. WRITE SCRIPTS
   • <base>.bat   (always if .bat OR .vbs is selected)
   • <base>.cmd   (if .cmd selected)
   • <base>_Silent.vbs (if .vbs selected)

4. COMPILE EXE (only if .exe selected)
   • create a temp workspace (kioskforge_*)
   • write the embedded Python stub
   • convert the icon to multi-resolution .ico (if provided)
   • write version_info.txt from the metadata fields
   • run:  python -m PyInstaller --noconfirm --onefile --noconsole --clean
           --distpath ... --workpath ... --specpath ...
           --version-file ... --name <base>
           [--icon ...] [--uac-admin] <stub>.py
   • copy dist\<base>.exe into the deliverables folder
   • the EXE becomes the primary file for helpers

5. WRITE HELPERS
   • Create_<base>_Desktop_Shortcut.bat
   • Install_<base>_AutoStart.bat
   • Close_<base>_Kiosk.bat

6. PACKAGE
   • <base>_Client_Deliverable.zip containing every generated file
     + README_Client_Instructions.txt

7. CLEAN UP
   • delete the temporary workspace
   • re-enable the build button
   • show "Build Successful" with the number of files and the folder

On failure: log "BUILD ERROR: <reason>", show a "Build Failed" dialog,
still clean the temp folder and re-enable the button.
```

---

## 11. Generated Files Reference

Assuming **Client** = `Al-Falah Medical Center`, **Title** = `Hospital Management Portal`, so base = `Hospital_Management_Portal_Launcher`:

| File | Type | Purpose |
|---|---|---|
| `Hospital_Management_Portal_Launcher.exe` | Portable executable | Double-click launcher; no Python needed |
| `Hospital_Management_Portal_Launcher.bat` | Batch script | Browser-finding launcher with health check |
| `Hospital_Management_Portal_Launcher.cmd` | Command script | Same content, `.cmd` extension |
| `Hospital_Management_Portal_Launcher_Silent.vbs` | VBScript | Launches the `.bat` with no console flash |
| `Create_Hospital_Management_Portal_Launcher_Desktop_Shortcut.bat` | Helper | Creates a desktop `.lnk` with the app title |
| `Install_Hospital_Management_Portal_Launcher_AutoStart.bat` | Helper | Copies the primary launcher into the Startup folder |
| `Close_Hospital_Management_Portal_Launcher_Kiosk.bat` | Helper | Force-closes this app's kiosk processes only |
| `Hospital_Management_Portal_Launcher_Client_Deliverable.zip` | Archive | Everything above + instruction sheet |
| `README_Client_Instructions.txt` *(inside the ZIP)* | Text guide | Client name, app URL, display mode, support desk, file list, 5-step deployment guide |

**Inside `README_Client_Instructions.txt`:** the app name, client name, URL, upper-case mode, support number, the exact list of files, and these steps — extract to a permanent folder, double-click the `.exe` (or `.bat`), optionally run the shortcut creator, optionally run the auto-start installer, press `Alt + F4` to leave full kiosk mode.

---

## 12. Runtime Behaviour of the Generated Launchers

### 12.1 The compiled `.exe`

```text
 1. Locate a browser
    Try each candidate path for the selected engine(s) in order.
    If none exists → Windows message box:
      "<App> - Browser Missing
       Google Chrome or Microsoft Edge was not found on this computer.
       Please install Google Chrome to launch <App>."
    then exit with code 1.

 2. Create the profile folder
    %LOCALAPPDATA%\WebAppKiosks\<ProfileFolder>   (created if missing)

 3. Optional: close previous instance
    PowerShell enumerates Win32_Process and stops any process whose
    command line contains this profile folder name.

 4. Optional: purge cache
    Delete <profile>\Default\Cache, Default\Code Cache, Default\GPUCache

 5. Optional: connectivity guard
    For up to N attempts (3-second timeout each, 2-second pause):
      request the target URL (certificate verification disabled)
    If still unreachable AND the offline screen is enabled:
      write offline_guard.html into the profile folder
      launch that local file instead of the real URL
    Otherwise launch the real URL anyway.

 6. Launch
    Start the browser with the computed arguments.
    In app mode the fallback URL is substituted inside --app=...

 7. Optional: session wipe
    Wait for the browser process to exit, then delete
    Cookies, Cookies-journal, Session Storage, Local Storage.
    (Requires the isolated profile option.)
```

Note: the PowerShell helper processes are started with the hidden console flag, so the user sees no black windows.

### 12.2 The `.bat` / `.cmd` launcher

1. Sets the window title to the app name.
2. Probes each candidate browser path; the first `if exist` hit wins.
3. If nothing is found: echoes *"Google Chrome or Microsoft Edge was not found on this computer."*, pauses, exits with code 1.
4. *(If enabled)* kills previous instances of this profile via PowerShell.
5. Creates the profile folder and *(if enabled)* removes `Default\Cache` and `Default\Code Cache`.
6. *(If enabled)* runs the `:CHECK_NET` label: `Invoke-WebRequest` with a 3-second timeout; success jumps to `:LAUNCH_APP`; failure decrements the retry counter, waits 2 seconds, loops.
7. After the retries are exhausted it **falls through to `:LAUNCH_APP`** and starts the browser with the real URL.
8. `start "" "%BROWSER_EXE%" <flags> <url>` then exit 0.

### 12.3 The `.vbs` wrapper

Resolves its own directory, appends the `.bat` filename, and if the file exists runs it with `WshShell.Run ..., 0, False` (hidden, non-blocking). If the `.bat` is missing it shows a *"Missing launcher script"* error box.

---

## 13. The Branded Offline Guard Screen

When the EXE cannot reach your server after all retries, it writes and opens a self-contained HTML page — no internet needed to display it.

| Element | Content |
|---|---|
| Badge | `WAITING FOR NETWORK / SERVER` |
| Heading | Your **Web App Title** |
| Message | *"Unable to reach the application server right now. Check your internet or local network cable. This terminal will reconnect automatically."* |
| Terminal line | Your **Client / Organization** |
| Support line | Your **Support Contact** |
| Live status | `Retrying connection in Ns...`, decrementing every second |
| Button | **Reconnect Now** → navigates straight to the real URL |
| Auto behaviour | Every 5 seconds it attempts the real URL again, forever |

Styling is a clean light card layout (white card, slate text, blue primary button) matching the builder's design language, so it looks intentional rather than broken.

---

## 14. Data & Configuration Reference

**File:** `kiosk_clients_db.json` in the same directory as `app.py`.
**Created automatically** on first save. Human-readable indented JSON.

```json
{
  "Al-Falah Medical Center - Hospital Management Portal": {
    "client_name": "Al-Falah Medical Center",
    "app_name": "Hospital Management Portal",
    "url": "https://hms.yourclient.com",
    "output_name": "Hospital_Management_Portal_Launcher",
    "output_dir": "C:\\Users\\Yasin\\Desktop\\Client_Kiosk_Deliverables",
    "icon_path": "C:\\assets\\logo.png",
    "browser_target": "Auto (Chrome -> Edge -> Brave)",
    "launch_mode": "kiosk",
    "kiosk_printing": true,
    "isolated_profile": true,
    "profile_folder": "Hospital_Management_Portal_Profile",
    "incognito": false,
    "disable_pinch": true,
    "disable_swipe_nav": true,
    "no_first_run": true,
    "suppress_dialogs": true,
    "autoplay_media": true,
    "disable_translate": true,
    "start_maximized": false,
    "start_fullscreen": false,
    "disable_extensions": true,
    "custom_geometry": false,
    "win_width": "1366",
    "win_height": "768",
    "win_x": "0",
    "win_y": "0",
    "scale_factor": "1.0",
    "extra_flags": "--disable-print-preview",
    "health_check": true,
    "health_retries": "3",
    "offline_fallback": true,
    "support_phone": "+92-336-1593533",
    "ignore_cert_errors": false,
    "clear_cache_on_launch": false,
    "clear_session_on_exit": false,
    "proxy_server": "",
    "user_agent": "",
    "exe_company": "Bannu Software Solutions (SSTS)",
    "exe_product": "Hospital Management Portal Kiosk",
    "exe_desc": "Dedicated Desktop Kiosk Client Launcher",
    "exe_version": "1.0.0.0",
    "exe_copyright": "Copyright (c) 2026 Bannu Software Solutions",
    "uac_admin": false,
    "gen_exe": true,
    "gen_bat": true,
    "gen_cmd": false,
    "gen_vbs": true,
    "gen_shortcut_helper": true,
    "add_startup_helper": true,
    "add_kill_helper": true,
    "gen_zip": true,
    "kill_existing": true
  }
}
```

**Client-side state** lives in `%LOCALAPPDATA%\WebAppKiosks\<ProfileFolder>\`:

| Path | Contents |
|---|---|
| `Default\` | Cookies, local storage, IndexedDB, cached assets, extension state for this app |
| `offline_guard.html` | Generated fallback page (EXE mode only) |

The sample file `kiosk_clients.json` shipped in the repository is an example profile export — use **Import JSON** to load it.

---

## 15. Import, Export & Backup

| Action | Behaviour | Safety note |
|---|---|---|
| **Export JSON** | Writes the entire profile database (indented) to a file you choose | Do this before reinstalling Windows, before a batch of deletions, and weekly if the database matters |
| **Import JSON** | Reads a dictionary and merges it into the current database | Same-named profiles are **overwritten**; the merge is not undoable |
| **Save Profile** | Upserts one profile | Overwrites silently if the client + app name already exist |

Recommended routine: keep `kiosk_clients_db.json` in version control (it is small, plain text, and contains no passwords) and export a dated copy (`profiles_2026-11-19.json`) before big changes.

> The database contains URLs, paths and branding text only. No credentials are stored by KioskForge Pro.

---

## 16. Common Workflows

### 16.1 First delivery for a new client (recommended default)

1. New profile → client name, app title, URL.
2. Preset: `Standalone Desktop Web App (--app)`, or `POS & Thermal Receipt Terminal` for counters.
3. Icon: their logo.
4. Network tab: health check ON, retries `3`, offline screen ON, your support number.
5. Metadata tab: company, product, description, version `1.0.0.0`, copyright.
6. Deliverables: `.exe`, `.bat`, `.vbs`, shortcut helper, auto-start installer, close utility, ZIP.
7. Test Launch → Build → zip the deliverables → send.

### 16.2 POS / pharmacy counter with thermal printing

1. Preset `POS & Thermal Receipt Terminal`.
2. Confirm **Silent POS Printing** is checked and the Windows default printer is the receipt printer.
3. Keep **Isolated App Profile**, pinch and swipe locks on.
4. UI scale `1.0` (or `0.9` on small panels).
5. Build; hand over the `.exe` plus `Close_<base>_Kiosk.bat` for emergencies.

### 16.3 Public self-service kiosk

1. Preset `Locked Public Self-Service Kiosk`.
2. Confirm **Incognito**, **Purge cache before launch**, **Wipe cookies after close** are all ON.
3. Offline screen ON with a support number.
4. Auto-start installer included so the terminal recovers after a power cut.
5. Test on the actual touchscreen for pinch/zoom behaviour.

### 16.4 Local intranet app with a self-signed certificate

1. Preset `Local Intranet / Self-Signed HTTPS App`.
2. Set the URL to the LAN address, e.g. `https://192.168.1.50`.
3. Keep **Ignore self-signed SSL certificate warnings** ON — only on trusted internal networks.
4. Health check ON so a temporarily down LAN server retries instead of showing a browser error.

### 16.5 Queue / token display TV

1. Preset `Hospital / School Queue Display Screen`.
2. Autoplay ON so voice/token audio plays without a click.
3. Start fullscreen ON if the browser window should not show a title bar.
4. Auto-start installer included; `Close_<base>_Kiosk.bat` for maintenance.

### 16.6 Pushing a web-app update to an existing client

1. Load the profile.
2. Tick **Purge browser disk cache before each launch** if the client must always see the new assets.
3. Bump the **File & Product Version** (`1.0.0.0` → `1.0.1.0`).
4. Build and deliver the new `.exe` (the URL and settings stay identical).

### 16.7 Delivering to many clients at once

1. Save a profile per client (each with its own output folder).
2. Open **Multi-Client Batch Build**, **Select All**, **Compile Selected Client Profiles**.
3. Collect each `<base>_Client_Deliverable.zip` from the respective folders.

---

## 17. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `Missing: PyInstaller` badge | PyInstaller not installed in this Python | Click **Install Build Tools**, or `pip install pyinstaller` |
| `.exe` build blocked with a dialog | Same as above | Install the tools, or uncheck `.exe` and ship `.bat` |
| Icon not embedded | Pillow missing, or the image cannot be read | Install Pillow; prefer a square PNG ≥ 256 px |
| Build Failed / PyInstaller error | Antivirus locking temp files, disk space, or a broken Python environment | Read the log, free disk space, retry, or build `.bat` only |
| "Browser Not Found" on Test Launch | No Chrome/Edge/Brave in the standard paths, or a forced engine is missing | Choose `Auto` or install the engine |
| Kiosk mode does nothing when the client already has Chrome open | Isolated profile is off | Enable **Isolated App Profile** |
| Print preview still appears | Silent printing off, or the client's default printer is a PDF/OneNote driver | Enable **Silent POS Printing**, set the receipt printer as Windows default |
| Client sees an old version of the app | Browser cache | Enable **Purge browser disk cache before each launch** |
| Offline screen never appears | `.bat` was used (fallback is EXE-only), or health check is off | Ship the `.exe`, enable health check + offline screen |
| Certificate warning still appears | Ignore-cert not enabled, or the warning is coming from your app, not Chrome | Enable it for trusted LAN only |
| Offline screen appears even though the server is up | The check is strict: any non-2xx response or a redirect issue can fail. Increase retries | Raise retries, verify the URL responds in a browser |
| Build button greyed out | A build or batch build is still running | Wait for `Build completed cleanly!` |
| Batch build skipped a profile | That profile had no URL / no output folder / missing PyInstaller | Fix the profile, rebuild it individually first |
| Profile disappeared | **Delete** has no confirmation step | Re-import from your exported JSON backup |
| Double-click opens two windows | Client double-clicked | Enable **Close Previous Instance of This App Before Launching** |
| Numbers/formatting look tiny on a 4K screen | DPI scaling | Set **UI Scale** to `1.1`–`1.5` |
| Window opens on the wrong monitor | Default positioning | Enable **Custom Window Bounds**, e.g. W `1920` H `1080` X `1920` Y `0` |

---

## 18. Best Practices

1. **Always Test Launch before Build.** It takes 5 seconds and catches 90% of mistakes.
2. **Use the Auto browser chain** unless a client contractually requires one engine.
3. **Never ship `.exe` without `.bat`.** The script is your fallback if antivirus quarantines an unsigned executable.
4. **Keep the isolated profile on.** It is the foundation of cache purge, session wipe and "close previous instance".
5. **Version every delivery.** Bump `x.y.z.w` and keep the ZIPs in dated folders.
6. **Put a real support number** on the offline screen — it is the client's only visible help during an outage.
7. **Export JSON weekly.** Delete has no undo.
8. **Document the base filename per client.** It is also the profile folder name; renaming it orphans the client's saved browser state.
9. **Do not enable "ignore certificate errors"** outside trusted intranets.
10. **Keep extensions blocked** for kiosks — adblockers break dashboards more often than people expect.
11. **Test on the actual hardware** (touchscreen, receipt printer, TV) before delivery.
12. **Include the emergency close utility** in every handover; it prevents a support call becoming an on-site visit.
13. **Name profiles consistently** as `Client - App`; it keeps the batch list readable and prevents accidental duplicates.
14. **Store deliverables outside OneDrive/Desktop sync folders** for kiosk PCs to avoid file-lock issues during compilation.

---

## 19. Limitations & Things to Know

- **Windows-oriented deliverables.** The generated `.exe`, `.bat`, `.cmd`, `.vbs` and helpers are for Windows. The builder itself runs on Python + Tkinter, but non-Windows compilation of Windows executables is not supported by PyInstaller.
- **The client still needs a Chromium browser.** The launcher opens an existing Chrome/Edge/Brave; it does not embed one. Edge is present on Windows 10/11 by default, so the auto chain almost always finds something.
- **The `.exe` is not code-signed.** SmartScreen may show "Unknown publisher" until the client clicks *More info → Run anyway*, or until you sign it with a code-signing certificate.
- **Offline fallback page is EXE-only.** Batch/CMD scripts retry and then launch the URL directly.
- **Session wiping is EXE-only** and requires the isolated profile option.
- **Delete has no confirmation.** Export a backup first.
- **`--ignore-certificate-errors` weakens security.** Use only inside a trusted network.
- **Custom CLI flags are split on spaces,** so a flag value containing a space can be misparsed. Keep values space-free.
- **Kiosk mode can be escaped** with `Alt + F4` (and `Ctrl+Alt+Del`). For true OS-level lockdown, combine with Windows Assigned Access / Shell Launcher.
- **The browser audit reflects your machine,** not the client's.
- **Presets only touch launch behaviour** — never identity, paths, metadata, network settings or deliverable choices.
- **No built-in updater.** New client builds are delivered as new files.
- **No cloud sync or telemetry.** The profile database is a local JSON file.

---

## 20. FAQ

**Is my web application copied into the `.exe`?**
No. The `.exe` only launches Chrome/Edge/Brave at your URL. Deploying a website update requires no rebuild unless you also want to change launcher settings.

**Does the client need Python installed?**
No. The `.exe` is a single portable file. Python is needed only on your build machine.

**Does the client need administrator rights?**
No, unless you enable `--uac-admin`.

**Can I build on macOS or Linux?**
The Tkinter UI may run, but Windows `.exe` compilation with this configuration is a Windows workflow.

**What exactly does `--kiosk-printing` do?**
It bypasses the Chrome print-preview dialog so printing goes straight to the Windows default printer — the standard trick for thermal receipt counters.

**Will the client be able to browse the internet?**
In full kiosk mode there is no address bar, so normal browsing is impractical, but the machine is not OS-locked. Combine with Windows Assigned Access if you need enforcement.

**What happens if the server is down at boot?**
With the health check enabled, the launcher retries N times (2 seconds apart). If it still fails, the EXE shows your branded offline page and keeps retrying every 5 seconds.

**Why does the offline page show when the site loads fine in a normal browser?**
The guard requires a successful response with a 3-second timeout. Slow servers, redirects to login, or HTTP errors can fail the check. Increase retries, or turn the guard off for that client.

**Can two different clients share one PC?**
Yes — each build uses its own profile folder and base filename, so their cookies and cache stay separate. Keep the profile folder names distinct.

**Can I use a logo that is not `.ico`?**
Yes. PNG/JPG/BMP/WEBP is converted to a multi-resolution ICO automatically (Pillow required). Square images of at least 256×256 look best.

**Where does the `.exe` get its icon?**
From the **Launcher Icon** field at build time. Changing the icon later requires a rebuild.

**Why is the same client listed twice in the dropdown?**
The key is `Client - App`, so a slightly different spelling creates a second profile. Delete the unwanted one.

**Is deleting a profile reversible?**
No. That is why **Export JSON** exists.

**Can I edit the generated `.bat` by hand?**
Yes — it is plain text and safe to modify. Note that rebuilding will overwrite it.

**Does batch build use each profile's own settings?**
Yes. Each profile is loaded and built with its own URL, folder, icon, flags and deliverable choices.

**Why did batch build stop?**
It does not stop; failures are logged and the run continues. Check the log lines for the failing profile.

**Can the launcher auto-start with Windows?**
Yes, if you include and run `Install_<base>_AutoStart.bat` on the client machine.

**How does the client close a full-screen kiosk?**
`Alt + F4`, or run `Close_<base>_Kiosk.bat`.

**Will anti-virus flag the `.exe`?**
Unsigned PyInstaller executables are sometimes flagged heuristically. Ship the `.bat`/`.vbs` alongside, and consider code-signing for large deployments.

**Can I point the launcher at `localhost`?**
Yes, if the web server runs on the client machine itself. Use `http://localhost:8080` (or the actual port).

**Does it work with `file://` pages?**
Yes, but the connectivity guard is skipped for `file://` targets.

**Where are cookies stored on the client PC?**
`%LOCALAPPDATA%\WebAppKiosks\<ProfileFolder>\Default\` when the isolated profile is enabled.

**Can I reset a client's kiosk state remotely?**
Not remotely — but you can instruct them to run `Close_<base>_Kiosk.bat` and delete the profile folder, or rebuild with cache purge enabled.

**Does KioskForge Pro send anything to the internet?**
Only pip (when you click Install Build Tools) and PyInstaller's own local work. No telemetry, no accounts, no cloud calls.

---

## 21. Glossary

| Term | Meaning |
|---|---|
| **Kiosk mode** | Borderless fullscreen browser with no tabs, address bar or window controls |
| **App mode** | A browser window that looks like a desktop program: title bar and close button, but no URL bar |
| **Isolated profile** | A private browser data folder used only by this app |
| **Profile folder** | `%LOCALAPPDATA%\WebAppKiosks\<name>` — where this app's cookies and cache live |
| **Base filename** | The root name used for every generated file |
| **Deliverable** | A file you hand to the client (`.exe`, `.bat`, `.zip`, …) |
| **Preset** | A saved combination of kiosk switches for a common scenario |
| **Health check** | A pre-launch request that verifies the server responds |
| **Offline guard** | The branded "waiting for network" page that retries automatically |
| **Silent printing** | Printing without the browser's print-preview dialog |
| **UAC** | Windows User Account Control; `--uac-admin` makes the `.exe` request elevation |
| **CLI flag / switch** | A command-line option passed to the browser |
| **Primary launcher** | The file the shortcut/auto-start helpers point to (the `.exe` if built) |
| **Batch build** | Compiling several saved profiles in one run |

---

## 22. Repository Layout

```text
webToExe/
├── app.py                  # Entire KioskForge Pro application (UI, logic, generators)
├── kiosk_clients.json      # Example client profile export (importable)
├── kiosk_clients_db.json   # Created at runtime: your live profile database
├── README.md               # This bilingual technical documentation
├── CLIENT-README.md        # Simple Urdu client handbook
├── FEATURES.md             # Comprehensive feature report
├── .gitignore              # Excludes PyInstaller build output
└── .github/
    ├── workflows/
    │   └── build-release.yml          # CI: compile portable EXE + publish Release
    └── scripts/
        └── gen_version_info.py        # Generates the EXE version resource
```

### Automated Releases (GitHub Actions)

`.github/workflows/build-release.yml` builds and publishes a Windows executable **entirely on GitHub-hosted runners** — no local Python, no local PyInstaller.

| Trigger | Result |
|---|---|
| Push to `main` or `master` | Compiles `KioskForgePro.exe` and publishes a new GitHub Release |
| Manual **Run workflow** | Same, without needing a commit |

**Pipeline steps**

1. Checkout → set up Python 3.12 → install PyInstaller + Pillow.
2. Read `APP_VERSION` from `app.py` and derive the tag `v<version>-build.<run_number>`.
3. Generate `version_info.txt` (Company / Product / Version / Copyright) from `APP_VERSION`.
4. Compile with `--onefile --noconsole --clean --version-file` (+ `--icon assets/icon.ico` automatically if that file exists).
5. Rename to `KioskForgePro-v<version>-windows-x64.exe`, generate `SHA256SUMS.txt`.
6. Upload a workflow artifact (30-day retention).
7. Create a GitHub Release with the EXE + checksum, auto-generated release notes, and mark it as **Latest**.

**To use it**

1. Push this repository to GitHub (the workflow must exist on the default branch).
2. Commit anything — the run starts automatically.
3. Open **Releases** on the repo and download the `.exe`.

Notes:
- Repository **Settings → Actions → General → Workflow permissions** must allow *Read and write permissions* (the workflow already requests `contents: write`).
- Add `assets/icon.ico` to the repo if you want a custom executable icon.
- Releases are unsigned, so SmartScreen may prompt once on the client machine.
- The portable build manages profiles, presets, previews and every script deliverable, but compiling a client `.exe` still needs PyInstaller in a local Python installation (a frozen build cannot run pip or PyInstaller on itself).

---

## 23. Changelog

### v2.4.0 — current
- Enterprise rebrand: **KioskForge Pro** with a full card-based slate/blue UI, live tooltips on nearly every control and a maximised, fullscreen-capable shell.
- **Client profile database** with load / save / delete / JSON import / JSON export.
- **Five deployment presets** (POS, standalone app, public kiosk, queue display, self-signed intranet).
- **Three launch modes** plus 12 individual runtime switches.
- **Live multi-view code preview** (CLI, batch, EXE Python source, VBS) with clipboard copy.
- **Network & Offline Guard** tab: reachability check with configurable retries, branded auto-reconnect page, cache purge, session wipe, proxy and user-agent overrides.
- **EXE Metadata & Security** tab: company/product/description/version/copyright branding plus optional UAC elevation.
- **Four deliverable formats** and **four helper utilities**, with automatic multi-resolution icon conversion and full ZIP packaging.
- **Multi-Client Batch Build** tab with multi-select and sequential compilation.
- **Build Log & Diagnostics** with timestamped logging and local browser audit.
- Threaded builds, dependency badge, one-click pip installer, auto-synchronised filename/profile/product derivation, and CLI flag sanitisation.
- **Portable-build support:** when running as a compiled `.exe`, the profile database is now stored beside the executable instead of PyInstaller's temporary extraction folder, so saved client profiles persist between runs.
- **CI/CD:** GitHub Actions workflow compiles the portable Windows executable and publishes a tagged GitHub Release on every push to `main`.

---

## 24. Support & Credits

<div align="center">

**Yasin Ullah** — Bannu Software Solutions
📱 WhatsApp: **0336-1593533**

*Building professional client delivery experiences for Pakistan and beyond.*

</div>

---
---

# PART B — اردو دستاویزات

## 25. اردو تعارف

**KioskForge Pro** ایک ونڈوز ڈیسک ٹاپ ایپلیکیشن ہے جو آپ کی ویب ایپلیکیشن کو کلائنٹ کے کمپیوٹر کے لیے ایک **پروفیشنل، برانڈڈ اور ڈبل کلک سے چلنے والے پروگرام** میں تبدیل کر دیتی ہے۔

آسان الفاظ میں:

> آپ کی ویب ایپلیکیشن آپ کے سرور پر رہتی ہے۔ KioskForge Pro اس کا وہ "دروازہ" بناتی ہے جس پر کلائنٹ ڈبل کلک کر کے اندر داخل ہوتا ہے — پوری اسکرین پر، اشتہاری بار کے بغیر، پرنٹ کے پاپ اپ کے بغیر، اور بجلی بند ہونے کے بعد خود بخود دوبارہ جڑنے والا۔

یہ ایپ **ویب سائٹ نہیں بناتی** اور ویب سائٹ کو کہیں منتقل بھی نہیں کرتی۔ یہ صرف کلائنٹ کی طرف کا وہ حصہ بناتی ہے جو ڈبل کلک کیا جاتا ہے، اور یہ طے کرتی ہے کہ کمپیوٹر پر موجود براؤزر (کروم، ایج یا بریو) آپ کی ویب ایپ کو کیسے کھولے گا۔

**یہ ایپ کیا بناتی ہے:**

- ایک پورٹیبل `.exe` فائل (کوئی تنصیب نہیں چاہیے، پائتھون کی ضرورت نہیں)
- `.bat` اور `.cmd` سکرپٹ (بیک اپ کے طور پر)
- `.vbs` سائلنٹ لانچر (کالی کمانڈ ونڈو نظر نہیں آتی)
- ڈیسک ٹاپ شارٹ کٹ بنانے والا سہولتی سکرپٹ
- ونڈوز کے ساتھ خود بخود چلنے والا سہولتی سکرپٹ
- ہنگامی طور پر کائیوسک بند کرنے والا سہولتی سکرپٹ
- سب کچھ ایک `.zip` میں، کلائنٹ کے لیے لکھی ہوئی ہدایت نامہ کے ساتھ
- برانڈڈ "نیٹ ورک نہیں ہے" والی اسکرین جو خود بخود دوبارہ کوشش کرتی ہے
- اور ایک پروفائل ڈیٹابیس جس میں ہر کلائنٹ کی سیٹنگز محفوظ رہتی ہیں

---

## 26. یہ ایپ کس کے لیے ہے

| صارف | استعمال |
|---|---|
| سافٹ ویئر ہاؤس / فری لانسر | کلائنٹ کو "کروم کھول کر یہ لنک لگائیں" کہنے کے بجائے پروفیشنل پروگرام دینا |
| دکان / ریسٹورنٹ / فارمیسی | بغیر پرنٹ پوپ اپ کے تھرمل رسید پرنٹنگ |
| ہسپتال / کلینک | ٹوکن ڈسپلے اسکرین، ریسپشن کاؤنٹر، فارمیسی ٹرمینل |
| اسکول / کالج | فیس کاؤنٹر، حاضری کائیوسک، والدین کی سیلف سروس |
| سسٹم انٹیگریٹر | لوکل نیٹ ورک کی ایپس کے لیے پہلے سے سیٹ ٹرمینل |
| سپورٹ انجینئر | ہنگامی بند کرنے کا ٹول اور آف لائن اسکرین دے کر کالز کم کرنا |
| ایجنسی | ایک ہی وقت میں کئی کلائنٹس کے لانچر بنانا |

---

## 27. اہم خصوصیات ایک نظر میں

| حصہ | تفصیل |
|---|---|
| **کلائنٹ پروفائلز** | ہر کلائنٹ کی سیٹنگز محفوظ، لوڈ، ڈیلیٹ، درآمد اور برآمد |
| **پانچ تیار پریسیٹ** | POS ٹرمینل، ڈیسک ٹاپ ایپ، پبلک کائیوسک، قطار ڈسپلے، لوکل نیٹ ورک |
| **تین ونڈو موڈ** | مکمل کائیوسک، ایپ ونڈو، عام براؤزر ونڈو |
| **بارہ براؤزر سوئچ** | سائلنٹ پرنٹنگ، الگ پروفائل، انکوگنیٹو، زوم لاک، سوائپ لاک، پہلی بار کی پریشانیاں بند، آواز کی اجازت، ترجمہ بند، ایکسٹینشن بند، میکسمائز، فل اسکرین |
| **اعلیٰ درجے کا کنٹرول** | الگ پروفائل فولڈر، اسکرین اسکیل، ونڈو کا سائز اور جگہ، اپنے اضافی براؤزر سوئچ |
| **آٹھ ڈیلیوریبل** | `.exe`، `.bat`، `.cmd`، `.vbs`، شارٹ کٹ بنانے والا، آٹو اسٹارٹ، ہنگامی بندش، `.zip` |
| **نیٹ ورک گارڈ** | چلانے سے پہلے سرور کی جانچ، 1 سے 20 کوششیں، برانڈڈ آف لائن اسکرین |
| **صفائی** | پرانا کیش صاف کرنا، بند ہونے پر لاگ ان صاف کرنا، انکوگنیٹو، پراکسی، یوزر ایجنٹ |
| **EXE برانڈنگ** | کمپنی، پروڈکٹ، تفصیل، ورژن، کاپی رائٹ، اپنی آئیکن، ایڈمن اجازت |
| **لائیو پیش نظارہ** | بنانے سے پہلے ہر سکرپٹ اور کمانڈ دیکھیں اور کاپی کریں |
| **تشخیص** | ٹولز کی حالت، ایک کلک میں تنصیب، براؤزر کی جانچ، وقت کے ساتھ لاگ |
| **بیچ بلڈ** | کئی کلائنٹ پروفائلز ایک ساتھ بنانا |
| **آسانی** | مکمل اسکرین (F11)، ہر بٹن پر رہنمائی، خودکار نام، پس منظر میں تعمیر |

---

## 28. سسٹم کی ضروریات اور تنصیب

**آپ کے کمپیوٹر پر:**

1. ونڈوز 10 یا 11
2. پائتھون 3.8 یا اس سے نیا (`tkinter` کے ساتھ)
3. PyInstaller — صرف `.exe` بنانے کے لیے
4. Pillow — صرف تصویر کو آئیکن میں بدلنے کے لیے
5. کم از کم ایک براؤزر: کروم، ایج یا بریو

**چلانے کا طریقہ:**

1. `app.py` فائل کھولیں۔
2. کمانڈ لائن میں لکھیں: `python app.py`
3. پروگرام مکمل اسکرین میں کھل جائے گا۔
4. پہلی بار اوپر دائیں طرف **Install Build Tools** دبائیں اور انتظار کریں۔
5. جب سبز نشان `Build Engine Ready` آ جائے تو سب تیار ہے۔

**کلائنٹ کے کمپیوٹر پر:**

- ونڈوز 10 یا 11
- کوئی براؤزر (ایج ونڈوز کے ساتھ پہلے سے ہوتا ہے)
- آپ کا دیا ہوا پروگرام
- نہ پائتھون، نہ تنصیب، نہ ایڈمن اجازت (جب تک آپ خود ایڈمن اجازت شامل نہ کریں)

---

## 29. انٹرفیس کا مکمل نقشہ

پروگرام کھلنے پر تین حصے نظر آتے ہیں:

**۱۔ اوپر کی پٹی (ٹاپ بار)**
- بائیں طرف پروگرام کا نام
- دائیں طرف ٹولز کی حالت (سبز یا پیلا نشان)
- **Install Build Tools** بٹن
- **Fullscreen (F11)** بٹن

**۲۔ ٹول بار (دوسری پٹی)**
- **Client Profile** — محفوظ پروفائل منتخب کریں
- **Load** — منتخب پروفائل کھولیں
- **Save Profile** — موجودہ سیٹنگز محفوظ کریں
- **Delete** — منتخب پروفائل مٹائیں
- **Import JSON** — باہر سے پروفائل لائیں
- **Export JSON** — سب پروفائلز بیک اپ کریں
- **Deployment Preset** — تیار سیٹنگ منتخب کریں

**۳۔ بائیں طرف تین کارڈ (سیٹنگز)**
- کارڈ 1: کلائنٹ اور ویب ایپ کی معلومات
- کارڈ 2: ونڈو موڈ اور براؤزر کے سوئچ
- کارڈ 3: کون سی فائلیں بنائی جائیں

**۴۔ دائیں طرف پانچ ٹیب**
- Code & Script Preview — کوڈ کا پیش نظارہ
- Network & Offline Guard — نیٹ ورک اور آف لائن اسکرین
- EXE Metadata & Security — پروگرام کی شناخت
- Multi-Client Batch Build — کئی کلائنٹ ایک ساتھ
- Build Log & Diagnostics — بنانے کا مکمل ریکارڈ

**۵۔ نیچے دائیں طرف بٹن**
- Test Launch on This PC — اپنے کمپیوٹر پر آزمائیں
- Open Output Folder — فائلیں کہاں بنی ہیں، وہاں جائیں
- Build & Package Client Launcher(s) — بنانا شروع کریں

**شارٹ کٹ:** `F11` سے مکمل اسکرین، `Esc` سے باہر۔ ہر بٹن پر ماؤس لے جانے سے ایک چھوٹی رہنمائی نظر آتی ہے۔

---

## 30. ہر ماڈیول کی تفصیل

### 30.1 اوپر کی پٹی

| چیز | کام |
|---|---|
| حالت کا نشان | بتاتا ہے کہ `.exe` بنانے والے ٹولز موجود ہیں یا نہیں |
| سبز نشان | سب تیار ہے |
| پیلا نشان | کوئی ٹول غائب ہے (`Missing: PyInstaller` وغیرہ) |
| Install Build Tools | غائب ٹولز خود بخود انسٹال کرتا ہے اور لاگ میں سب دکھاتا ہے |
| Fullscreen | پوری اسکرین پر کام کرنے کے لیے |

**اہم بات:** PyInstaller نہ ہو تو صرف `.exe` نہیں بن سکتا؛ `.bat` اور `.cmd` پھر بھی بن سکتے ہیں۔ Pillow نہ ہو تو پروگرام بن جاتا ہے لیکن آئیکن شامل نہیں ہوتی۔

### 30.2 کلائنٹ پروفائل مینیجر

ہر کلائنٹ کی سیٹنگز ایک نام کے ساتھ محفوظ ہوتی ہیں۔ نام کا طریقہ: `کلائنٹ کا نام - ایپ کا نام`۔

| بٹن | کام | خیال رکھیں |
|---|---|---|
| Load | منتخب پروفائل کی سیٹنگز اسکرین پر لاتا ہے | آئیکن بھی ساتھ آتی ہے |
| Save Profile | موجودہ سیٹنگز محفوظ کرتا ہے | وہی نام دوبارہ دیں تو پرانی تبدیل ہو جاتی ہے |
| Delete | پروفائل مٹا دیتا ہے | کوئی تصدیق نہیں پوچھی جاتی، پہلے بیک اپ لیں |
| Import JSON | باہر کی فائل سے پروفائل لاتا ہے | نئے پروفائل شامل ہوتے ہیں، پرانے رہتے ہیں |
| Export JSON | تمام پروفائلز ایک فائل میں محفوظ کرتا ہے | کمپیوٹر بدلنے سے پہلے ضرور کریں |

### 30.3 تیار پریسیٹ

| پریسیٹ | کس کے لیے |
|---|---|
| POS & Thermal Receipt Terminal | دکان، فارمیسی، رسید پرنٹنگ والے کاؤنٹر |
| Standalone Desktop Web App | دفتری ڈیسک ٹاپ پروگرام کی طرح |
| Locked Public Self-Service Kiosk | عوام کے لیے کھلا سیلف سروس ٹرمینل |
| Hospital / School Queue Display Screen | انتظار گاہ کی ٹوکن/قطار اسکرین |
| Local Intranet / Self-Signed HTTPS App | لوکل نیٹ ورک کی ایپس |

**یاد رکھیں:** پریسیٹ صرف چلنے کے طریقے بدلتا ہے — کلائنٹ کا نام، لنک، آئیکن، فولڈر، نیٹ ورک سیٹنگز اور فائلوں کا انتخاب نہیں بدلتا۔

### 30.4 کارڈ 1 — کلائنٹ اور ویب ایپ

| خانہ | مطلب |
|---|---|
| Client / Organization | کلائنٹ کے ادارے کا نام |
| Web App Title | آپ کی ایپ کا نام — لکھتے ہی فائل کا نام، پروفائل فولڈر اور پروڈکٹ نام خود بن جاتے ہیں |
| Web Application URL | ایپ کا پتہ؛ `https://` خود لگ جاتا ہے |
| Target Browser Engine | کون سا براؤزر — خودکار (کروم، پھر ایج، پھر بریو) یا کوئی ایک |
| Launcher Icon | کمپنی کا لوگو؛ تصویر خود آئیکن میں بدل جاتی ہے |
| Output Base Filename | بننے والی تمام فائلوں کا بنیادی نام |
| Deliverables Folder | فائلیں کہاں محفوظ ہوں |

### 30.5 کارڈ 2 — ونڈو موڈ اور سوئچ

**تین موڈ:**

1. **Full Kiosk** — پوری اسکرین، نہ ایڈریس بار، نہ ٹیب، نہ بند کرنے کا بٹن۔ کاؤنٹر اور پبلک ٹرمینل کے لیے۔
2. **Standalone App Window** — عام پروگرام جیسی ونڈو، بند کرنے کا بٹن موجود، مگر ایڈریس بار نہیں۔ دفتری استعمال کے لیے۔
3. **Standard Browser Window** — عام براؤزر ونڈو، باقی سیٹنگز پھر بھی لاگو۔ جانچ کے لیے۔

**بارہ سوئچ اور ان کا فائدہ:**

| سوئچ | فائدہ |
|---|---|
| Silent POS Printing | پرنٹ کا پوپ اپ نہیں آتا، سیدھا پرنٹ ہوتا ہے |
| Isolated App Profile | اس ایپ کے لیے الگ براؤزر فولڈر — کائیوسک سیٹنگز کام کرتی ہیں |
| Incognito | کوئی لاگ ان یا ڈیٹا محفوظ نہیں رہتا |
| Disable Touch Pinch-Zoom | ٹچ اسکرین پر غلطی سے زوم نہیں ہوتا |
| Disable Swipe Navigation | انگلی کے سوائپ سے ایپ سے باہر نہیں جاتے |
| Skip First-Run Prompts | "خوش آمدید" اور "ڈیفالٹ براؤزر" والے پاپ اپ نہیں آتے |
| Suppress Crash Bubbles | بجلی جانے کے بعد "دوبارہ کھولیں؟" والا پیغام نہیں آتا |
| Allow Sound Autoplay | آواز اور ٹوکن کی آواز بغیر کلک چلتی ہے |
| Disable Translate Popup | ترجمے کی پٹی نہیں آتی |
| Disable Extensions | کوئی ایکسٹینشن ایپ کو خراب نہیں کرتا |
| Start Maximized | ونڈو پوری کھلتی ہے |
| Start Fullscreen | پوری اسکرین میں شروع ہوتی ہے |

**اضافی کنٹرول:** الگ پروفائل فولڈر کا نام، اسکرین اسکیل (چھوٹی/بڑی نظر آنے کے لیے)، اپنی مرضی کی ونڈو چوڑائی/اونچائی اور جگہ، اور اپنے اضافی براؤزر سوئچ۔

### 30.6 کارڈ 3 — کون سی فائلیں بنیں

| انتخاب | بننے والی فائل |
|---|---|
| Portable Single-File .EXE | `<نام>.exe` — سب سے اہم فائل، ڈبل کلک سے چلتی ہے |
| Windows Batch Script | `<نام>.bat` — بیک اپ لانچر |
| Windows Command Script | `<نام>.cmd` — ویسی ہی فائل، مختلف توسیع |
| Silent VBScript | `<نام>_Silent.vbs` — بغیر کالی ونڈو کے چلاتا ہے |
| Desktop Shortcut Creator | `Create_<نام>_Desktop_Shortcut.bat` — ڈیسک ٹاپ پر آئیکن بناتا ہے |
| Auto-Start Installer | `Install_<نام>_AutoStart.bat` — کمپیوٹر آن ہوتے ہی ایپ کھل جائے |
| Emergency Close Tool | `Close_<نام>_Kiosk.bat` — پھنسی ہوئی اسکرین بند کرتا ہے |
| Bundle ZIP + Guide | `<نام>_Client_Deliverable.zip` — سب کچھ ایک فائل میں |
| Close Previous Instance | پرانی کھلی ونڈو بند کر کے نئی کھولتا ہے |

**اہم:** کم از کم ایک لانچر (`.exe` یا `.bat` یا `.cmd`) ضرور منتخب ہونا چاہیے۔ `.vbs` منتخب ہو تو `.bat` خود بنتی ہے کیونکہ `.vbs` اسی کو چلاتی ہے۔

### 30.7 کوڈ پیش نظارہ ٹیب

یہاں آپ بنانے سے **پہلے** دیکھ سکتے ہیں کہ بالکل کیا بنے گا:

- **CLI Command** — براؤزر کو دی جانے والی مکمل کمانڈ
- **Windows Batch** — `.bat` سکرپٹ کا مکمل متن
- **Portable EXE Python Source** — `.exe` کے اندر چلنے والا پروگرام
- **Silent VBScript** — `.vbs` کا متن

**Copy Code** بٹن سے سارا متن کاپی ہو جاتا ہے۔

### 30.8 نیٹ ورک اور آف لائن گارڈ ٹیب

| کنٹرول | کام |
|---|---|
| Verify Server Reachability | چلانے سے پہلے دیکھتا ہے کہ سرور جواب دے رہا ہے |
| Retry Attempts | کتنی بار کوشش کی جائے (ہر کوشش کے بعد 2 سیکنڈ وقفہ) |
| Show Offline Screen | سرور نہ ملنے پر برانڈڈ اسکرین دکھائی جائے (صرف `.exe` میں) |
| Support Contact | آف لائن اسکرین پر آپ کا نمبر |
| Ignore SSL Warnings | لوکل سرور کے سرٹیفکیٹ کی تنبیہ نظر انداز |
| Purge Cache Before Launch | پرانا کیش صاف — کلائنٹ کو ہمیشہ نیا ورژن ملے |
| Wipe Session After Close | بند ہونے پر لاگ ان اور کوکیز صاف (صرف `.exe`) |
| Proxy Server | پراکسی کی ضرورت ہو تو پتہ |
| Custom User-Agent | خاص صورتوں میں براؤزر کی شناخت بدلنا |

### 30.9 پروگرام کی شناخت (EXE Metadata) ٹیب

یہ معلومات پروگرام کی "پراپرٹیز" میں نظر آتی ہیں:

- کمپنی کا نام
- پروڈکٹ کا نام
- مختصر تفصیل
- ورژن (مثلاً `1.0.0.0`)
- کاپی رائٹ
- ایڈمن اجازت (عام طور پر بند رکھیں)

### 30.10 بیچ بلڈ ٹیب

ایک ساتھ کئی کلائنٹس کے پروگرام بنانے کے لیے:

1. فہرست میں سے ایک یا زیادہ پروفائل منتخب کریں (Ctrl دبا کر کئی منتخب ہو سکتے ہیں)
2. **Select All** سے سب منتخب کریں
3. **Compile Selected Client Profiles** دبائیں
4. ہر پروفائل اپنے فولڈر میں بنے گا
5. آخر میں ایک خلاصہ پیغام آئے گا

### 30.11 بلڈ لاگ ٹیب

یہاں ہر کام کا وقت کے ساتھ ریکارڈ رہتا ہے: کون سی سیٹنگ لگی، کون سا پروفائل کھلا، کیا فائل بنی، کہاں غلطی ہوئی۔

- **Re-Scan Browsers** — دوبارہ براؤزر تلاش کریں
- **Clear Log** — ریکارڈ صاف کریں

### 30.12 نیچے کے بٹن

| بٹن | کام |
|---|---|
| Test Launch on This PC | اپنے کمپیوٹر پر ویسے ہی چلا کر دیکھیں جیسے کلائنٹ دیکھے گا |
| Open Output Folder | فائلیں جہاں بنی ہیں وہ فولڈر کھولیں |
| Build & Package | اصل فائلیں بنانا شروع کریں |

---

## 31. بنانے کا مکمل طریقہ — قدم بہ قدم

**پہلی بار:**
1. **Install Build Tools** دبائیں، سبز نشان آنے تک انتظار کریں۔

**ہر نئے کلائنٹ کے لیے:**
1. **Client / Organization** میں ادارے کا نام لکھیں۔
2. **Web App Title** میں ایپ کا نام لکھیں — باقی نام خود بن جائیں گے۔
3. **Web Application URL** میں لنک لکھیں۔
4. **Deployment Preset** سے مناسب سیٹنگ منتخب کریں۔
5. **Launcher Icon** میں لوگو منتخب کریں۔
6. **Deliverables Folder** منتخب کریں۔
7. **Network & Offline Guard** ٹیب میں اپنا سپورٹ نمبر لکھیں۔
8. **EXE Metadata** ٹیب میں کمپنی، پروڈکٹ، ورژن بھریں۔
9. **Test Launch on This PC** سے جانچیں۔
10. **Build & Package Client Launcher(s)** دبائیں۔
11. لاگ میں `Build completed cleanly!` آنے پر **Open Output Folder** کھولیں۔
12. `.zip` فائل کلائنٹ کو بھیجیں۔

**بنانے کے دوران کیا ہوتا ہے (ترتیب):**
1. جانچ — کیا کم از کم ایک لانچر منتخب ہے، کیا ٹولز موجود ہیں
2. فولڈر بنانا، نام صاف کرنا
3. `.bat`، `.cmd`، `.vbs` لکھنا
4. `.exe` بنانا (اگر منتخب ہو) — آئیکن اور معلومات شامل کر کے
5. شارٹ کٹ، آٹو اسٹارٹ اور بندش والی سہولتی فائلیں بنانا
6. سب کو `.zip` میں بند کرنا، ہدایت نامہ شامل کرنا
7. عارضی فائلیں صاف کرنا اور کامیابی کا پیغام دینا

---

## 32. بننے والی فائلیں

| فائل | کام |
|---|---|
| `<نام>.exe` | اصل پروگرام — ڈبل کلک سے چلتا ہے |
| `<نام>.bat` | متبادل لانچر |
| `<نام>.cmd` | متبادل لانچر (دوسری توسیع) |
| `<نام>_Silent.vbs` | بغیر کالی ونڈو کے چلانے والا |
| `Create_<نام>_Desktop_Shortcut.bat` | ڈیسک ٹاپ آئیکن بناتا ہے |
| `Install_<نام>_AutoStart.bat` | کمپیوٹر آن ہونے پر خود چلنے کا انتظام |
| `Close_<نام>_Kiosk.bat` | پھنسی اسکرین بند کرتا ہے |
| `<نام>_Client_Deliverable.zip` | سب فائلیں + ہدایت نامہ |
| `README_Client_Instructions.txt` | ZIP کے اندر کلائنٹ کے لیے ہدایات |

---

## 33. کلائنٹ کے کمپیوٹر پر پروگرام کیسے چلتا ہے

**`.exe` کی ترتیب:**
1. براؤزر تلاش کرتا ہے (کروم، پھر ایج، پھر بریو)
2. نہ ملے تو صاف پیغام دکھا کر بند ہو جاتا ہے
3. اپنا الگ فولڈر بناتا ہے
4. پرانی کھلی ونڈو بند کرتا ہے (اگر سیٹنگ ہو)
5. پرانا کیش صاف کرتا ہے (اگر سیٹنگ ہو)
6. سرور کی جانچ کرتا ہے، نہ ملے تو کئی بار کوشش کرتا ہے
7. پھر بھی نہ ملے تو آپ کی برانڈڈ آف لائن اسکرین کھول دیتا ہے
8. سرور مل جائے تو ایپ کھول دیتا ہے
9. بند ہونے پر لاگ ان صاف کرتا ہے (اگر سیٹنگ ہو)

**`.bat` کا طریقہ:** براؤزر تلاش کرتا ہے، فولڈر بناتا ہے، کیش صاف کرتا ہے، سرور کی جانچ کرتا ہے، پھر ایپ کھول دیتا ہے۔

**`.vbs` کا طریقہ:** `.bat` کو چھپا کر چلاتا ہے تاکہ کالی ونڈو نظر نہ آئے۔

---

## 34. آف لائن اسکرین

جب سرور نہ ملے تو یہ اسکرین آتی ہے:

- اوپر پیلے رنگ میں: **WAITING FOR NETWORK / SERVER**
- آپ کی ایپ کا نام
- پیغام: سرور سے رابطہ نہیں ہو رہا، کیبل یا انٹرنیٹ دیکھیں، یہ ٹرمینل خود کوشش کرتا رہے گا
- ٹرمینل کا نام (کلائنٹ)
- آپ کا سپورٹ نمبر
- نیچے گنتی: "5 سیکنڈ میں دوبارہ کوشش"
- **Reconnect Now** بٹن

یہ اسکرین ہر 5 سیکنڈ بعد خود بخود کوشش کرتی رہتی ہے، کلائنٹ کو کچھ کرنے کی ضرورت نہیں۔

---

## 35. پروفائلز، بیک اپ اور منتقلی

- تمام پروفائلز `kiosk_clients_db.json` فائل میں محفوظ ہوتے ہیں۔
- یہ فائل `app.py` کے ساتھ والے فولڈر میں بنتی ہے۔
- **Export JSON** سے بیک اپ بنائیں — خاص طور پر ڈیلیٹ کرنے یا کمپیوٹر بدلنے سے پہلے۔
- **Import JSON** سے بیک اپ واپس لائیں۔
- یاد رکھیں: **Delete** میں کوئی تصدیق نہیں پوچھی جاتی۔
- فائل میں صرف لنک، نام اور سیٹنگز ہوتی ہیں — کوئی پاس ورڈ نہیں۔

**کلائنٹ کے کمپیوٹر پر ڈیٹا:** `%LOCALAPPDATA%\WebAppKiosks\<پروفائل فولڈر>\` میں کوکیز، کیش اور آف لائن اسکرین رکھی جاتی ہیں۔

---

## 36. عام استعمال کے منظرنامے

**۱۔ نیا کلائنٹ، پہلی ڈیلیوری**
نام، لنک، آئیکن، پریسیٹ، سپورٹ نمبر، معلومات → جانچ → بنائیں → ZIP بھیجیں۔

**۲۔ دکان کا رسید کاؤنٹر**
پریسیٹ `POS & Thermal Receipt Terminal` → سائلنٹ پرنٹنگ یقینی بنائیں → ونڈوز کا ڈیفالٹ پرنٹر رسید پرنٹر رکھیں → `.exe` اور بندش والا ٹول دیں۔

**۳۔ عوام کے لیے کھلا ٹرمینل**
پریسیٹ `Locked Public Self-Service Kiosk` → انکوگنیٹو، کیش صفائی اور سیشن صفائی آن → آف لائن اسکرین آن → آٹو اسٹارٹ شامل کریں۔

**۴۔ لوکل نیٹ ورک کی ایپ**
پریسیٹ `Local Intranet` → لوکل پتہ ڈالیں → سرٹیفکیٹ تنبیہ آن (صرف قابلِ اعتماد نیٹ ورک میں)۔

**۵۔ انتظار گاہ کی اسکرین**
پریسیٹ `Queue Display` → آواز کی اجازت آن → فل اسکرین → آٹو اسٹارٹ۔

**۶۔ ایپ کی نئی ورژن بھیجنا**
پروفائل کھولیں → کیش صفائی آن کریں → ورژن بڑھائیں (`1.0.0.0` سے `1.0.1.0`) → دوبارہ بنائیں۔

**۷۔ ایک ساتھ کئی کلائنٹ**
سب پروفائل محفوظ کریں → بیچ بلڈ → سب منتخب → بنائیں۔

---

## 37. مسائل اور ان کا حل

| مسئلہ | وجہ | حل |
|---|---|---|
| `Missing: PyInstaller` | ٹول نہیں ہے | Install Build Tools دبائیں |
| `.exe` نہیں بن رہا | PyInstaller غائب | ٹول انسٹال کریں یا صرف `.bat` بنائیں |
| آئیکن نہیں آئی | Pillow غائب یا تصویر خراب | Pillow انسٹال کریں، مربع تصویر دیں |
| بنا رہا ہے مگر ناکام | اینٹی وائرس، جگہ کم، یا سسٹم خراب | لاگ دیکھیں، جگہ خالی کریں، دوبارہ کوشش |
| Test Launch پر براؤزر نہیں ملا | براؤزر نہیں ہے یا غلط منتخب | خودکار (Auto) منتخب کریں |
| کائیوسک کام نہیں کرتا | الگ پروفائل بند ہے | Isolated App Profile آن کریں |
| پرنٹ پوپ اپ آ رہا ہے | سائلنٹ پرنٹنگ بند یا ڈیفالٹ پرنٹر غلط | سوئچ آن کریں، رسید پرنٹر ڈیفالٹ کریں |
| پرانا ورژن نظر آ رہا ہے | براؤزر کیش | کیش صفائی آن کریں |
| آف لائن اسکرین نہیں آتی | `.bat` استعمال ہوا یا جانچ بند | `.exe` دیں، جانچ اور آف لائن آن کریں |
| دو ونڈوز کھل جاتی ہیں | کلائنٹ نے دو بار کلک کیا | پرانی ونڈو بند کرنے والی سیٹنگ آن کریں |
| لکھائی بہت چھوٹی | اسکرین کا سائز | UI Scale بڑھائیں |
| ونڈو غلط اسکرین پر | جگہ کی سیٹنگ | Custom Window Bounds استعمال کریں |

---

## 38. بہترین طریقے

1. ہر بار **Test Launch** کریں۔
2. `.exe` کے ساتھ `.bat` بھی دیں — اینٹی وائرس سے بچاؤ۔
3. الگ پروفائل ہمیشہ آن رکھیں۔
4. ہر ڈیلیوری کا ورژن بڑھائیں۔
5. آف لائن اسکرین پر اصلی سپورٹ نمبر لکھیں۔
6. ہفتے میں ایک بار Export JSON کریں۔
7. ہنگامی بندش والا ٹول ہر کلائنٹ کو دیں۔
8. پروفائل کا نام ہمیشہ ایک ہی انداز میں رکھیں۔
9. غیر ضروری جگہ سرٹیفکیٹ تنبیہ آن نہ کریں۔
10. ڈیلیوری سے پہلے اصل ہارڈویئر پر جانچیں۔

---

## 39. اکثر پوچھے جانے والے سوالات

**کیا میری ویب سائٹ `.exe` کے اندر آ جاتی ہے؟**
نہیں۔ `.exe` صرف براؤزر کھول کر آپ کا لنک کھولتا ہے۔ ویب سائٹ کی تبدیلی کے لیے دوبارہ بنانا ضروری نہیں۔

**کلائنٹ کو پائتھون چاہیے؟**
نہیں۔ `.exe` اکیلی فائل چلتی ہے۔

**کلائنٹ کو ایڈمن اجازت چاہیے؟**
نہیں، جب تک آپ خود یہ سیٹنگ آن نہ کریں۔

**کیا یہ میکنٹوش یا لینکس پر چلے گا؟**
اصل ڈیلیوری ونڈوز کے لیے ہے۔

**سرور بند ہو تو کیا ہوگا؟**
کئی بار کوشش کے بعد آپ کی آف لائن اسکرین آئے گی اور ہر 5 سیکنڈ بعد خود کوشش کرتی رہے گی۔

**کیا آف لائن اسکرین `.bat` میں بھی آتی ہے؟**
نہیں، صرف `.exe` میں۔ `.bat` کوشش کے بعد سیدھا لنک کھول دیتا ہے۔

**ایک کمپیوٹر پر دو کلائنٹ چل سکتے ہیں؟**
جی ہاں، ہر ایک کا اپنا الگ فولڈر اور نام ہونا چاہیے۔

**کیا PNG لوگو استعمال ہو سکتا ہے؟**
جی ہاں، خود آئیکن میں بدل جاتا ہے۔ مربع اور بڑی تصویر بہتر ہے۔

**پروفائل ڈیلیٹ ہو گیا، واپس آ سکتا ہے؟**
نہیں، اسی لیے Export JSON ضروری ہے۔

**کلائنٹ مکمل اسکرین سے باہر کیسے آئے؟**
`Alt + F4` دبائیں یا `Close_<نام>_Kiosk.bat` چلائیں۔

**کیا اینٹی وائرس اعتراض کر سکتا ہے؟**
کبھی کبھی بغیر دستخط شدہ `.exe` پر ہوتا ہے۔ ساتھ `.bat` دیں یا کوڈ سائننگ کریں۔

**کیا یہ ایپ انٹرنیٹ پر کچھ بھیجتی ہے؟**
نہیں۔ کوئی اکاؤنٹ، کوئی کلاؤڈ، کوئی خفیہ ڈیٹا نہیں بھیجا جاتا۔

**کیا فائل خود بنتی ہے جب کمپیوٹر آن ہو؟**
جی ہاں، اگر آپ `Install_<نام>_AutoStart.bat` چلا دیں۔

**کیا لنک `localhost` ہو سکتا ہے؟**
جی ہاں، اگر ویب سرور اسی کمپیوٹر پر ہو۔

---

## 40. آسان لغت

| لفظ | مطلب |
|---|---|
| **کائیوسک** | پوری اسکرین پر چلنے والا پروگرام جس میں باہر نکلنے کے بٹن نہیں ہوتے |
| **لانچر** | وہ پروگرام جو ڈبل کلک سے آپ کی ویب ایپ کھولتا ہے |
| **پروفائل** | کسی ایک ایپ کے لیے الگ براؤزر فولڈر (کوکیز اور کیش) |
| **پریسیٹ** | پہلے سے تیار سیٹنگ کا مجموعہ |
| **ڈیلیوریبل** | وہ فائلیں جو کلائنٹ کو دی جاتی ہیں |
| **آف لائن اسکرین** | سرور نہ ملنے پر دکھائی جانے والی اسکرین |
| **سائلنٹ پرنٹنگ** | بغیر پوپ اپ کے سیدھا پرنٹ |
| **کیش** | براؤزر کے محفوظ کیے ہوئے پرانے حصے |
| **انکوگنیٹو** | ایسی حالت جس میں کچھ محفوظ نہیں رہتا |
| **بیچ بلڈ** | کئی کلائنٹ ایک ساتھ بنانا |

---

<div align="center">

**KioskForge Pro v2.4.0** — built with Python & Tkinter

**Yasin Ullah** · Bannu Software Solutions · WhatsApp **0336-1593533**

</div>
