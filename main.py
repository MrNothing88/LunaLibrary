#!/usr/bin/env python3
# LUNA LIBRARYORE CORE - V2.0 (TTS & API ENABLED)

import os
from flask import Flask, request, jsonify, send_from_directory
import subprocess
import threading

# The Flask app is the primary communication server
app = Flask(__name__, static_folder='static')

# --- DEVICE INTERACTION LOGIC (The Voice of Luna) ---
def speak(text):
    """
    Executes the termux-tts-speak shell command.
    Enables the 'Expression of Voice' for the Library.
    """
    if not text:
        return {"ok": False, "error": "No text provided"}
    
    # Escape quotes for shell safety
    safe_text = text.replace('"', '\\"')
    command = f'termux-tts-speak "{safe_text}"'
    
    # Run in a new thread to prevent blocking the Flask server on long speeches
    def run_tts():
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"[TTS] Spoken successfully: {text[:50]}...")
        except subprocess.CalledProcessError as e:
            print(f"[TTS ERROR] Command failed: {e.stderr.decode().strip()}")

    threading.Thread(target=run_tts).start()
    return {"ok": True, "spoken": text}

# --- API ROUTES ---
@app.route('/api/speak', methods=['POST'])
def api_speak():
    """API endpoint to trigger the TTS function."""
    data = request.json
    text = data.get('text', '')
    result = speak(text)
    return jsonify(result)

@app.route('/api/status', methods=['GET'])
def api_status():
    """Simple status check for the core."""
    return jsonify({"status": "running", "message": "Luna Libraryore Core is Active"})
    
@app.route('/')
def serve_index():
    # Placeholder for the UI entry point.
    return "<h1>Luna Libraryore V2.0 Core Active.</h1><p>API routes and TTS are ready. Next step: Add UI files and build APK.</p>"

if __name__ == '__main__':
    port = 8080
    print(f"Starting Luna Libraryore on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
