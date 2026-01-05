from luna.memory.store import remember, recall

# Simple offline sentiment word lists
POSITIVE_WORDS = ["happy", "joy", "love", "excited", "great", "good", "fun"]
NEGATIVE_WORDS = ["sad", "upset", "angry", "hate", "bad", "tired", "frustrated"]
URGENT_WORDS = ["help", "urgent", "emergency", "now", "immediately"]

class LunaEngine:
    """Core Luna Engine for offline processing."""
    def __init__(self):
        self.state = "ready"
        self.running = False

    def run(self):
        """Start the Luna engine in offline mode."""
        self.running = True
        print("Luna running in offline mode")

    def stop(self):
        """Stop the engine gracefully."""
        self.running = False
        print("Luna stopped.")


def detect_mood(text: str) -> str:
    """
    Detect mood from text using simple word-based scoring.
    Returns one of: 'happy', 'sad', 'calm', 'urgent', 'neutral'
    """
    text_lower = text.lower()

    if any(word in text_lower for word in URGENT_WORDS):
        return "urgent"
    if any(word in text_lower for word in POSITIVE_WORDS):
        return "happy"
    if any(word in text_lower for word in NEGATIVE_WORDS):
        return "sad"
    if "remember" in text_lower or "note" in text_lower:
        return "calm"

    return "neutral"


def process(text: str) -> tuple[str, str]:
    """
    Process user input and return (response, mood).
    Uses sentiment-based mood detection and memory context.
    """
    text = text.strip()
    mood = detect_mood(text)

    # Keyword-based responses
    if any(word in text.lower() for word in ["hello", "hi", "hey"]):
        response = "Hello! I am Luna."
    elif any(word in text.lower() for word in ["who are you", "your name"]):
        response = "I am Luna. I exist offline with you."
    elif any(word in text.lower() for word in ["remember", "note", "save"]):
        response = "I will remember this."
    elif any(word in text.lower() for word in ["help", "urgent", "emergency"]):
        response = "I am here to assist you immediately!"
    else:
        # Retrieve previous memory if no keywords match
        last = recall("last_command")
        if last:
            response = f"I'm still thinking about what you told me: {last['value']}"
            mood = last.get("mood", mood)
        else:
            response = "I am listening."

    # Remember this input with detected mood
    remember("last_command", text, mood=mood)

    return response, mood
