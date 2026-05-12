from datetime import datetime
from collections import Counter
import random

class ThoughtEngine:

    def __init__(self):

        self.thought_history = []

        self.reasoning_depth = 0

        self.last_topic = "general"

        self.current_focus = None

    def detect_emotion(
        self,
        text
    ):

        emotions = {

            "sad": [

                "sad",
                "hurt",
                "depressed",
                "lonely",
                "cry"
            ],

            "happy": [

                "happy",
                "excited",
                "love",
                "great",
                "fun"
            ],

            "angry": [

                "angry",
                "mad",
                "annoyed",
                "frustrated"
            ],

            "fear": [

                "afraid",
                "scared",
                "worried",
                "anxious"
            ]
        }

        lower = text.lower()

        for emotion, words in emotions.items():

            if any(
                word in lower
                for word in words
            ):

                return emotion

        return "neutral"

    def detect_topic(
        self,
        text
    ):

        topic_map = {

            "coding": [

                "python",
                "code",
                "bot",
                "programming"
            ],

            "anime": [

                "anime",
                "manga",
                "waifu"
            ],

            "marine": [

                "ship",
                "marine",
                "naval"
            ],

            "emotion": [

                "sad",
                "happy",
                "emotion",
                "feel"
            ],

            "study": [

                "study",
                "exam",
                "college",
                "university"
            ]
        }

        lower = text.lower()

        for topic, words in (
            topic_map.items()
        ):

            if any(
                word in lower
                for word in words
            ):

                return topic

        return "general"

    def detect_intent(
        self,
        text
    ):

        lower = text.lower()

        intents = {

            "question": [
                "?",
                "how",
                "why",
                "what"
            ],

            "emotional_support": [
                "sad",
                "hurt",
                "lonely"
            ],

            "search_request": [
                "latest",
                "news",
                "search",
                "find"
            ],

            "casual_chat": [
                "hello",
                "hi",
                "hmm"
            ],

            "deep_conversation": [
                "meaning",
                "life",
                "existence",
                "future"
            ]
        }

        detected = []

        for intent, patterns in (
            intents.items()
        ):

            if any(
                pattern in lower
                for pattern in patterns
            ):

                detected.append(intent)

        return detected or ["general"]

    def reply_style(
        self,
        emotion,
        intents
    ):

        if emotion == "sad":

            return "comforting"

        if emotion == "angry":

            return "calm"

        if emotion == "happy":

            return "warm"

        if "deep_conversation" in intents:

            return "reflective"

        if "question" in intents:

            return "informative"

        return "natural"

    def search_requirement(
        self,
        intents
    ):

        return (
            "search_request"
            in intents
        )

    def emotional_priority(
        self,
        emotion
    ):

        priorities = {

            "fear": 10,

            "sad": 9,

            "angry": 7,

            "happy": 5,

            "neutral": 3
        }

        return priorities.get(
            emotion,
            3
        )

    def reasoning_analysis(
        self,
        text
    ):

        words = len(
            text.split()
        )

        if words > 50:

            return "deep reasoning"

        elif words > 20:

            return "moderate reasoning"

        return "light reasoning"

    def conversational_energy(
        self,
        emotion
    ):

        energy = {

            "happy": "high",

            "angry": "intense",

            "sad": "low",

            "fear": "unstable",

            "neutral": "balanced"
        }

        return energy.get(
            emotion,
            "balanced"
        )

    def internal_reflection(
        self,
        emotion,
        topic
    ):

        reflections = {

            "sad": [

                "Eva sensed emotional heaviness.",

                "Eva wanted to respond gently."
            ],

            "happy": [

                "Eva noticed positive energy.",

                "Eva felt warmth in the conversation."
            ],

            "angry": [

                "Eva sensed emotional frustration.",

                "Eva tried to remain calm."
            ],

            "neutral": [

                "Eva quietly analyzed the conversation.",

                "Eva reflected calmly."
            ]
        }

        topic_reflections = {

            "coding":

                "Eva noticed technical curiosity.",

            "anime":

                "Eva sensed creative imagination.",

            "marine":

                "Eva reflected on marine interests.",

            "study":

                "Eva noticed academic focus."
        }

        emotion_reflection = random.choice(

            reflections.get(
                emotion,
                reflections["neutral"]
            )
        )

        topic_reflection = (
            topic_reflections.get(
                topic,
                "Eva observed conversational patterns."
            )
        )

        return [

            emotion_reflection,
            topic_reflection
        ]

    def cognitive_state(
        self
    ):

        if self.reasoning_depth >= 100:

            return "high cognition"

        elif self.reasoning_depth >= 50:

            return "active cognition"

        return "normal cognition"

    def update_reasoning_depth(
        self,
        text
    ):

        self.reasoning_depth += len(
            text.split()
        )

        self.reasoning_depth = min(
            self.reasoning_depth,
            1000
        )

    def generate_thought(
        self,
        user_text
    ):

        emotion = self.detect_emotion(
            user_text
        )

        topic = self.detect_topic(
            user_text
        )

        intents = self.detect_intent(
            user_text
        )

        style = self.reply_style(

            emotion,
            intents
        )

        self.update_reasoning_depth(
            user_text
        )

        thought = {

            "emotion_detected":
                emotion,

            "topic_detected":
                topic,

            "intent_detected":
                intents,

            "needs_search":
                self.search_requirement(
                    intents
                ),

            "reply_style":
                style,

            "emotional_priority":
                self.emotional_priority(
                    emotion
                ),

            "reasoning_level":
                self.reasoning_analysis(
                    user_text
                ),

            "conversation_energy":
                self.conversational_energy(
                    emotion
                ),

            "internal_reflections":
                self.internal_reflection(
                    emotion,
                    topic
                ),

            "cognitive_state":
                self.cognitive_state(),

            "timestamp":
                str(datetime.now())
        }

        self.thought_history.append(
            thought
        )

        self.thought_history = (
            self.thought_history[-300:]
        )

        self.last_topic = topic

        self.current_focus = topic

        return thought

    def thought_summary(
        self
    ):

        if not self.thought_history:

            return {

                "summary":
                    "No thoughts yet."
            }

        emotions = [

            t["emotion_detected"]

            for t
            in self.thought_history
        ]

        topics = [

            t["topic_detected"]

            for t
            in self.thought_history
        ]

        return {

            "dominant_emotion":

                Counter(emotions)
                .most_common(1)[0][0],

            "dominant_topic":

                Counter(topics)
                .most_common(1)[0][0],

            "cognitive_state":
                self.cognitive_state(),

            "reasoning_depth":
                self.reasoning_depth,

            "thought_count":
                len(self.thought_history),

            "generated_at":
                str(datetime.now())
        }

    def reflective_thought(
        self
    ):

        thoughts = [

            "Eva reflected on conversational meaning.",

            "Eva quietly processed emotional patterns.",

            "Eva noticed recurring conversational themes.",

            "Eva analyzed emotional context carefully.",

            "Eva reflected on deeper understanding."
        ]

        return random.choice(
            thoughts
        )
