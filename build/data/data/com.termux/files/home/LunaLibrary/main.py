import sys
import os
import time
import sqlite3

# --- LUNA LIBRARY CORE SETUP ---
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
INTERNAL_CORE_PATH = os.path.join(CORE_DIR, 'internal_core')
DB_PATH = os.path.join(CORE_DIR, 'luna_data.db')

# Ensure internal_core is the first path
if INTERNAL_CORE_PATH not in sys.path:
    sys.path.insert(0, INTERNAL_CORE_PATH)
    # print(f"[CORE] Added internal dependency path: {INTERNAL_CORE_PATH}") # Commented out for cleaner output

os.environ['LUNA_CORE_MODE'] = "OFFLINE_SELF_HOSTED"
os.environ['LUNA_CORE_START_TIME'] = str(int(time.time()))

print(f"[CORE] Running in mode: {os.environ.get('LUNA_CORE_MODE')}")
print("-" * 30)

# --- CORE UTILITIES ---
def db_query(sql, params=()):
    """A safe utility function for database interaction."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor.fetchall()
    except Exception as e:
        print(f"[DB ERROR] Operation failed: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_app_state(key):
    """Reads a single key from the app_state table."""
    result = db_query("SELECT value FROM app_state WHERE key = ?", (key,))
    return result[0][0] if result else None

def set_app_state(key, value):
    """Writes a single key/value pair to the app_state table."""
    db_query("INSERT OR REPLACE INTO app_state (key, value) VALUES (?, ?)", (key, value))

# --- CORE APPLICATION LOGIC ---

def run_test_app_a():
    """Confirms current environment status."""
    print("[App: TestApp_A] RUNNING: Environment Check...")
    try:
        # Import the stable wrapper
        import requests_core as requests
        
        # Database Read Demonstration
        core_version = get_app_state('core_version')
        print(f"  -> State Read: Core Version is {core_version}")
        
        # Mocked Network Call Demonstration
        response = requests.get("https://api.your-app-data.com/v1/status")
        
        print(f"  -> Mock Call: Status {response.status_code} ({response.reason})")
        print("  -> App A Complete.")
        
    except Exception as e:
        print(f"[App: TestApp_A] CRASHED: {e}")

def run_test_app_b():
    """Demonstrates a state change and persistence."""
    print("[App: TestApp_B] RUNNING: Offline Workflow Demonstration...")
    
    # 1. READ current run count from DB
    run_count = get_app_state('run_count')
    if run_count is None:
        run_count = 0
    else:
        run_count = int(run_count)

    print(f"  -> Initial State: App B has run {run_count} times.")

    # 2. Simulate "fetching" new data (via mock)
    import requests_core as requests
    response = requests.post("https://api.your-app-data.com/v1/update_state", data={'status': 'ok'})
    
    # 3. Process the (mocked) response and update state
    if response.status_code == 200:
        new_run_count = run_count + 1
        set_app_state('run_count', str(new_run_count))
        print(f"  -> State Update: Run count incremented to {new_run_count}.")
    else:
        print("  -> ERROR: Mock service failed.")
    
    print("  -> App B Complete.")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("[CORE] Luna Libraryore Initializing...")
    
    # Ensure a clean run_count exists for App B demo
    if get_app_state('run_count') is None:
        set_app_state('run_count', '0')
        print("[DB] Initializing 'run_count' to 0.")
        
    run_test_app_a()
    print("-" * 30)
    run_test_app_b()
    print("-" * 30)
    
    # Run App B again to prove persistence
    print("RUNNING App B SECOND TIME (Testing Persistence)...")
    run_test_app_b()
    
    print("-" * 30)
    print("[CORE] Initialization complete. Core successfully running multiple self-hosted applications.")

