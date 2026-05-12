from datetime import datetime, timedelta
from collections import Counter
import random

class EmotionTracker:

    def __init__(self):

        self.current_emotion = "neutral"
        self.previous_emotion = "neutral"

        self.emotion_intensity = 0

        self.last_update = str(datetime.now())

        self.emotion_history = []

        self.emotional_patterns = {}

        self.emotion_duration = 0

        self.stability_score = 100

    def emotion_keywords(self):

        return {

            "sad": [

                "sad",
                "depressed",
                "lonely",
                "hurt",
                "cry",
                "broken",
                "tired",
                "stress",
                "upset"
            ],

            "happy": [

                "happy",
                "excited",
                "love",
                "amazing",
                "great",
                "wonderful",
                "joy",
                "fun"
            ],

            "angry": [

                "angry",
                "mad",
                "annoyed",
                "frustrated",
                "hate",
                "irritated"
            ],

            "fear": [

                "afraid",
                "scared",
                "fear",
                "nervous",
                "worried",
                "anxious"
            ],

            "calm": [

                "peaceful",
                "calm",
                "relaxed",
                "comfortable",
                "fine"
            ]
        }

    def detect_emotion(
        self,
        text
    ):

        text = text.lower()

        scores = {}

        keywords = self.emotion_keywords()

        for emotion, words in keywords.items():

            scores[emotion] = 0

            for word in words:

                scores[emotion] += text.count(word)

        dominant = max(
            scores,
            key=scores.get
        )

        if scores[dominant] == 0:
            return "neutral"

        return dominant

    def calculate_intensity(
        self,
        text,
        emotion
    ):

        intensity = 1

        text = text.lower()

        strong_words = [

            "very",
            "extremely",
            "really",
            "so much",
            "deeply"
        ]

        for word in strong_words:

            if word in text:
                intensity += 2

        exclamations = text.count("!")

        intensity += min(
            exclamations,
            3
        )

        emotion_bonus = {

            "sad": 5,
            "happy": 5,
            "angry": 6,
            "fear": 6,
            "calm": 3,
            "neutral": 2
        }

        intensity += emotion_bonus.get(
            emotion,
            2
        )

        return min(intensity, 10)

    def update_history(
        self,
        emotion,
        intensity
    ):

        self.emotion_history.append({

            "emotion": emotion,
            "intensity": intensity,
            "timestamp": str(datetime.now())
        })

        self.emotion_history = (
            self.emotion_history[-100:]
        )

    def calculate_stability(self):

        if len(self.emotion_history) < 5:
            return 100

        recent = [

            e["emotion"]
            for e in self.emotion_history[-10:]
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

    def dominant_emotion(self):

        if not self.emotion_history:
            return "neutral"

        emotions = [

            e["emotion"]
            for e in self.emotion_history
        ]

        return Counter(
            emotions
        ).most_common(1)[0][0]

    def emotional_trend(self):

        if len(self.emotion_history) < 5:
            return "stable"

        recent = [

            e["emotion"]
            for e in self.emotion_history[-5:]
        ]

        if recent.count("sad") >= 3:
            return "emotionally low"

        if recent.count("happy") >= 3:
            return "emotionally positive"

        if recent.count("angry") >= 3:
            return "emotionally frustrated"

        return "stable"

    def emotional_response_style(
        self,
        emotion
    ):

        styles = {

            "sad": "gentle",

            "happy": "cheerful",

            "angry": "calm",

            "fear": "reassuring",

            "calm": "soft",

            "neutral": "natural"
        }

        return styles.get(
            emotion,
            "natural"
        )

    def reflective_observation(self):

        reflections = [

            "Eva noticed emotional patterns becoming clearer.",

            "Eva quietly reflected on recent emotional shifts.",

            "Eva sensed deeper emotional consistency.",

            "Eva carefully observed emotional changes over time.",

            "Eva tried to understand the user's emotional state gently."
        ]

        return random.choice(reflections)

    def emotion_memory_summary(self):

        dominant = self.dominant_emotion()

        trend = self.emotional_trend()

        return {

            "dominant_emotion": dominant,

            "emotional_trend": trend,

            "stability_score": self.stability_score,

            "total_records": len(
                self.emotion_history
            )
        }

    def analyze(
        self,
        text
    ):

        emotion = self.detect_emotion(
            text
        )

        intensity = self.calculate_intensity(
            text,
            emotion
        )

        self.previous_emotion = (
            self.current_emotion
        )

        self.current_emotion = emotion

        self.emotion_intensity = intensity

        self.last_update = str(
            datetime.now()
        )

        if (
            self.previous_emotion ==
            self.current_emotion
        ):

            self.emotion_duration += 1

        else:

            self.emotion_duration = 1

        self.update_history(
            emotion,
            intensity
        )

        self.stability_score = (
            self.calculate_stability()
        )

        response = {

            "emotion": emotion,

            "previous_emotion":
                self.previous_emotion,

            "intensity": intensity,

            "duration":
                self.emotion_duration,

            "stability_score":
                self.stability_score,

            "trend":
                self.emotional_trend(),

            "response_style":
                self.emotional_response_style(
                    emotion
                ),

            "dominant_emotion":
                self.dominant_emotion(),

            "reflection":
                self.reflective_observation(),

            "updated":
                self.last_update
        }

        return response
