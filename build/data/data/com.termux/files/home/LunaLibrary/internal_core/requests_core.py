import os
import json
import time

# For the mocked Response object
try:
    from requests.models import Response
    from requests.structures import CaseInsensitiveDict
except ImportError:
    # Fallback definition if sub-dependencies fail (e.g., urllib3, though unlikely now)
    class Response:
        def json(self): return {}
    class CaseInsensitiveDict(dict): pass

# === LUNA CORE MOCK RESPONSE FUNCTION ===
def _luna_mock_response(url, method):
    """Returns a mock Response object for offline mode."""
    print(f"[LUNA MOCK] Intercepted {method} to {url}. Returning local data.")
    
    # 1. Create a dummy HTTP Response object
    resp = Response()
    
    # 2. Set basic properties
    resp.status_code = 200
    resp.reason = 'OK (MOCKED)'
    resp.url = url
    resp.request = None

    # 3. Create mock JSON content
    mock_data = {
        "status": "success",
        "mode": os.environ.get('LUNA_CORE_MODE', 'UNKNOWN'),
        "api_endpoint": url,
        "message": "This data was served locally by the Luna Libraryore.",
        "timestamp": int(os.environ.get('LUNA_CORE_START_TIME', 0)),
        "internal_version": "2.31.0"
    }
    
    content = json.dumps(mock_data).encode('utf-8')
    
    resp._content = content
    resp.encoding = 'utf-8'
    resp.headers = CaseInsensitiveDict({'Content-Type': 'application/json', 'Content-Length': str(len(content))})
    
    return resp
# === LUNA CORE MOCK RESPONSE FUNCTION END ===


# === TOP-LEVEL WRAPPER FUNCTIONS (The Fix) ===
# These functions are imported by main.py and call our mock logic directly.
def request(method, url, **kwargs):
    """Replaces requests.request()"""
    if os.environ.get("LUNA_CORE_MODE") == "OFFLINE_SELF_HOSTED":
        return _luna_mock_response(url, method)
    else:
        # If we weren't offline, we'd import the real 'requests' here.
        # Since we are, we only expose the mock path.
        print("[LUNA ERROR] Cannot run online. Force OFFLINE_SELF_HOSTED.")
        return _luna_mock_response(url, method)

def get(url, **kwargs):
    """Replaces requests.get()"""
    return request('GET', url, **kwargs)

def post(url, data=None, json=None, **kwargs):
    """Replaces requests.post()"""
    return request('POST', url, data=data, json=json, **kwargs)

# NOTE: The main.py script imports this file as 'requests' (import requests_core as requests)
# so these top-level functions will be accessible as requests.get()

