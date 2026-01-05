import os
import json
import importlib.util

DATA_FILE = os.path.expanduser("~/LunaLibrary/data/storage.json")
UPGRADE_FOLDER = os.path.expanduser("~/LunaLibrary/upgrades")
MODULE_FOLDER = os.path.expanduser("~/LunaLibrary/build/modules")

# --- Initialize storage ---
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"knowledge": {}, "settings": {}}, f)

# --- Load core modules ---
core_modules = ["engine", "utils"]
loaded_modules = {}
for mod in core_modules:
    spec = importlib.util.spec_from_file_location(mod, os.path.join(MODULE_FOLDER, f"{mod}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    loaded_modules[mod] = module

# --- Load upgrades automatically ---
if os.path.exists(UPGRADE_FOLDER):
    for file in os.listdir(UPGRADE_FOLDER):
        if file.endswith(".py"):
            mod_name = file[:-3]
            spec = importlib.util.spec_from_file_location(mod_name, os.path.join(UPGRADE_FOLDER, file))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            loaded_modules[mod_name] = module

# --- Example usage ---
print("🎨 Loaded modules:", list(loaded_modules.keys()))
