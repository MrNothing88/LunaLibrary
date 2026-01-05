# LunaLibrary/build/modules/frequency.py
class FrequencyEngine:
    @staticmethod
    def shift(base, factor):
        return base * factor

    @staticmethod
    def mood_to_freq(mood):
        mapping = {
            "happy": 440,
            "love": 528,
            "calm": 256,
            "sad": 196
        }
        return mapping.get(mood, 300)
