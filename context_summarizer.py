from datetime import datetime
from collections import Counter
import re

class ContextSummarizer:

    def __init__(self):

        self.max_messages = 50

    def clean_text(self, text):

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def extract_user_messages(
        self,
        messages
    ):

        user_msgs = []

        for msg in messages:

            if msg.get("role") == "user":

                content = msg.get(
                    "content",
                    ""
                )

                if content:

                    user_msgs.append(
                        self.clean_text(content)
                    )

        return user_msgs

    def detect_topics(
        self,
        messages
    ):

        topic_keywords = {

            "anime": [
                "anime",
                "manga",
                "waifu"
            ],

            "coding": [
                "python",
                "code",
                "bot",
                "programming"
            ],

            "emotion": [
                "sad",
                "happy",
                "stress",
                "lonely"
            ],

            "study": [
                "study",
                "exam",
                "university",
                "college"
            ],

            "marine": [
                "ship",
                "marine",
                "naval",
                "engine"
            ]
        }

        detected = []

        combined = " ".join(messages).lower()

        for topic, words in topic_keywords.items():

            for word in words:

                if word in combined:

                    detected.append(topic)
                    break

        return list(set(detected))

    def emotional_analysis(
        self,
        messages
    ):

        emotional_words = {

            "sad": [
                "sad",
                "depressed",
                "hurt",
                "lonely"
            ],

            "happy": [
                "happy",
                "excited",
                "love",
                "great"
            ],

            "angry": [
                "angry",
                "annoyed",
                "mad",
                "frustrated"
            ]
        }

        emotion_scores = {
            "sad": 0,
            "happy": 0,
            "angry": 0
        }

        combined = " ".join(messages).lower()

        for emotion, words in emotional_words.items():

            for word in words:

                emotion_scores[emotion] += (
                    combined.count(word)
                )

        dominant = max(
            emotion_scores,
            key=emotion_scores.get
        )

        if emotion_scores[dominant] == 0:
            return "neutral"

        return dominant

    def important_memories(
        self,
        messages
    ):

        important_keywords = [

            "my name",
            "i love",
            "i like",
            "my goal",
            "my dream",
            "important",
            "favorite",
            "i study",
            "i work"
        ]

        memories = []

        for msg in messages:

            lower = msg.lower()

            if any(
                key in lower
                for key in important_keywords
            ):

                memories.append(msg)

        return memories[:10]

    def conversation_style(
        self,
        messages
    ):

        combined = " ".join(messages)

        avg_length = (
            len(combined.split()) /
            max(len(messages), 1)
        )

        if avg_length < 5:
            return "short"

        elif avg_length < 15:
            return "casual"

        elif avg_length < 30:
            return "detailed"

        return "very detailed"

    def interaction_stats(
        self,
        messages
    ):

        return {

            "total_messages": len(messages),

            "total_words": len(
                " ".join(messages).split()
            ),

            "average_length": round(
                len(
                    " ".join(messages).split()
                ) / max(len(messages), 1),
                2
            )
        }

    def generate_summary(
        self,
        messages
    ):

        if not messages:

            return {
                "summary": "No conversation found."
            }

        user_messages = self.extract_user_messages(
            messages[-self.max_messages:]
        )

        if not user_messages:

            return {
                "summary": "No user messages found."
            }

        topics = self.detect_topics(
            user_messages
        )

        emotion = self.emotional_analysis(
            user_messages
        )

        memories = self.important_memories(
            user_messages
        )

        style = self.conversation_style(
            user_messages
        )

        stats = self.interaction_stats(
            user_messages
        )

        short_summary = (
            " | ".join(
                user_messages[-5:]
            )
        )

        result = {

            "summary": short_summary,

            "topics": topics,

            "dominant_emotion": emotion,

            "important_memories": memories,

            "conversation_style": style,

            "stats": stats,

            "generated_at": str(
                datetime.now()
            )
        }

        return result

    def reflective_summary(
        self,
        messages
    ):

        summary = self.generate_summary(
            messages
        )

        reflections = []

        emotion = summary.get(
            "dominant_emotion",
            "neutral"
        )

        if emotion == "sad":

            reflections.append(
                "User seems emotionally sensitive lately."
            )

        elif emotion == "happy":

            reflections.append(
                "User has shown positive emotional patterns."
            )

        topics = summary.get(
            "topics",
            []
        )

        if "coding" in topics:

            reflections.append(
                "User appears technically curious."
            )

        if "marine" in topics:

            reflections.append(
                "User enjoys marine-related discussions."
            )

        if summary.get(
            "conversation_style"
        ) == "very detailed":

            reflections.append(
                "User likes deep conversations."
            )

        summary["reflections"] = reflections

        return summary
