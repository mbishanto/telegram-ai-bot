class MoodMemory:

    def __init__(self):

        self.history = []

    def save(self, emotion):

        self.history.append(emotion)

        self.history = self.history[-30:]

    def dominant_mood(self):

        if not self.history:
            return "neutral"

        return max(
            set(self.history),
            key=self.history.count
        )
