# 🖥️ KioskForge Pro — Comprehensive Feature Report

### Enterprise Client Web App & Portable EXE Builder

**Version** `2.4.0` · **Platform** Windows 10/11 · **Stack** Python 3.8+ / Tkinter / PyInstaller / Pillow
**Repository** `webToExe` · **Entry point** `app.py` · **Document version** 2026-11-19

---

## 📌 Executive Summary

KioskForge Pro is a single-window Windows desktop studio that converts any hosted or local web application into a **branded, locked-down, double-clickable client launcher**. It does not host, copy or modify your web application — it engineers the client-side entry point and the exact Chromium runtime environment in which that web application opens.

From one screen it produces a portable single-file `.exe`, zero-dependency `.bat`/`.cmd` scripts, a console-free `.vbs` wrapper, a desktop-shortcut creator, a Windows auto-start installer, an emergency kiosk-close utility, and a delivery ZIP containing a formatted client instruction sheet — all driven by a persistent multi-client profile database and five scenario presets.

| Metric | Value |
|---|---|
| Total feature modules | **29** |
| Generated deliverable formats | **8** |
| Chromium runtime switches controllable | **12** + custom flags |
| Deployment presets | **5** |
| Launch modes | **3** |
| Browser engines supported | **3** (Chrome, Edge, Brave) |
| Persisted profile fields | **52** |
| Files in repository | 2 application files |
| External services / telemetry | **None** |

---

## 🧭 Module & Feature Matrix

| 📋 Module & Features | ✨ Key Capabilities | 🔐 Safety & Access |
|---|---|---|
| **🪟 Application Shell & Branding**<br>✅ Single-window enterprise UI<br>✅ Auto-maximise on launch<br>✅ Borderless fullscreen (F11 / Esc)<br>✅ Card-based inspector layout<br>✅ Splash-free instant start<br>✅ Versioned window title (`v2.4.0`) | 🎨 Modern slate/blue visual language with `clam` ttk theme<br>📐 Split workspace: 5-unit inspector / 6-unit workspace<br>🖱️ Mouse-wheel scrollable left inspector<br>⚡ Zero-lag native Tkinter rendering | 🔒 Local-only desktop execution<br>🚫 No login, no cloud, no telemetry<br>🧩 Isolated from the client's browser profile |
| **👤 Client Profile Database**<br>✅ Save named profiles<br>✅ Load / overwrite profiles<br>✅ Delete profiles<br>✅ JSON import (merge)<br>✅ JSON export (full backup)<br>✅ Alphabetical dropdown listing<br>✅ Key scheme `Client - App` | 💾 52 persisted fields per client<br>🔁 Instant load of every UI control<br>🖼️ Icon thumbnail restored on load<br>📦 Human-readable indented JSON<br>🔄 Portable across machines | 🔐 Local file `kiosk_clients_db.json` beside `app.py`<br>🔑 Contains URLs, paths, branding text only — no passwords<br>⚠️ Delete is permanent (no undo dialog)<br>💡 Export before destructive actions |
| **🎛️ Deployment Presets**<br>✅ POS & Thermal Receipt Terminal<br>✅ Standalone Desktop Web App (`--app`)<br>✅ Locked Public Self-Service Kiosk<br>✅ Hospital / School Queue Display Screen<br>✅ Local Intranet / Self-Signed HTTPS App | ⚡ One selection applies 18 launch attributes<br>🧠 Field-tested flag combinations<br>📝 Logs `Applied preset profile: <name>`<br>✏️ Every value remains individually editable<br>🎯 Presets never touch identity, paths, metadata or deliverables | 🔒 Presets are read-only templates<br>✅ No silent URL or filename changes<br>🧾 Audit line written to build console<br>↩️ Revert by picking another preset |
| **🏷️ Client Identity & Target Configuration**<br>✅ Client / Organization name<br>✅ Web App Title<br>✅ Web Application URL<br>✅ Target browser engine<br>✅ Launcher icon path<br>✅ Output base filename<br>✅ Deliverables folder | 🔗 URL normalisation (auto `https://` when scheme omitted)<br>🔤 Slug generator: illegal characters → underscore<br>🖼️ Live 32-px icon thumbnail<br>📁 Auto-created output directory<br>🧩 Supports `http`, `https`, `file` schemes | 🔐 Explicit fields — nothing inferred silently<br>✅ Fallback slug `Client_WebApp` prevents empty names<br>👁️ Thumbnail confirms the correct logo before build |
| **🪟 Launch Mode Engine**<br>✅ Full Kiosk (`--kiosk`)<br>✅ Standalone App Window (`--app=<url>`)<br>✅ Standard Browser Window<br>✅ Mutually exclusive radio selection | 🖥️ Kiosk: borderless, no tabs/address bar/window controls<br>🗔 App: native title bar + minimise/close, no URL bar<br>🌐 Standard: normal window with all other flags applied<br>🔀 Correct URL placement per mode | 🔒 Deliberate, explicit mode choice<br>✅ One mode at a time (radio enforcement)<br>🧾 Mode visible in live CLI preview and client guide |
| **⚙️ Kiosk Attribute Engine**<br>✅ Silent POS printing<br>✅ Isolated app profile<br>✅ Incognito / ephemeral mode<br>✅ Touch pinch-zoom lock<br>✅ Swipe navigation lock<br>✅ First-run prompt suppression<br>✅ Crash & restore bubble suppression<br>✅ Media autoplay permission<br>✅ Translate-popup suppression<br>✅ Extension blocking<br>✅ Start maximised<br>✅ Start fullscreen | 🖨️ `--kiosk-printing` — prints straight to the Windows default printer<br>📂 `--user-data-dir` — dedicated profile so kiosk flags work beside normal Chrome<br>🔒 `--disable-pinch`, `--overscroll-history-navigation=0`<br>🚫 `--no-first-run`, `--no-default-browser-check`<br>🧹 `--noerrdialogs`, `--disable-session-crashed-bubble`, `--disable-infobars`<br>🔊 `--autoplay-policy=no-user-gesture-required`<br>🌐 `--disable-features=Translate`<br>🧩 `--disable-extensions`<br>📏 `--start-maximized`, `--start-fullscreen` | 🔐 Every switch is an explicit, labelled opt-in<br>👁️ Tooltip explains each switch in plain language<br>🧾 Final flag list inspectable before compiling<br>🛡️ No registry edits, no OS lockdown, no hidden changes |
| **🖥️ Advanced Display & Window Control**<br>✅ Isolated profile folder naming<br>✅ UI scale factor (0.75–1.5)<br>✅ Custom window width / height<br>✅ Custom screen X / Y position<br>✅ Free-form extra CLI flags | 📐 `--force-device-scale-factor` for high-DPI or compact POS panels<br>🗺️ `--window-size` + `--window-position` for multi-monitor layouts<br>🧮 Numeric validation before a flag is emitted<br>➕ Arbitrary additional Chromium switches | 🔒 Values are validated before injection<br>✅ Blank/invalid geometry is silently skipped (no broken launch)<br>⚠️ Extra flags are space-split — keep values space-free |
| **🌐 Browser Engine Targeting & Audit**<br>✅ Auto chain: Chrome → Edge → Brave<br>✅ Chrome-only mode<br>✅ Edge-only mode<br>✅ Brave-only mode<br>✅ Startup browser audit<br>✅ Manual re-scan<br>✅ Full path logging | 🔍 Probes `%ProgramFiles%`, `%ProgramFiles(x86)%`, `%LocalAppData%`<br>📋 Logs every `[FOUND]` path or a clear warning<br>🛟 Auto mode guarantees a fallback on stock Windows (Edge)<br>🔁 Baked candidate list inside generated EXE | 🔐 Read-only filesystem probes<br>🚫 No registry scraping, no elevation<br>📝 Audit results reproducible from the log |
| **📦 Deliverable Compiler**<br>✅ Portable single-file `.exe`<br>✅ `.bat` launcher<br>✅ `.cmd` launcher<br>✅ Silent `.vbs` wrapper<br>✅ Desktop shortcut creator<br>✅ Auto-start installer<br>✅ Emergency close/reset tool<br>✅ Delivery ZIP + client guide | 🧱 Four primary formats + four helper utilities<br>🎯 Primary-file resolution: `.exe` first, else first generated script<br>🔗 VBS automatically writes its required `.bat`<br>📦 ZIP includes every generated file + `README_Client_Instructions.txt`<br>🧹 Temporary build workspace auto-deleted | 🔐 Explicit checkbox selection per deliverable<br>🛑 Build refused if no primary launcher is chosen<br>✅ Helpers only target files generated in the same run<br>📝 Every generated path logged |
| **🏗️ Portable EXE Compilation Pipeline**<br>✅ PyInstaller single-file build<br>✅ Console-free (`--noconsole`)<br>✅ Clean build (`--clean`)<br>✅ Custom icon embedding<br>✅ Version-resource embedding<br>✅ Optional UAC admin manifest<br>✅ Output copied to deliverables folder<br>✅ Live PyInstaller log filtering | ⚙️ `--onefile --noconsole --clean --noconfirm`<br>📄 Generates `version_info.txt` resource file<br>🎨 Multi-resolution ICO injected via `--icon`<br>🛡️ `--uac-admin` only when requested<br>📊 Streams `INFO:`, `WARNING:`, `ERROR:` lines<br>🧯 Clean failure handling with temp cleanup | 🔒 Build fails closed with a clear dialog<br>📁 Isolated temp directory (`kioskforge_*`)<br>🚫 Never modifies the source tree<br>✅ Dependency pre-check prevents half-built output |
| **🤫 Silent VBS Wrapper**<br>✅ Hidden console launch<br>✅ Self-locating script directory<br>✅ Missing-script error box<br>✅ Non-blocking execution | 🪟 `WshShell.Run ..., 0, False` — no black window flash<br>📂 Resolves its own folder via `Scripting.FileSystemObject`<br>🔗 References the `.bat` by exact filename<br>💬 Clear message box if the script is missing | 🔐 No elevation, no registry writes<br>✅ Fails visibly rather than silently<br>📝 No shell injection surface (fixed local filename) |
| **🖱️ Desktop Shortcut Creator**<br>✅ Generates a real Windows `.lnk`<br>✅ Uses the app title as the shortcut name<br>✅ Sets working directory<br>✅ Validates target existence<br>✅ Friendly success/failure message | 🧩 PowerShell `WScript.Shell` COM shortcut creation<br>📛 Illegal filename characters stripped from the title<br>🖥️ Writes to the current user's Desktop folder<br>♻️ Safe to run multiple times (overwrites) | 🔐 Standard-user permissions only<br>✅ Aborts with a clear message if the target file is absent<br>🚫 No system-wide changes |
| **🚀 Windows Auto-Start Installer**<br>✅ Copies the primary launcher to the Startup folder<br>✅ Target-existence validation<br>✅ Confirmation message<br>✅ Per-user installation | 🔁 Launches automatically after Windows sign-in<br>📁 Uses `%APPDATA%\...\Start Menu\Programs\Startup`<br>🖥️ Ideal for queue displays, POS counters, reception terminals<br>🛠️ Reversible by removing the copied file | 🔐 Per-user scope — no admin rights required<br>✅ No scheduled tasks, no services, no registry run keys<br>📝 Explicit, visible, auditable copy operation |
| **🛑 Emergency Kiosk Close / Reset Utility**<br>✅ Force-closes only this app's processes<br>✅ Matches on the isolated profile folder name<br>✅ Leaves normal Chrome sessions untouched<br>✅ Progress confirmation<br>✅ No arguments required | 🎯 PowerShell `Get-CimInstance Win32_Process` + `Where-Object CommandLine -like '*<profile>*'`<br>🧯 Recovers a stuck fullscreen kiosk instantly<br>📞 Reduces on-site support visits<br>⚡ Silent error suppression | 🔐 Scoped to one profile name — cannot kill unrelated browsers<br>✅ No elevation needed for own-user processes<br>📝 Console output confirms completion |
| **🗜️ Delivery ZIP Packaging**<br>✅ Bundles every generated file<br>✅ Embedded `README_Client_Instructions.txt`<br>✅ Deflate compression<br>✅ Flat archive structure<br>✅ Named `<base>_Client_Deliverable.zip` | 🎁 One file to email or WhatsApp<br>📋 Instruction sheet includes client name, URL, display mode, support desk, file list and 5-step deployment guide<br>📦 Only current-run deliverables included<br>🗂️ Predictable archive naming | 🔐 Contains no credentials or source code of your web app<br>✅ Includes the support contact for end users<br>📝 Packaging step logged |
| **🔍 Live Code Preview Studio**<br>✅ CLI command view<br>✅ Windows Batch view<br>✅ Portable EXE Python source view<br>✅ Silent VBScript view<br>✅ Instant regeneration on any change<br>✅ Copy to clipboard<br>✅ Monospace scrollable viewer | 👁️ See the exact output *before* spending build time<br>🧪 Verify flags, retries, URLs and paths<br>📋 Copy code into tickets, emails or documentation<br>🧠 Full transparency — nothing is hidden from the operator<br>⚡ Traced variables refresh previews on every keystroke | 🔐 Read-only inspection of generated text<br>✅ Clipboard copy logged<br>🚫 Preview never executes anything |
| **📡 Network Reachability Guard**<br>✅ Pre-launch server check<br>✅ Configurable retry attempts (1–20)<br>✅ 3-second request timeout<br>✅ 2-second retry interval<br>✅ Automatic `file://` bypass<br>✅ PowerShell check inside `.bat`<br>✅ Native check inside `.exe` | 🌐 Prevents the "no internet dinosaur" page at boot<br>📶 Survives slow DHCP/Wi-Fi association on cold boot<br>🔁 Retries give routers and LAN servers time to come up<br>🧾 Success jumps directly to the launch label<br>📉 Exhausted retries still launch the real URL in script mode | 🔐 No third-party services involved<br>✅ Only the configured URL is contacted<br>🔓 Certificate verification is relaxed inside the EXE probe (intranet-friendly) |
| **🛟 Branded Offline Guard Screen**<br>✅ Custom HTML fallback page<br>✅ Client name display<br>✅ Support contact display<br>✅ 5-second auto-retry loop<br>✅ Live countdown text<br>✅ "Reconnect Now" button<br>✅ Clean professional styling | 🎨 White card, slate text, blue action button<br>📴 Renders with no internet connection<br>🔄 Retries forever until the server returns<br>🧭 Auto-navigates back to the real app on success<br>💬 Replaces frightening browser error pages | 🔐 Generated locally into the profile folder<br>✅ Contains no scripts beyond a retry redirect<br>📝 Terminal and support details come from your profile |
| **🧹 Session Hygiene & Cache Management**<br>✅ Purge disk cache before launch<br>✅ Remove code cache & GPU cache<br>✅ Wipe cookies after close<br>✅ Wipe session storage<br>✅ Wipe local storage<br>✅ Incognito mode option<br>✅ Automatic profile folder creation | 🗑️ Guarantees the client loads your newest deployed assets<br>🔐 Prevents the next shift inheriting the previous login<br>⚡ Three cache locations cleared (`Cache`, `Code Cache`, `GPUCache`)<br>⏳ Session wipe runs after the browser process exits<br>📂 Operates strictly inside the app's own profile folder | 🔒 Deletion scoped to `%LOCALAPPDATA%\WebAppKiosks\<profile>`<br>🚫 Never touches the user's personal Chrome data<br>✅ Requires an isolated profile (documented)<br>⚠️ Session wipe is EXE-runtime only |
| **🌍 Proxy & User-Agent Overrides**<br>✅ Custom proxy server<br>✅ HTTP and SOCKS5 support<br>✅ Custom User-Agent string<br>✅ Blank = direct connection<br>✅ Correct quoting in generated output | 🌐 `--proxy-server=<address>`<br>🕵️ `--user-agent="<string>"` for backends that inspect clients<br>🧩 Blank values emit nothing (clean command line)<br>🔄 Included in every generated format identically | 🔐 Optional, operator-controlled<br>✅ Quoted correctly to avoid argument splitting<br>📝 Preserved per profile for repeat builds |
| **🏷️ EXE Metadata Branding**<br>✅ Company / studio name<br>✅ Product name<br>✅ File description<br>✅ Four-part file & product version<br>✅ Copyright notice<br>✅ Optional UAC elevation manifest | 🪟 Visible in Windows File Properties → Details<br>📋 Shown in Task Manager and Explorer tooltips<br>🔢 Version parser extracts digits and pads to 4 parts<br>🧼 Apostrophes stripped to keep the resource file valid<br>🏢 Professional publisher identity instead of "unknown" | 🔐 Branding only — cannot alter OS behaviour<br>✅ Version string sanitised and normalised<br>⚠️ UAC elevation is opt-in and off by default |
| **🎨 Icon Conversion Pipeline**<br>✅ `.ico` passthrough<br>✅ PNG / JPG / JPEG / BMP / WEBP conversion<br>✅ Multi-resolution ICO output<br>✅ Live thumbnail preview<br>✅ Graceful skip if conversion fails | 🖼️ Sizes generated: 256, 128, 64, 48, 32, 16 px<br>🔍 Explorer, taskbar and Alt-Tab all render crisply<br>📁 Icon copied into the build workspace<br>⚡ Thumbnail updates the moment you browse | 🔐 Local image processing only<br>✅ Build continues iconless rather than failing<br>💡 Square source ≥ 256 px recommended |
| **🗂️ Multi-Client Batch Build**<br>✅ Multi-select profile list<br>✅ Select All / Clear Selection<br>✅ Sequential compilation<br>✅ Per-profile output folders<br>✅ Per-profile deliverable choices<br>✅ Progress logging `[i/n]`<br>✅ Single summary dialog | 🏭 Compile dozens of client launchers unattended<br>📊 Alphabetical processing order<br>🧯 One failure does not abort the run<br>🔒 Main build button locked during batch<br>🔇 Per-build popups suppressed for clean output | 🔐 No cross-profile setting leakage<br>✅ Each profile loaded fresh before building<br>📝 Full per-client log trail<br>⚠️ Every selected profile must be individually valid |
| **🩺 Build Console & Diagnostics**<br>✅ Timestamped log (`[HH:MM:SS]`)<br>✅ Dependency status badge<br>✅ One-click tool installer<br>✅ Browser audit + re-scan<br>✅ Live PyInstaller filtering<br>✅ Clear Log<br>✅ Auto-scroll to latest line | 🔧 Instant visibility into what succeeded or failed<br>📦 `pip install --upgrade pyinstaller pillow` in a background thread<br>🟢 Green "Build Engine Ready" state<br>🟡 Amber missing-dependency state<br>📜 Persistent session history<br>🧾 Every user action recorded | 🔐 Read-only console presentation<br>✅ Installer runs in the active Python environment only<br>📝 Complete diagnostic trail for support tickets |
| **⚡ Build Orchestration & Threading**<br>✅ Non-blocking UI during builds<br>✅ Build-in-progress lock<br>✅ Button state management<br>✅ Sequential helper generation<br>✅ Guaranteed temp cleanup<br>✅ Success and failure dialogs<br>✅ File count reporting | 🧵 All heavy work on daemon threads<br>🖥️ Interface stays responsive throughout<br>🔁 Repeat builds safe (single-flight guard)<br>🧯 Exceptions logged, not swallowed silently<br>📊 Final message states exactly how many files were produced | 🔒 Concurrent builds prevented by design<br>✅ Temp workspace removed in a `finally` block<br>🚫 No partial state left behind |
| **🧠 Intelligent Automation**<br>✅ Title → filename sync<br>✅ Title → profile folder sync<br>✅ Title → EXE product name sync<br>✅ URL scheme auto-completion<br>✅ Slug sanitisation<br>✅ Version normalisation<br>✅ Primary-file auto-resolution | ⌨️ Type the app name once, three fields populate themselves<br>🔗 `hms.client.com` becomes `https://hms.client.com`<br>🧼 `My App (v2)!` becomes a safe filename<br>🔢 `1.0` becomes `1.0.0.0`<br>🎯 Helpers always point at the best available launcher | 🔐 Derived values remain editable<br>✅ Sanitisation prevents invalid Windows filenames<br>👁️ Every derived value visible before building |
| **💾 Configuration Portability**<br>✅ Single-file JSON database<br>✅ Indented, human-readable format<br>✅ Merge-on-import semantics<br>✅ Full-database export<br>✅ Version-control friendly<br>✅ No external database engine | 📦 Move the whole client roster with one file<br>🔄 Restore after reinstalling Windows<br>🧾 Diffable in Git<br>🚫 No server, no service, no schema migration | 🔐 Plain text — review before sharing<br>🚫 Contains no secrets<br>⚠️ Merges overwrite same-named profiles |
| **🛡️ Validation & Failure Safety**<br>✅ Primary-launcher requirement<br>✅ PyInstaller availability check<br>✅ Numeric geometry validation<br>✅ URL scheme normalisation<br>✅ Empty-name fallbacks<br>✅ Missing-folder auto-creation<br>✅ Browser-missing message box | 🚧 Stops builds that would produce nothing usable<br>💬 Clear, actionable error dialogs<br>🔁 Idempotent operations (safe to re-run)<br>📁 Missing directories created on demand<br>🧹 Build workspace always cleaned | 🔒 Fails closed, not silently<br>✅ No destructive operations on user data<br>📝 Every refusal logged or shown |
| **📈 Performance & Reliability**<br>✅ Near-instant startup<br>✅ Instant preset application<br>✅ Real-time preview refresh<br>✅ Efficient JSON persistence<br>✅ Background dependency install<br>✅ Streaming build output<br>✅ No external service dependency | ⚡ Native widgets — no Electron or web runtime<br>💾 Tiny on-disk footprint (single Python file)<br>🔁 Deterministic output for identical settings<br>🌐 Works fully offline (except pip/pyinstaller steps)<br>🧱 Stable under repeated build cycles | 🔐 Runs in user space<br>✅ No background services or scheduled tasks<br>🚫 No outbound telemetry |

---

## 🏆 System Highlights

| 🌟 Category | 🎯 Key Achievements |
|---|---|
| **🎯 Delivery Speed** | Any web app → professional branded Windows launcher in under five minutes, including icon, metadata, offline screen and ZIP packaging |
| **🖥️ Runtime Control** | 12 individual Chromium switches plus free-form flags, three launch modes and precision window geometry — enough to match virtually any client environment |
| **🔁 Repeatability** | 52-field profile database rebuilds an identical launcher months later with one Load + Build |
| **🏭 Scale** | Multi-client batch compilation turns a day of manual packaging into a single supervised run |
| **🛟 Resilience** | Pre-launch reachability checks, a branded self-retrying offline page, crash-bubble suppression and an emergency close utility |
| **🔐 Data Hygiene** | Isolated browser profiles, optional cache purge, cookie/session wiping and incognito mode keep shared terminals clean |
| **🏢 Professional Identity** | Real Windows publisher metadata, multi-resolution icons and a branded offline screen — no "unknown publisher" look |
| **🔍 Transparency** | Full source of every generated script is previewable and copyable before anything is built |
| **🧠 Operator Ergonomics** | Auto-synchronised names, sanitised filenames, tooltips on nearly every control, timestamped diagnostics and threaded builds |
| **🧩 Zero Infrastructure** | One Python file, one JSON database, no services, no accounts, no cloud, no telemetry |

---

## 📦 Generated Artifact Reference

| Artifact | Extension | Producer | Purpose |
|---|---|---|---|
| Primary executable | `.exe` | PyInstaller | Portable, console-free launcher with icon + metadata |
| Batch launcher | `.bat` | Built-in generator | Browser-detecting script with health check |
| Command launcher | `.cmd` | Built-in generator | Same logic, enterprise-friendly extension |
| Silent wrapper | `.vbs` | Built-in generator | Runs the `.bat` with no console flash |
| Shortcut creator | `.bat` | Built-in generator | Creates a Desktop `.lnk` |
| Auto-start installer | `.bat` | Built-in generator | Registers the launcher in the Startup folder |
| Emergency close tool | `.bat` | Built-in generator | Terminates only this app's kiosk processes |
| Delivery archive | `.zip` | `zipfile` (Deflate) | Everything above + client instruction sheet |
| Client instruction sheet | `.txt` | Built-in generator | Branded deployment guide inside the ZIP |
| Profile database | `.json` | Application | All saved client configurations |
| Icon resource | `.ico` | Pillow | Multi-resolution Windows icon (256→16 px) |
| Version resource | `.txt` | Built-in generator | PyInstaller `VSVersionInfo` metadata |
| Offline guard page | `.html` | Runtime (inside `.exe`) | Branded auto-reconnect status screen |

---

## ⚙️ Chromium Switch Reference

| UI Concept | Emitted Switch(es) | Effect |
|---|---|---|
| Full kiosk | `--kiosk` | Borderless, no chrome UI |
| App window | `--app=<url>` | Native-looking window, no URL bar |
| Silent printing | `--kiosk-printing` | Bypasses print preview |
| Isolated profile | `--user-data-dir="…"` | Dedicated browser data folder |
| Incognito | `--incognito` | No persisted session |
| Pinch lock | `--disable-pinch` | Blocks touch zoom |
| Swipe-nav lock | `--overscroll-history-navigation=0` | Blocks swipe back/forward |
| First-run suppression | `--no-first-run` `--no-default-browser-check` | No onboarding prompts |
| Dialog suppression | `--noerrdialogs` `--disable-session-crashed-bubble` `--disable-infobars` | No crash/restore bubbles |
| Autoplay | `--autoplay-policy=no-user-gesture-required` | Audio without interaction |
| Translate suppression | `--disable-features=Translate` | No translate bar |
| Extension blocking | `--disable-extensions` | Clean runtime |
| Maximised | `--start-maximized` | Fills work area |
| Fullscreen start | `--start-fullscreen` | F11-style at launch |
| Certificate bypass | `--ignore-certificate-errors` | Intranet self-signed support |
| UI scale | `--force-device-scale-factor=<n>` | DPI override |
| Proxy | `--proxy-server=<addr>` | Routing override |
| User agent | `--user-agent="<str>"` | Client identity override |
| Window geometry | `--window-size=W,H` `--window-position=X,Y` | Precise placement |
| Custom flags | operator-supplied | Unlimited extension |

---

## 🧱 Technical Architecture

| Layer | Implementation |
|---|---|
| **Presentation** | Tkinter / ttk with `clam` theme, custom style tokens, card frames, `ToolTip` helper class |
| **State** | 30+ `tk.StringVar` / `BooleanVar` bindings, traced for live preview regeneration |
| **Domain logic** | `build_flag_list()` assembles the browser command; `sanitize_slug()` normalises names |
| **Generators** | `generate_batch_content()`, `generate_vbs_content()`, `generate_embedded_python_source()`, `generate_desktop_shortcut_bat()`, `generate_startup_helper_bat()`, `generate_kill_helper_bat()`, `generate_version_info_file()`, `build_offline_fallback_html()`, `generate_readme_text()` |
| **Build pipeline** | `build_single_client_worker()` orchestrates scripts → EXE → helpers → ZIP → cleanup |
| **Compilation** | PyInstaller invoked via `python -m PyInstaller` with `--onefile --noconsole --clean` |
| **Imaging** | Pillow converts any raster logo to a multi-size ICO |
| **Persistence** | `kiosk_clients_db.json` read/written with `json` |
| **Concurrency** | `threading.Thread(daemon=True)` for installs and builds; UI updates marshalled with `root.after()` |
| **Process management** | `subprocess.Popen` for pip, PyInstaller, browsers and PowerShell helpers |
| **Diagnostics** | Timestamped in-memory console widget with dependency and browser audits |

---

## 🎯 Deployment Scenario Coverage

| Scenario | Preset | Critical Settings |
|---|---|---|
| Retail POS / pharmacy receipt counter | POS & Thermal Receipt Terminal | Kiosk + silent printing + isolated profile + pinch/swipe locks |
| Back-office desktop app | Standalone Desktop Web App | App mode + start maximised |
| Public walk-in self-service terminal | Locked Public Self-Service Kiosk | Kiosk + incognito + cache purge + session wipe |
| Hospital / school queue display | Hospital / School Queue Display Screen | Kiosk + autoplay + scale 1.1 |
| LAN app with self-signed HTTPS | Local Intranet / Self-Signed HTTPS App | App mode + ignore cert errors + allow insecure localhost |
| Multi-branch rollout | Presets + Batch Build | Per-branch profile, one compile run |
| Version update push | Any preset + cache purge | Bump version, rebuild, redeploy |

---

## 🔐 Security Posture

| Control | Status |
|---|---|
| Local-only operation | ✅ No cloud, no accounts, no telemetry |
| Profile data sensitivity | ✅ URLs, paths and branding text only — no credentials |
| Client browser isolation | ✅ Dedicated `--user-data-dir` per application |
| Session confidentiality | ✅ Optional incognito + cookie/storage wipe |
| Cache integrity | ✅ Optional purge before every launch |
| Certificate handling | ⚠️ Opt-in bypass — trusted intranets only |
| Executable reputation | ⚠️ Unsigned by default; code-signing recommended for large rollouts |
| Elevation | ⚠️ UAC opt-in, disabled by default |
| OS-level lockdown | ⚠️ Out of scope — kiosk mode is browser-level; combine with Windows Assigned Access for enforcement |
| Destructive operations | ⚠️ Profile Delete has no confirmation — export backups |
| Process control scope | ✅ Emergency tool targets one profile name only |
| Build isolation | ✅ Temporary workspace, always cleaned |

---

## 🧾 Field Reference (52 persisted values)

| Group | Fields |
|---|---|
| Identity | `client_name`, `app_name`, `url`, `output_name`, `output_dir`, `icon_path`, `browser_target` |
| Launch | `launch_mode`, `kiosk_printing`, `isolated_profile`, `profile_folder`, `incognito`, `disable_pinch`, `disable_swipe_nav`, `no_first_run`, `suppress_dialogs`, `autoplay_media`, `disable_translate`, `start_maximized`, `start_fullscreen`, `disable_extensions`, `kill_existing` |
| Display | `custom_geometry`, `win_width`, `win_height`, `win_x`, `win_y`, `scale_factor`, `extra_flags` |
| Network | `health_check`, `health_retries`, `offline_fallback`, `support_phone`, `ignore_cert_errors`, `clear_cache_on_launch`, `clear_session_on_exit`, `proxy_server`, `user_agent` |
| Metadata | `exe_company`, `exe_product`, `exe_desc`, `exe_version`, `exe_copyright`, `uac_admin` |
| Deliverables | `gen_exe`, `gen_bat`, `gen_cmd`, `gen_vbs`, `gen_shortcut_helper`, `add_startup_helper`, `add_kill_helper`, `gen_zip` |

---

## 📋 Requirements Matrix

| Item | Builder Machine | Client Machine |
|---|---|---|
| Windows 10 / 11 | ✅ Recommended | ✅ Required |
| Python 3.8+ with Tkinter | ✅ Required | ❌ Not required |
| PyInstaller | ✅ For `.exe` output only | ❌ Not required |
| Pillow | ✅ For icon conversion only | ❌ Not required |
| Chrome / Edge / Brave | ✅ For testing & audit | ✅ Required (Edge preinstalled) |
| Network access to target URL | ✅ For testing | ✅ Required |
| Administrator rights | ❌ Not required | ❌ Not required (unless UAC enabled) |
| Internet for the builder itself | ❌ Only for pip installs | ❌ Not required |

---

## ⚠️ Known Boundaries

1. Generated artifacts target **Windows**; PyInstaller produces Windows executables only when run on Windows.
2. The launcher **opens an installed browser** — it does not bundle a browser engine.
3. The `.exe` is **not code-signed** by default, so SmartScreen may prompt once.
4. The **offline guard page is `.exe`-only**; script launchers retry then open the URL.
5. **Session wiping is `.exe`-runtime only** and requires the isolated profile.
6. **Profile Delete has no confirmation** — export backups before cleanup.
7. `--ignore-certificate-errors` **weakens TLS validation** — trusted intranets only.
8. Custom CLI flags are **split on spaces**, so values containing spaces can misparse.
9. Kiosk mode is **browser-level**, escapable with `Alt + F4` / `Ctrl+Alt+Del`.
10. The **browser audit reflects the operator's PC**, not the client's.
11. **Presets never modify** identity, paths, metadata, network settings or deliverable selections.
12. **No built-in auto-update** — new builds are delivered as new files.

---

## 🗺️ Module Interaction Map

```text
   Client Identity ─┐
   Launch Mode ─────┤
   Kiosk Switches ──┼──► build_flag_list() ──►  CLI preview
   Display Options ─┤                            │
   Proxy / UA ──────┘                            ▼
                                       ┌───────────────────┐
   Network Guard ─────────────────────►│  BUILD PIPELINE   │
   Offline Screen ────────────────────►│                   │
   Session Hygiene ───────────────────►│  .bat/.cmd/.vbs   │
   Metadata + Icon ───────────────────►│  .exe (PyInstaller)│
   Deliverable Choices ───────────────►│  helpers → ZIP    │
                                       └─────────┬─────────┘
                                                 ▼
                                    Deliverables Folder
                                                 │
                    ┌────────────────────────────┼────────────────────────────┐
                    ▼                            ▼                            ▼
              Client desktop              Startup folder              Emergency tool
              (double-click)              (auto-launch)               (support use)
                    │
                    ▼
        Browser + isolated profile
                    │
        ┌───────────┴────────────┐
        ▼                        ▼
   App reachable            App unreachable
        │                        │
        ▼                        ▼
   Normal operation      Branded offline screen
                         (auto-retry every 5 s)
```

---

## 📊 Compliance & Quality Checklist

| Check | Status |
|---|---|
| Every UI control documented | ✅ |
| Every generated flag documented | ✅ |
| Every output file documented | ✅ |
| Every preset documented | ✅ |
| Every persisted field documented | ✅ |
| Failure modes documented | ✅ |
| Limitations stated honestly | ✅ |
| No invented features | ✅ |
| Client-facing documentation provided | ✅ `CLIENT-README.md` |
| Bilingual documentation provided | ✅ `README.md` |

---

### 👨‍💻 Created By

<div align="center">

**Yasin Ullah** — Bannu Software Solutions
📱 WhatsApp: **0336-1593533**

*Building professional client delivery experiences for Pakistan and beyond.*

</div>

---
