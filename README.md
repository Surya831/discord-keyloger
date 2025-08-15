# 🔍 Authorized Keylogger with Discord Integration

**Author:** Surya831  
**Version:** 1.0  
**License:** For educational and authorized use only.

---

## 📌 Overview
This is a **Python-based keylogger** that captures keystrokes along with:
- Active application name
- Current window title
- Timestamp of when keys are pressed

The collected logs are **sent automatically to a Discord channel** via webhook for monitoring purposes.  
This tool is designed for **ethical use only** — such as in cybersecurity labs, on your own systems, or with explicit consent.

---

## ⚠ Legal Disclaimer
> Unauthorized use of keyloggers is illegal in many countries.  
> This project is **strictly for educational purposes** and **authorized testing** only.  
> The author is **not responsible** for any misuse of this software.

---

## ✨ Features
- Logs **every key press** with timestamps.
- Captures **active app process name** and **window title**.
- Sends logs to a **Discord channel** via webhook.
- Runs **silently in the background** as `.pyw` (no console window).
- Hotkey to stop logging (**Ctrl + Alt + P**).

---

## 🛠 Installation

### **Windows Setup**
1. Clone this repository:
   ```bash
   git clone https://github.com/Surya831/keylogger.git
   cd keylogger
   # 🔍 Authorized Keylogger with Discord Integration

**Author:** Surya831  
**Version:** 1.0  
**License:** For educational and authorized use only.

---

## 📌 Overview
This is a **Python-based keylogger** that captures keystrokes along with:
- Active application name
- Current window title
- Timestamp of when keys are pressed

The collected logs are **sent automatically to a Discord channel** via webhook for monitoring purposes.  
This tool is designed for **ethical use only** — such as in cybersecurity labs, on your own systems, or with explicit consent.

---

## ⚠ Legal Disclaimer
> Unauthorized use of keyloggers is illegal in many countries.  
> This project is **strictly for educational purposes** and **authorized testing** only.  
> The author is **not responsible** for any misuse of this software.

---

## ✨ Features
- Logs **every key press** with timestamps.
- Captures **active app process name** and **window title**.
- Sends logs to a **Discord channel** via webhook.
- Runs **silently in the background** as `.pyw` (no console window).
- Hotkey to stop logging (**Ctrl + Alt + P**).

---

## 🛠 Installation

### **Windows Setup**
1. Clone this repository:
   ```bash
   git clone https://github.com/Surya831/keylogger.git
   cd keylogger
Run the setup batch file:

setup_client_discord.bat


When prompted, paste your Discord webhook URL.

The logger will start running silently.
🎯 How to Get a Discord Webhook

Open Discord → Go to your server.

Create or choose a text channel.

Go to Edit Channel → Integrations → Webhooks.

Create a new webhook and copy the URL.

Paste it when running setup_client_discord.bat.

⌨ Hotkey to Stop

While running, press:

Ctrl + Alt + P


The program will stop logging and exit.

📂 Project Structure
├── client.pyw                # Main keylogger script
├── setup_client_discord.bat  # Installer and launcher
├── start_client_hidden.bat   # Starts logger silently
├── config.txt                # Stores Discord webhook URL
└── logs/                     # Local logs before sending

🚀 Roadmap

 Option to send logs via email.

 Multi-OS support (Linux, macOS).

 Encrypted log storage before sending.

 Real-time monitoring dashboard.

📜 License

This project is released under the MIT License for educational use.
See LICENSE for details.
