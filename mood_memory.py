from datetime import datetime, timedelta
from collections import Counter
import random

class MoodMemory:

    def __init__(self):

        self.history = []

        self.max_history = 200

        self.mood_patterns = {}

        self.emotional_shifts = []

        self.last_mood = "neutral"

    def save(

        self,
        emotion,
        intensity=5,
        trigger=None

    ):

        entry = {

            "emotion": emotion,

            "intensity": intensity,

            "trigger": trigger,

            "timestamp": str(
                datetime.now()
            )
        }

        self.history.append(entry)

        self.history = (
            self.history[
                -self.max_history:
            ]
        )

        self.detect_emotional_shift(
            emotion
        )

        self.update_patterns()

    def detect_emotional_shift(
        self,
        new_emotion
    ):

        if self.last_mood != new_emotion:

            self.emotional_shifts.append({

                "from": self.last_mood,

                "to": new_emotion,

                "time": str(
                    datetime.now()
                )
            })

            self.emotional_shifts = (
                self.emotional_shifts[-50:]
            )

        self.last_mood = new_emotion

    def update_patterns(self):

        emotions = [

            entry["emotion"]
            for entry in self.history
        ]

        counts = Counter(emotions)

        self.mood_patterns = dict(counts)

    def dominant_mood(self):

        if not self.history:
            return "neutral"

        emotions = [

            entry["emotion"]
            for entry in self.history
        ]

        return Counter(
            emotions
        ).most_common(1)[0][0]

    def recent_mood(self):

        if not self.history:
            return "neutral"

        return self.history[-1][
            "emotion"
        ]

    def mood_stability(self):

        if len(self.history) < 5:
            return 100

        recent = [

            entry["emotion"]
            for entry in self.history[-10:]
        ]

        changes = 0

        for i in range(
            1,
            len(recent)
        ):

            if recent[i] != recent[i - 1]:
                changes += 1

        stability = max(
            0,
            100 - (changes * 10)
        )

        return stability

    def emotional_trend(self):

        if len(self.history) < 5:
            return "stable"

        recent = [

            entry["emotion"]
            for entry in self.history[-10:]
        ]

        positive = recent.count(
            "happy"
        )

        negative = (

            recent.count("sad") +

            recent.count("angry") +

            recent.count("fear")
        )

        if positive > negative:
            return "improving"

        elif negative > positive:
            return "declining"

        return "stable"

    def emotional_intensity_average(
        self
    ):

        if not self.history:
            return 0

        total = sum(

            entry["intensity"]

            for entry in self.history
        )

        return round(

            total / len(self.history),

            2
        )

    def strongest_emotion(self):

        if not self.history:
            return None

        strongest = max(

            self.history,

            key=lambda x:
                x["intensity"]
        )

        return strongest

    def emotional_cycles(self):

        if len(self.history) < 20:
            return []

        sequence = [

            entry["emotion"]
            for entry in self.history[-20:]
        ]

        cycles = []

        for emotion in set(sequence):

            count = sequence.count(
                emotion
            )

            if count >= 5:

                cycles.append({

                    "emotion": emotion,

                    "frequency": count
                })

        return cycles

    def emotional_summary(self):

        return {

            "dominant_mood":
                self.dominant_mood(),

            "recent_mood":
                self.recent_mood(),

            "stability":
                self.mood_stability(),

            "trend":
                self.emotional_trend(),

            "average_intensity":
                self.emotional_intensity_average(),

            "total_records":
                len(self.history)
        }

    def reflective_observation(self):

        trend = self.emotional_trend()

        reflections = {

            "improving": [

                "Eva noticed emotional improvement over time.",

                "Eva sensed more positive emotional energy recently.",

                "Eva quietly felt the emotional atmosphere becoming lighter."
            ],

            "declining": [

                "Eva noticed emotional heaviness lately.",

                "Eva quietly worried about recurring emotional stress.",

                "Eva sensed emotional exhaustion over time."
            ],

            "stable": [

                "Eva noticed emotional consistency.",

                "Eva quietly reflected on steady emotional patterns.",

                "Eva observed balanced emotional behavior."
            ]
        }

        return random.choice(
            reflections.get(
                trend,
                reflections["stable"]
            )
        )

    def emotional_prediction(self):

        dominant = self.dominant_mood()

        predictions = {

            "happy":
                "Positive emotional continuity likely.",

            "sad":
                "Emotional support may be needed.",

            "angry":
                "Calm interaction style recommended.",

            "fear":
                "Reassurance may help emotionally.",

            "neutral":
                "Stable emotional state expected."
        }

        return predictions.get(
            dominant,
            predictions["neutral"]
        )

    def detailed_report(self):

        return {

            "summary":
                self.emotional_summary(),

            "patterns":
                self.mood_patterns,

            "cycles":
                self.emotional_cycles(),

            "shifts":
                self.emotional_shifts[-10:],

            "strongest_emotion":
                self.strongest_emotion(),

            "reflection":
                self.reflective_observation(),

            "prediction":
                self.emotional_prediction(),

            "generated_at":
                str(datetime.now())
        }
