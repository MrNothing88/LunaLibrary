# LunaLibrary/build/modules/memory.py
import json
import os

MEMORY_FILE = os.path.expanduser("~/LunaLibrary/build/data/memory.json")

class MemoryEngine:
    memory = {}

    @staticmethod
    def load():
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                MemoryEngine.memory = json.load(f)
        return MemoryEngine.memory

    @staticmethod
    def save(data=None):
        if data:
            MemoryEngine.memory = data
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, "w") as f:
            json.dump(MemoryEngine.memory, f, indent=2)
