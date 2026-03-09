# File Integrity Monitoring (FIM) System

This project demonstrates the development of a **File Integrity Monitoring (FIM) tool** built in Python. The application monitors selected files and directories for unauthorized changes by comparing **cryptographic hashes** and detecting filesystem events in real time.

The project also includes a **graphical dashboard interface** built with Tkinter to manage monitored paths, capture baselines, and visualize alerts.

---

# 🛠️ Project Overview

This project simulates a simplified **host-based integrity monitoring system** similar to tools used in real-world security environments.

The system monitors files and folders and alerts the user if any unexpected changes occur.

### Key Features

* File integrity monitoring using **SHA-256 hashing**
* Real-time filesystem monitoring
* Detection of file creation, modification, deletion, and renaming
* Alert logging for detected events
* Graphical dashboard for monitoring activity
* Persistent storage of monitored paths and alerts

---

# 📜 Step-by-Step Implementation

---

# 1. Building the File Integrity Monitoring Engine

### Hash-Based Integrity Verification

The core of the system relies on **cryptographic hashing**.

For each monitored file, the application generates a **SHA-256 hash**, which uniquely represents the file contents.

Example:

```
file.txt → SHA256 hash
config.ini → SHA256 hash
```

If a file is modified, the generated hash will differ from the stored hash, allowing the system to detect the change.

---

### Baseline Creation

Before monitoring can begin, the system must capture a **baseline** of all monitored files.

The baseline process performs the following steps:

1. Scan all monitored paths
2. Identify all files inside those paths
3. Generate SHA-256 hashes for each file
4. Store the hashes for future comparison

Baseline information is stored in:

```
baseline.json
```

Example structure:

```
{
 "C:\\monitor\\file.txt": "a92f1c2e9f34...",
 "C:\\monitor\\config.ini": "91fa22b37c89..."
}
```

This baseline represents the **trusted state of the system**.

---

# 2. Implementing Real-Time File Monitoring

### File System Event Detection

The project uses the **Watchdog Python library** to monitor filesystem events in real time.

The monitoring engine detects the following events:

* File Created
* File Modified
* File Deleted
* File Renamed / Moved

When an event occurs:

1. The system generates a new hash for the file.
2. The hash is compared with the baseline hash.
3. If the hashes differ, an alert is generated.

Example alert:

```
MODIFIED
C:\Users\user\test.txt
a92f1c2e9f... -> 5b98ac1f3a...
```

---

# 3. Implementing Alert Logging

Every detected event is recorded for future analysis.

Alert information is stored in:

```
alerts_log.json
```

Each alert includes:

* Timestamp
* Event type
* File path
* Hash difference (if applicable)

Example alert entry:

```
{
 "time": "2026-03-08 14:32:11",
 "type": "MODIFIED",
 "path": "C:\\monitor\\test.txt",
 "detail": "a92f1c2e9f... -> 5b98ac1f3a..."
}
```

This allows the user to review **historical security events**.

---

# 4. Building the Graphical Dashboard

To improve usability, the monitoring system includes a **graphical user interface built with Tkinter**.

The interface is divided into three main sections:

* Dashboard
* Paths
* Settings

---

## Dashboard Page

The Dashboard is the main monitoring interface.

It allows the user to:

* Capture the file integrity baseline
* Start or stop monitoring
* View alerts in real time

Alerts are displayed in a list and **color-coded by event type**.

Dashboard Screenshot

---

## Paths Page

The Paths section allows users to manage which files or directories are monitored.

Users can:

* Add files
* Add folders
* Remove monitored paths

All monitored paths are stored in:

```
paths.json
```

Paths Page Screenshot

---

## Settings Page

The Settings page is included as a placeholder for future configuration options.

Potential future features include:

* Alert filtering
* Log export options
* Notification settings

Settings Page Screenshot

---

# 5. Monitoring Workflow

The monitoring workflow follows these steps:

1. The user adds files or folders to monitor.
2. The system captures a **baseline of file hashes**.
3. Monitoring begins using filesystem observers.
4. When a file event occurs:

   * A new hash is generated
   * The hash is compared with the stored baseline
5. If the file integrity changes, an **alert is generated and logged**.

---

# 🧱 Project Structure

```
FIM Project
│
├── gui.py                # Main GUI application
├── monitor.py            # Core monitoring engine
├── dashboard.py          # Monitoring dashboard
├── paths.py              # Path management interface
├── settings.py           # Settings page
├── paths_handler.py      # Path storage and management
│
├── baseline.json         # File integrity baseline
├── alerts_log.json       # Alert log
└── paths.json            # Stored monitored paths
```

---



# ✅ Results

The project successfully demonstrates:

* A working **File Integrity Monitoring system**
* Real-time filesystem event detection
* Hash-based file integrity verification
* Security alert generation and logging
* A graphical monitoring dashboard

This lab simulates functionality commonly used in **Host-based Intrusion Detection Systems (HIDS)**.

---

# 🔐 Security Concepts Demonstrated

This project demonstrates several important cybersecurity concepts:

* File Integrity Monitoring (FIM)
* Cryptographic hashing (SHA-256)
* Endpoint monitoring
* Event-driven security detection
* Security alert logging
* Defensive security automation

These concepts are commonly used in tools such as:

* OSSEC
* Wazuh
* Tripwire

---

# 🚀 Future Improvements

Possible improvements for future versions include:

* Email or Slack alert notifications
* SIEM integration
* Database-based logging
* File whitelist functionality
* Exportable incident reports
* Real-time monitoring statistics
* Background monitoring service




Developed to demonstrate **blue team monitoring and detection engineering concepts using Python**.
