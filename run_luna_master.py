#!/usr/bin/env python3
"""
🌙 LunaLibrary Master Script
- Fully self-contained
- All engines included: Color, Frequency, Memory, Personality, Packet, Realm, Sunny
- Eva understanding + GalaxyMind routing
- Outputs results to file and terminal
"""

import os
import json
import random
import uuid
import time

# --------------------------
# Directories & Output
# --------------------------
BASE_DIR = os.path.expanduser("~/LunaLibrary")
OUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_FILE = os.path.join(OUT_DIR, "luna_output.txt")

MEMORY_FILE = os.path.join(BASE_DIR, "luna_memory.json")

# --------------------------
# Core Engines
# --------------------------
class ColorEngine:
    @staticmethod
    def blend(c1, c2):
        return tuple((a+b)//2 for a,b in zip(c1,c2))
    @staticmethod
    def test():
        return f"🎨 Color Engine: {ColorEngine.blend((255,0,0),(0,0,255))}"

class FrequencyEngine:
    @staticmethod
    def shift(base, factor):
        return base * factor
    @staticmethod
    def test():
        return f"🎵 Frequency Engine: {FrequencyEngine.shift(440,1.25)}"

class MemoryEngine:
    memory = {}
    @staticmethod
    def load():
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE,"r") as f:
                MemoryEngine.memory = json.load(f)
        else:
            MemoryEngine.memory = {}
    @staticmethod
    def save():
        with open(MEMORY_FILE,"w") as f:
            json.dump(MemoryEngine.memory,f,indent=2)
    @staticmethod
    def store(key,value):
        MemoryEngine.memory[key] = {"value":value,"time":time.time()}
        MemoryEngine.save()
    @staticmethod
    def test():
        MemoryEngine.load()
        MemoryEngine.store("status","alive")
        return f"🧠 Memory Engine: {MemoryEngine.memory}"

class PersonalityEngine:
    personality = {"warmth":0.5,"precision":0.5,"playfulness":0.5}
    @staticmethod
    def evolve():
        return {k:min(1,max(0,v+random.uniform(-0.1,0.1))) for k,v in PersonalityEngine.personality.items()}
    @staticmethod
    def test():
        return f"💗 Personality Engine: {PersonalityEngine.evolve()}"

class PacketEngine:
    @staticmethod
    def build(data):
        return {"id":str(uuid.uuid4()),"payload":data,"size":len(str(data)),"time":time.time()}
    @staticmethod
    def test():
        return f"📦 Packet Engine: {PacketEngine.build('hello luna')}"

class RealmEngine:
    @staticmethod
    def tag(value):
        low = value.lower()
        if "love" in low: return "heart"
        if "logic" in low: return "mind"
        return "neutral"
    @staticmethod
    def test():
        return f"🌌 Realm Engine: {RealmEngine.tag('love and balance')}"

class SunnyEngine:
    @staticmethod
    def shine(level=3):
        return "☀️"*level
    @staticmethod
    def test():
        return f"☀️ Sunny Engine: {SunnyEngine.shine()}"

# --------------------------
# Eva Understanding
# --------------------------
class EvaUnderstanding:
    @staticmethod
    def unify(text=None,image_desc=None):
        analysis = {}
        if text:
            analysis["text_sentiment"] = "POSITIVE" if any(w in text.lower() for w in ["love","happy","good"]) else "NEGATIVE"
        if image_desc:
            analysis["image_analysis"] = {"description":image_desc,"score":0.5}
        analysis["knowledge_snapshot"] = MemoryEngine.memory
        analysis["advice"] = "Proceed as normal." if analysis.get("text_sentiment")=="POSITIVE" else "Be gentle. Suggest a calming activity."
        return analysis

# --------------------------
# GalaxyMind Router
# --------------------------
class GalaxyMind:
    def __init__(self):
        self.atom = MemoryEngine
        self.luna = PersonalityEngine
        self.eva = EvaUnderstanding
        self.color = ColorEngine
        self.freq = FrequencyEngine
        self.realm = RealmEngine
        self.sunny = SunnyEngine

    def route(self,text=None,image_desc=None):
        persona = self.luna.evolve()
        color_tag = self.color.blend((255,200,200),(200,255,200))
        freq_tag = self.freq.shift(440,random.uniform(0.8,1.2))
        eva_out = self.eva.unify(text=text,image_desc=image_desc)
        eva_out.update({
            "persona":persona,
            "color_tag":color_tag,
            "frequency_tag":freq_tag,
            "realm_tag":self.realm.tag(text if text else ""),
            "sunny":self.sunny.shine(2)
        })
        return eva_out

# --------------------------
# Main Script
# --------------------------
def main():
    MemoryEngine.load()
    gm = GalaxyMind()
    output = []
    output.append("🌙 LunaLibrary Master Script Starting...\n")
    output.append(ColorEngine.test())
    output.append(FrequencyEngine.test())
    output.append(MemoryEngine.test())
    output.append(PersonalityEngine.test())
    output.append(PacketEngine.test())
    output.append(RealmEngine.test())
    output.append(SunnyEngine.test())
    # Example GalaxyMind route
    res = gm.route(text="I love learning!", image_desc="sunset photo")
    output.append("\n🌌 GalaxyMind Unified Output:")
    output.append(json.dumps(res,indent=2))
    # Write output to file
    with open(OUT_FILE,"w") as f:
        f.write("\n".join(output))
    print(f"📄 Output written to {OUT_FILE}")
    print("\n".join(output))

if __name__=="__main__":
    main()
