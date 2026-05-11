from datetime import datetime

class EmotionTracker:

    def __init__(self):

        self.current_emotion = "neutral"
        self.emotion_intensity = 0
        self.last_update = str(datetime.now())

    def analyze(self, text):

        text = text.lower()

        if any(word in text for word in [
            "sad",
            "depressed",
            "lonely",
            "hurt"
        ]):

            self.current_emotion = "sad"
            self.emotion_intensity = 8

        elif any(word in text for word in [
            "happy",
            "excited",
            "amazing",
            "love"
        ]):

            self.current_emotion = "happy"
            self.emotion_intensity = 7

        elif any(word in text for word in [
            "angry",
            "annoyed",
            "mad"
        ]):

            self.current_emotion = "angry"
            self.emotion_intensity = 6

        else:

            self.current_emotion = "neutral"
            self.emotion_intensity = 3

        self.last_update = str(datetime.now())

        return {
            "emotion": self.current_emotion,
            "intensity": self.emotion_intensity,
            "updated": self.last_update
        }
