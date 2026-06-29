# Secure File Transfer Monitoring System

Version: 1.0.0

Status: Stable Release

## Project Overview

The Secure File Transfer Monitoring System is a cybersecurity-focused application developed using Python, Flask, SQLite, Watchdog, Bootstrap, and Chart.js. It monitors file transfer and file system activities in real time, detects file creation, modification, deletion, and movement events, verifies file integrity using SHA-256 hashing, identifies sensitive and unauthorized file access, stores security events in a SQLite database, generates audit reports, and provides an interactive web dashboard for monitoring, analytics, alerts, and security reporting.

The project demonstrates practical concepts used in File Integrity Monitoring (FIM), Host-Based Intrusion Detection Systems (HIDS), and Security Operations Center (SOC) environments.


---

## Features

* Secure User Authentication
* Real-Time File Monitoring
* File Creation Detection
* File Modification Detection
* File Deletion Detection
* File Move Detection
* Sensitive File Identification
* Unauthorized Access Detection
* SHA-256 File Integrity Verification
* User and Process Tracking
* SQLite Database Logging
* Dashboard Analytics
* Security Alerts
* Search and Filter Events
* Interactive Charts
* PDF Report Generation
* Excel Report Generation
* CSV Report Generation
* REST API Support
* Responsive Bootstrap Dashboard


---

## Technologies Used

### Programming Language

* Python 3

### Backend

* Flask
* SQLite3
* Watchdog
* Pandas
* OpenPyXL
* ReportLab
* psutil

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Chart.js
* Bootstrap Icons


---

## Project Workflow

1. User logs into the monitoring dashboard.
2. The monitoring engine continuously watches the configured directory.
3. File creation, modification, deletion, and movement events are detected in real time.
4. SHA-256 hashes are generated to verify file integrity.
5. Sensitive and unauthorized file access is identified.
6. User and process information is recorded for each event.
7. All security events are stored in the SQLite database.
8. Dashboard statistics, analytics, and alerts are updated.
9. Security reports can be exported in PDF, Excel, and CSV formats.


---

## Installation

### Clone the Project

```bash
git clone <repository-url>
cd Secure-File-Transfer-Monitoring-System
```

### Create a Virtual Environment

```bash
python3 -m venv venv
```

### Activate Virtual Environment

#### Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```


---

## Running the Project

Start the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

Login using your configured administrator credentials.


---

## Dashboard Modules

* Dashboard
* Events
* Analytics
* Alerts
* Reports
* Settings

---

## Security Features

* Real-Time File Monitoring
* File Integrity Monitoring (FIM)
* SHA-256 Integrity Verification
* Sensitive File Detection
* Unauthorized Access Detection
* User Activity Tracking
* Process Monitoring
* SQLite Audit Logging
* Security Analytics Dashboard
* Alert Management

---

## Reports

The system supports exporting security audit logs in multiple formats:

* PDF Security Audit Report
* Microsoft Excel Report
* CSV Report

---

## Future Enhancements

* Email Alert Notifications
* Role-Based Access Control (RBAC)
* Live Dashboard Updates using WebSockets
* Docker Deployment
* Cloud Database Support
* SIEM Integration
* Threat Intelligence Integration
* Malware Detection Rules


---

## Author

**Harshal Suresh Gaddekar**

Developed as part of a cybersecurity internship project to demonstrate practical implementation of file monitoring, file integrity verification, security event logging, analytics, and audit reporting using Python and Flask.

---

## License

This project is intended for educational, internship, and professional portfolio purposes.
