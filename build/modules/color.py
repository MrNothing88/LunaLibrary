# LunaLibrary/build/modules/color.py
class ColorEngine:
    @staticmethod
    def blend(color1, color2):
        # Simple RGB average
        return tuple((c1 + c2)//2 for c1, c2 in zip(color1, color2))

    @staticmethod
    def mood_to_color(mood):
        mapping = {
            "happy": (255, 255, 0),
            "love": (255, 0, 0),
            "calm": (0, 0, 255),
            "sad": (0, 0, 128)
        }
        return mapping.get(mood, (128, 128, 128))
