import json
import os
from datetime import datetime, timedelta

# Base directory and file
BASE = os.path.expanduser("~/LunaLibrary/data")
FILE = os.path.join(BASE, "luna_memory.json")
os.makedirs(BASE, exist_ok=True)

# Default memory expiration (optional, in days)
DEFAULT_EXPIRATION_DAYS = None  # Set to e.g. 30 for auto-forgetting after 30 days


def load() -> dict:
    """Load the memory from file safely."""
    if not os.path.exists(FILE):
        return {}
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: Memory file corrupted. Resetting memory.")
        return {}


def save(mem: dict):
    """Save memory to file safely."""
    try:
        with open(FILE, "w") as f:
            json.dump(mem, f, indent=2)
    except IOError as e:
        print(f"Error saving memory: {e}")


def _clean_expired(mem: dict) -> dict:
    """Remove expired memories if expiration is set."""
    if DEFAULT_EXPIRATION_DAYS is None:
        return mem
    now = datetime.utcnow()
    expired_keys = []
    for k, entries in mem.items():
        new_entries = []
        for entry in entries:
            ts = datetime.fromisoformat(entry["timestamp"])
            if now - ts < timedelta(days=DEFAULT_EXPIRATION_DAYS):
                new_entries.append(entry)
        if new_entries:
            mem[k] = new_entries
        else:
            expired_keys.append(k)
    for k in expired_keys:
        del mem[k]
    return mem


def remember(k: str, v: str, mood: str = "neutral"):
    """
    Remember a value under a key with timestamp and optional mood.
    Stores multiple entries per key.
    """
    mem = load()
    mem = _clean_expired(mem)
    entry = {
        "value": v,
        "timestamp": datetime.utcnow().isoformat(),
        "mood": mood
    }
    if k in mem:
        mem[k].append(entry)
    else:
        mem[k] = [entry]
    save(mem)


def recall(k: str, latest: bool = True):
    """
    Recall a memory by key.
    Returns a dict with value and mood.
    If latest=True, returns the most recent entry.
    If latest=False, returns all entries.
    """
    mem = load()
    mem = _clean_expired(mem)
    if k not in mem:
        return None
    if latest:
        return mem[k][-1]
    return mem[k]


def recall_all():
    """Return the full memory dict with moods."""
    mem = load()
    mem = _clean_expired(mem)
    return mem


# Optional demo / test code
if __name__ == "__main__":
    # Example usage
    remember("last_command", "Play music", mood="happy")
    remember("last_command", "Turn off lights", mood="calm")

    # Recall latest
    entry = recall("last_command")
    if entry:
        print("Latest memory:", entry["value"], entry["mood"])

    # Recall all entries
    all_entries = recall("last_command", latest=False)
    for e in all_entries:
        print("Memory:", e["value"], e["mood"])
    
    # Full memory dump
    print("Full memory:", recall_all())
