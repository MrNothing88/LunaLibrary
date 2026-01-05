import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from luna.core.engine import process, LunaEngine
from luna.voice.speaker import speak

# Initialize Luna engine
luna = LunaEngine()

# Greet user with happy mood
speak("Luna is online. I am here with you.", mood="happy")

# Run engine in a background thread to keep UI responsive
threading.Thread(target=luna.run, daemon=True).start()


class LunaUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # Conversation log
        self.log = TextInput(readonly=True, size_hint_y=0.7, font_size=16)

        # User input field
        self.input = TextInput(size_hint_y=0.15, multiline=False, font_size=16)
        
        # Send button
        btn = Button(text="Send", size_hint_y=0.15, font_size=16)
        btn.bind(on_press=self.send)

        # Add widgets to layout
        self.add_widget(self.log)
        self.add_widget(self.input)
        self.add_widget(btn)

    def send(self, _):
        text = self.input.text.strip()
        if not text:
            return

        # Process user input and get mood-aware response
        response, mood = process(text)

        # Update conversation log
        self.log.text += f"\nYou: {text}\nLuna: {response}\n"

        # Speak the response with mood
        speak(response, mood=mood)

        # Clear input field
        self.input.text = ""

        # Auto-scroll to bottom
        self.log.cursor = (0, len(self.log.text.splitlines()))


class LunaApp(App):
    def build(self):
        return LunaUI()


if __name__ == "__main__":
    LunaApp().run()
