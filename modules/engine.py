import time

class LunaEngine:
    def __init__(self):
        self.name = "Luna Library"
        self.version = "1.0"
    def run(self):
        print(f"🚀 {self.name} v{self.version} starting...")
        for i in range(3):
            print(f"✨ Heartbeat {i+1}")
            time.sleep(1)
        print("✅ Luna Engine is ready!")
