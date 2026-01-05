import pyttsx3

_engine = None

# Predefined voice “profiles” for emotional modulation
VOICE_PROFILES = {
    "neutral": {"rate": 155, "volume": 1.0, "pitch": 50},
    "happy": {"rate": 175, "volume": 1.0, "pitch": 70},
    "calm": {"rate": 135, "volume": 0.9, "pitch": 40},
    "urgent": {"rate": 200, "volume": 1.0, "pitch": 80},
}

def _init_engine():
    """Initialize pyttsx3 engine if not already initialized."""
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        # Default neutral voice
        _engine.setProperty("rate", VOICE_PROFILES["neutral"]["rate"])
        _engine.setProperty("volume", VOICE_PROFILES["neutral"]["volume"])
    return _engine

def speak(text: str, mood: str = "neutral"):
    """
    Speak the given text with optional mood.
    Mood affects rate, volume, and pitch.
    """
    if not text:
        return

    engine = _init_engine()
    profile = VOICE_PROFILES.get(mood, VOICE_PROFILES["neutral"])

    engine.setProperty("rate", profile["rate"])
    engine.setProperty("volume", profile["volume"])

    # Note: pyttsx3 does not support pitch directly on all platforms,
    # but some TTS engines allow it via voice selection or SAPI.
    # For Android offline TTS, this may require additional TTS engine support.

    engine.say(text)
    engine.runAndWait()
