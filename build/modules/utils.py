# LunaLibrary/build/modules/utils.py
import datetime
import os

LOG_FILE = os.path.expanduser("~/LunaLibrary/build/data/luna.log")

def log(message):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[LOG] {message}")

def greet(name):
    return f"Hello, {name}! 🌟"
