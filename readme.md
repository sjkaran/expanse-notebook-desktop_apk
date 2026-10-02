<div align="center">

# 🧾 BIZ-TRACK — The Business Book

### Visionary Business Suite v4.2

**Minimal. Reliable. Offline. Personalized.**

A desktop application for small businesses to record daily income and expenses, understand performance through visual analytics, and export monthly reports to Excel — all stored locally on your own computer.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![UI](https://img.shields.io/badge/UI-CustomTkinter-2CC985)
![Database](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Charts](https://img.shields.io/badge/Charts-Matplotlib-11557C)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Packaging](https://img.shields.io/badge/Packaged%20with-PyInstaller-orange)

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Screenshots](#-screenshots)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [User Guide](#-user-guide)
- [Data Storage & Privacy](#-data-storage--privacy)
- [Packaging as a Desktop Application](#-packaging-as-a-desktop-application-pyinstaller)
- [Creating a Windows Installer (Optional)](#-creating-a-windows-installer-optional)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**BIZ-TRACK** is a production-ready, offline desktop application built for small business owners — cafés, grocery shops, juice bars, stalls, and similar businesses — who want a simple way to track money without a cloud account, a subscription, or an internet connection.

Enter each sale and expense as it happens, and the app does the rest: it totals your day, builds monthly pivot reports, draws analytical charts, and exports clean Excel sheets that are ready to hand to an accountant or use for tax filing.

**Why BIZ-TRACK?**

| | |
|---|---|
| 🔒 **Private** | Your data lives in a single local SQLite file. Nothing is uploaded anywhere. |
| ⚡ **Fast to use** | Keyboard-driven data entry — type an amount, press `Enter`, done. |
| 📊 **Insightful** | Pie charts and cash-flow bars reveal where money goes and what remains as profit. |
| 📁 **Tax-ready** | One-click monthly Excel export with per-category columns and totals. |
| 🛡️ **Safe** | Built-in database backup and a triple-confirmation guard on destructive actions. |

---

## 📸 Screenshots

> The screenshots below use sample data for a demo business called *"Karan's Cafe"*.

### 1. Dashboard — Daily Transaction Ledger

The home screen. Log an entry in seconds and see the day's **Total Income**, **Total Expense**, and **Net Balance** update instantly in the cards at the top right.

![Dashboard](assets/Screenshot%202026-10-02%20122020.png)

- Enter an **amount**, choose **Expense** or **Profit**, pick (or type) a **category**, choose the **date**, and press **ADD ENTRY +** or hit `Enter`.
- Switch the working date between *Today*, *Yesterday*, or any custom date (`DD-MM-YYYY`).
- Every entry is listed with its date, time, type, category, and amount, color-coded green (income) and red (expense), with a **Delete** button on each row.

---

### 2. Visual Analytics & Trends

Understand your month at a glance with interactive Matplotlib charts.

![Visual Analytics](assets/Screenshot%202026-10-02%20122047.png)

- **Operational Expense Breakdown** — a pie chart of spending per category.
- **Revenue Distribution** — shows how total sales are split between expenses and the remaining **Net Profit** slice, which is highlighted.
- **Daily Cash Flow Tracker** — a bar chart comparing income and expenses for every day of the month.
- Toggle chart labels between **Percentages (%)** and **actual currency values** with one button.
- Each chart includes the Matplotlib toolbar to zoom, pan, and save the chart as an image.

---

### 3. Reports & Export

A spreadsheet-style monthly report, previewed right inside the app before you export it.

![Monthly Reports](assets/Screenshot%202026-10-02%20122201.png)

- Pick a month and click **Load Preview** to build a pivot table: one row per day, one column per category.
- Automatically calculated **Total Expense**, **Total Income**, and **Net Margin** columns, plus a **GRAND TOTAL** row.
- Click any cell to open a detail pop-up where you can **Edit** or **Delete** the individual transactions behind that number.
- Use the **Zoom −/+** controls to make the table comfortable to read.
- Click **Download Excel** to save the report as a `.xlsx` file (default name: `Monthly_Report_YYYY-MM.xlsx`) with auto-fitted column widths.

---

### 4. System Settings

Configure the app, protect your data, and manage categories.

![System Settings](assets/Screenshot%202026-10-02%20122130.png)

- **Business Name** — shown as the heading on the Dashboard.
- **Currency Symbol** — use `₹`, `$`, `€`, `£`, or anything else; applied across the whole app.
- **Data Protection** — create a timestamped backup of your database anywhere you choose.
- **Danger Zone** — wipe all transactions to start a fresh accounting period (protected by multiple confirmations).
- **Category Manager** — rename or remove income and expense categories.

---

## ✨ Features

### Transaction Management
- Add, view, and delete daily income (**Profit**) and **Expense** entries.
- Create custom categories on the fly — just type a new name when adding an entry.
- Back-date or review entries using *Today*, *Yesterday*, or a custom date.
- Full keyboard navigation: `Enter` to submit, arrow keys to move between fields and cycle through options.
- Confirmation prompt before any deletion.

### Analytics
- Monthly expense breakdown, revenue distribution, and daily cash-flow charts.
- Percentage / currency-value label toggle.
- Zoom, pan, and save charts using the built-in Matplotlib toolbar.

### Reports & Excel Export
- Monthly pivot report by day and category with totals and net margin.
- Edit or delete individual transactions directly from the report view.
- Export to Excel (`.xlsx`) with auto-sized columns — ideal for accountants and tax filing.

### Settings & Data Safety
- Custom business name and currency symbol.
- One-click timestamped database backups (`Backup_BusinessData_YYYYMMDD_HHMMSS.db`).
- **Rename a category** and all of its historical transactions update with it, so reports never break.
- **Remove a category** from the dropdown list without losing historical data.
- **Format Database** safely resets transaction history while keeping your settings and categories (see [below](#-data-storage--privacy)).

### Out of the Box
- Dark, modern UI with a green accent theme.
- Preloaded starter categories — Expense: *Fruits, Milk, Grocery*; Income: *Online Payments, Cash Payments*.
- Default currency of `₹` (changeable at any time).
- 100% offline.

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| GUI | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) 5.2.2 |
| Database | SQLite (`sqlite3`, standard library) |
| Data processing | pandas, NumPy |
| Charts | Matplotlib (TkAgg backend) |
| Excel export | openpyxl |
| Packaging | PyInstaller |

---

## 📂 Project Structure

```
expanse-notebook-desktop_apk/
├── assets/                     # README screenshots
├── desk_app_ext/
│   ├── main.py                 # Application entry point & all UI pages
│   ├── backend.py              # SQLite data layer & analytics queries
│   └── icon.ico                # Window icon (loaded at runtime)
├── icons/
│   ├── biz-track.ico           # Multi-resolution icon for the .exe
│   └── buisness-tracker_icon.ico
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

**Architecture at a glance**

- `backend.py` → `BackendManager`: owns the database connection, creates tables on first launch, seeds default categories and currency, and provides all queries (transactions, category breakdown, daily trends, monthly pivots, backup, and format).
- `main.py` → `BusinessTrackerApp`: the main window with a sidebar and four pages — `TransactionPage` (Dashboard), `VisualsPage` (Analytics & Trends), `ReportsPage` (Reports & Export), and `SettingsPage` (System Settings).

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11 or newer** (tested on 3.12) — [python.org/downloads](https://www.python.org/downloads/)
- **Tkinter** — included with the Windows and macOS Python installers. On Debian/Ubuntu install it with:
  ```bash
  sudo apt install python3-tk
  ```
- **Git**

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/sjkaran/expanse-notebook-desktop_apk.git
cd expanse-notebook-desktop_apk

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
#    Windows (CMD / PowerShell):
venv\Scripts\activate
#    Linux / macOS:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Run from source

```bash
cd desk_app_ext
python main.py
```

On first launch, the app automatically creates its database (`business_data.db`) and seeds the default categories.

---

## 📖 User Guide

### Recording a transaction
1. Open **Dashboard**.
2. Type the **amount**.
3. Choose **Expense** (money out) or **Profit** (money in).
4. Select a **category** from the list — or type a new one to create it.
5. Pick the **date** (defaults to today).
6. Press **ADD ENTRY +** or hit `Enter`.

### Keyboard shortcuts (Dashboard)

| Key | Action |
|---|---|
| `Enter` | Add the entry |
| `→` / `←` | Move between Amount → Type → Category |
| `↑` / `↓` | Cycle through Type or Category options |

### Viewing analytics
Open **Analytics & Trends**, select a month, and scroll through the charts. Use the purple button to switch between percentage and currency labels.

### Exporting a monthly report
1. Open **Reports & Export** and select a month.
2. Click **Load Preview** and review the table.
3. Click any cell to inspect, edit, or delete the underlying transactions.
4. Click **Download Excel** and choose where to save the `.xlsx` file.

### Starting a new accounting period
Go to **System Settings → Danger Zone → FORMAT DATABASE**. You will be asked to:
1. Confirm that you have exported all monthly Excel reports.
2. Optionally create a safety backup (`.db`) first.
3. Type the word `DELETE` to confirm.

Only **transactions** are erased. Your business name, currency, and categories are preserved.

---

## 🔐 Data Storage & Privacy

- All data is stored in a single SQLite file: **`business_data.db`**.
- The app makes **no network connections** — your financial data never leaves your machine.
- The database contains three tables: `transactions`, `categories`, and `settings`.

> **📌 Where is `business_data.db` created?**
> The database file is created in the **folder the application is launched from** (its working directory). For a packaged app, keep the application in a folder where your user account has write permission (for example `D:\BizTrack` or your user profile) — **not** in a protected location such as `C:\Program Files`. The installer in [this guide](#-creating-a-windows-installer-optional) is configured to do this for you.

**Backups:** use **System Settings → Backup Database Now** regularly and store copies on a separate drive or cloud folder. To restore, close the app and replace `business_data.db` with a backup file (renamed to `business_data.db`).

---

## 📦 Packaging as a Desktop Application (PyInstaller)

Follow these steps to turn BIZ-TRACK into a standalone application that runs on machines **without Python installed**.

> ⚠️ PyInstaller is **not a cross-compiler**. Build on the operating system you are targeting: build on Windows for a Windows `.exe`, on Linux for a Linux binary, and on macOS for a `.app`.

### Step 1 — Prepare the build environment

From the project root, with your virtual environment activated:

```bash
pip install -r requirements.txt
pip install --upgrade pyinstaller
```

### Step 2 — Build the application

Run **one** of the commands below from the **project root** (the folder that contains `desk_app_ext/` and `icons/`).

#### ✅ Recommended: folder build (`--onedir`)

Starts faster, is easier to debug, and triggers fewer antivirus false positives. Best choice for distribution with an installer.

**Windows (CMD or PowerShell)**
```bash
pyinstaller --noconfirm --clean --onedir --windowed --name BizTrack --icon "icons\biz-track.ico" --collect-all customtkinter --hidden-import openpyxl --paths desk_app_ext --add-data "desk_app_ext\icon.ico;." desk_app_ext\main.py
```

**Linux / macOS**
```bash
pyinstaller --noconfirm --clean --onedir --windowed --name BizTrack --icon "icons/biz-track.ico" --collect-all customtkinter --hidden-import openpyxl --paths desk_app_ext --add-data "desk_app_ext/icon.ico:." desk_app_ext/main.py
```
*(On macOS, use an `.icns` icon file instead of `.ico`. The `--icon` option is ignored on Linux.)*

#### Alternative: single-file build (`--onefile`)

Produces one portable executable. Startup is slower because it unpacks itself to a temporary folder on every launch.

**Windows**
```bash
pyinstaller --noconfirm --clean --onefile --windowed --name BizTrack --icon "icons\biz-track.ico" --collect-all customtkinter --hidden-import openpyxl --paths desk_app_ext --add-data "desk_app_ext\icon.ico;." desk_app_ext\main.py
```

### Step 3 — Understand the flags

| Flag | Why it is needed |
|---|---|
| `--onedir` / `--onefile` | Output a folder of files, or a single executable |
| `--windowed` | Hides the console window — required for a GUI app |
| `--name BizTrack` | Names the executable `BizTrack` (`BizTrack.exe` on Windows) |
| `--icon icons\biz-track.ico` | Sets the executable's icon (multi-resolution, up to 256×256) |
| `--collect-all customtkinter` | **Essential.** Bundles CustomTkinter's theme JSON files and assets; without it the app crashes at startup |
| `--hidden-import openpyxl` | pandas selects the Excel engine by name at runtime (`engine='openpyxl'`), so PyInstaller cannot detect it automatically |
| `--paths desk_app_ext` | Lets PyInstaller find `backend.py`, which `main.py` imports |
| `--add-data "…icon.ico;."` | Bundles the window icon that `main.py` loads at runtime. Use `;` on Windows and `:` on Linux/macOS |

### Step 4 — Find your build

```
dist/
└── BizTrack/
    ├── BizTrack.exe        ← your application (Windows)
    └── _internal/          ← bundled libraries and assets (keep next to the .exe)
```

For `--onefile` builds, the single `dist/BizTrack.exe` is created instead. Intermediate files are placed in `build/` and a `BizTrack.spec` file is generated.

### Step 5 — Test the build

1. Copy `dist/BizTrack/` to a **writable** folder (e.g. `D:\BizTrack`).
2. Double-click `BizTrack.exe`.
3. Run through this checklist:
   - [ ] Window opens with the correct icon and the **BIZ-TRACK** sidebar
   - [ ] A transaction can be added and deleted
   - [ ] **Analytics & Trends** draws all charts
   - [ ] **Reports & Export → Download Excel** creates a valid `.xlsx`
   - [ ] **Backup Database Now** creates a `.db` file
   - [ ] `business_data.db` appears next to the app and survives a restart

For ideal testing, also try the build on a clean machine (or a fresh Windows VM) that has no Python installed.

### Step 6 — Rebuild repeatably with the `.spec` file

After the first build, PyInstaller writes `BizTrack.spec`. Commit it so every release is built identically, and rebuild with:

```bash
pyinstaller --noconfirm --clean BizTrack.spec
```

Edit the `.spec` file whenever you need to add data files, hidden imports, or change the icon — you no longer need to retype long command lines.

### Step 7 — Distribute

- **Zip** the `dist/BizTrack` folder and share it, **or**
- Build a proper installer — see the next section.

Add these to `.gitignore` so build output is never committed:

```
build/
dist/
```

---

## 🪟 Creating a Windows Installer (Optional)

For a professional "Next → Next → Finish" setup experience, wrap the `--onedir` build with [Inno Setup](https://jrsoftware.org/isinfo.php) (free).

1. Build the app using the **recommended `--onedir` command** above.
2. Install Inno Setup and save the following as `installer.iss` in the project root:

```ini
[Setup]
AppName=BIZ-TRACK
AppVersion=4.2
AppPublisher=Karan
DefaultDirName={autopf}\BizTrack
DefaultGroupName=BIZ-TRACK
OutputDir=installer_output
OutputBaseFilename=BizTrack-Setup-4.2
SetupIconFile=icons\biz-track.ico
UninstallDisplayIcon={app}\BizTrack.exe
Compression=lzma2
SolidCompression=yes
; Per-user install keeps the app folder writable, so the database can be created beside the app
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
Source: "dist\BizTrack\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\BIZ-TRACK"; Filename: "{app}\BizTrack.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\BIZ-TRACK"; Filename: "{app}\BizTrack.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\BizTrack.exe"; Description: "Launch BIZ-TRACK"; Flags: nowait postinstall skipifsilent
```

3. Open `installer.iss` in Inno Setup and press **Compile** (or run `iscc installer.iss`).
4. Your installer is created at `installer_output\BizTrack-Setup-4.2.exe`.

**Good to know:** the installer does not ship a database, so **upgrading to a newer version never overwrites the user's `business_data.db`**.

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| App closes instantly or shows a theme/JSON error | Make sure `--collect-all customtkinter` is in your build command |
| `ModuleNotFoundError: backend` | Add `--paths desk_app_ext` and run the command from the project root |
| Excel export fails with an engine / `openpyxl` error | Add `--hidden-import openpyxl` |
| Window shows the default icon | Confirm `desk_app_ext/icon.ico` is bundled with `--add-data` (`;` on Windows, `:` on Linux/macOS) |
| Error when saving data / database not created | The app folder is not writable. Move it out of `C:\Program Files`, or use the installer above |
| To see the real error message | Rebuild **without** `--windowed` so a console shows the traceback |
| Antivirus flags the `.exe` | Common for unsigned PyInstaller apps, especially `--onefile`. Use `--onedir`, build with a fresh PyInstaller version, and consider code-signing |
| Large output size | Build in a clean virtual environment containing only the project's dependencies |
| `pip install -r requirements.txt` fails on an old Python | The pinned NumPy/pandas versions require Python 3.11+ |

---

## 🤝 Contributing

Contributions, bug reports, and feature ideas are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m "Add amazing feature"`
4. Push the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---
<!--
## 📄 License

No license has been specified for this project yet. Add a `LICENSE` file to define how others may use, modify, and distribute it.

---
-->
<div align="center">

**Built with ❤️ by [Karan](https://github.com/sjkaran)**

*Track smarter. Grow faster.*

</div>
