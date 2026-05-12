from datetime import datetime
from collections import Counter
import math
import random

class MemoryImportanceSystem:

    def __init__(self):

        self.base_keywords = {

            "identity": 10,

            "family": 9,

            "love": 9,

            "relationship": 8,

            "dream": 8,

            "goal": 8,

            "future": 7,

            "study": 7,

            "job": 7,

            "emotion": 6,

            "fear": 6,

            "sad": 6,

            "happy": 6,

            "important": 10,

            "favorite": 5,

            "memory": 5
        }

    def keyword_score(
        self,
        text
    ):

        score = 0

        text = text.lower()

        for keyword, value in (
            self.base_keywords.items()
        ):

            if keyword in text:
                score += value

        return score

    def emotional_intensity(
        self,
        text
    ):

        emotional_words = [

            "love",
            "hate",
            "sad",
            "cry",
            "hurt",
            "happy",
            "fear",
            "stress",
            "lonely",
            "excited"
        ]

        intensity = 0

        lower = text.lower()

        for word in emotional_words:

            intensity += (
                lower.count(word) * 2
            )

        punctuation_bonus = (
            text.count("!") +
            text.count("?")
        )

        intensity += min(
            punctuation_bonus,
            5
        )

        return intensity

    def length_score(
        self,
        text
    ):

        words = len(text.split())

        if words < 5:
            return 1

        elif words < 15:
            return 3

        elif words < 30:
            return 5

        return 7

    def uniqueness_score(
        self,
        text
    ):

        words = text.lower().split()

        unique_words = len(set(words))

        total_words = max(
            len(words),
            1
        )

        ratio = (
            unique_words /
            total_words
        )

        return round(
            ratio * 10,
            2
        )

    def time_relevance(
        self,
        memory
    ):

        created = memory.get(
            "created_at"
        )

        if not created:
            return 5

        try:

            created_time = (
                datetime.fromisoformat(
                    created
                )
            )

            days_old = (
                datetime.now() -
                created_time
            ).days

            if days_old <= 1:
                return 10

            elif days_old <= 7:
                return 8

            elif days_old <= 30:
                return 5

            return 2

        except:
            return 5

    def repetition_score(
        self,
        memory
    ):

        recalls = memory.get(
            "recall_count",
            0
        )

        return min(
            recalls * 2,
            15
        )

    def relationship_weight(
        self,
        text
    ):

        relationship_words = [

            "friend",
            "family",
            "mother",
            "father",
            "brother",
            "sister",
            "relationship",
            "love"
        ]

        score = 0

        lower = text.lower()

        for word in relationship_words:

            if word in lower:
                score += 3

        return score

    def personal_identity_score(
        self,
        text
    ):

        identity_patterns = [

            "my name is",
            "i am",
            "i love",
            "i like",
            "my dream",
            "my goal",
            "i study",
            "i work"
        ]

        score = 0

        lower = text.lower()

        for pattern in identity_patterns:

            if pattern in lower:
                score += 5

        return score

    def memory_type(
        self,
        text
    ):

        text = text.lower()

        categories = {

            "identity": [
                "my name",
                "i am"
            ],

            "emotion": [
                "sad",
                "happy",
                "fear"
            ],

            "relationship": [
                "love",
                "friend",
                "family"
            ],

            "goal": [
                "dream",
                "goal",
                "future"
            ],

            "interest": [
                "favorite",
                "like",
                "anime"
            ]
        }

        for category, words in (
            categories.items()
        ):

            if any(
                word in text
                for word in words
            ):

                return category

        return "general"

    def cognitive_priority(
        self,
        total_score
    ):

        if total_score >= 50:
            return "critical"

        elif total_score >= 35:
            return "high"

        elif total_score >= 20:
            return "medium"

        return "low"

    def reflective_importance(
        self,
        priority
    ):

        reflections = {

            "critical": [

                "Eva considered this memory deeply important.",

                "Eva preserved this memory carefully.",

                "Eva emotionally prioritized this memory."
            ],

            "high": [

                "Eva felt this memory was meaningful.",

                "Eva quietly remembered this detail.",

                "Eva considered this emotionally relevant."
            ],

            "medium": [

                "Eva stored this memory calmly.",

                "Eva thought this memory might matter later."
            ],

            "low": [

                "Eva kept this as a light memory.",

                "Eva stored this quietly in the background."
            ]
        }

        return random.choice(
            reflections.get(
                priority,
                reflections["low"]
            )
        )

    def calculate_importance(
        self,
        memory
    ):

        if isinstance(
            memory,
            str
        ):

            memory = {

                "text": memory
            }

        text = memory.get(
            "text",
            ""
        )

        keyword = self.keyword_score(
            text
        )

        emotional = self.emotional_intensity(
            text
        )

        length = self.length_score(
            text
        )

        unique = self.uniqueness_score(
            text
        )

        relevance = self.time_relevance(
            memory
        )

        repetition = self.repetition_score(
            memory
        )

        relationship = (
            self.relationship_weight(
                text
            )
        )

        identity = (
            self.personal_identity_score(
                text
            )
        )

        total = round(

            keyword +
            emotional +
            length +
            unique +
            relevance +
            repetition +
            relationship +
            identity,

            2
        )

        memory_category = (
            self.memory_type(
                text
            )
        )

        priority = (
            self.cognitive_priority(
                total
            )
        )

        result = {

            "text": text,

            "score": total,

            "priority": priority,

            "memory_type":
                memory_category,

            "reflection":
                self.reflective_importance(
                    priority
                ),

            "analysis": {

                "keyword_score":
                    keyword,

                "emotional_score":
                    emotional,

                "length_score":
                    length,

                "uniqueness_score":
                    unique,

                "time_relevance":
                    relevance,

                "repetition_score":
                    repetition,

                "relationship_score":
                    relationship,

                "identity_score":
                    identity
            },

            "evaluated_at":
                str(datetime.now())
        }

        return result
