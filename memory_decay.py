from datetime import datetime, timedelta
import random

class MemoryDecaySystem:

    def __init__(self):

        self.max_memories = 200

        self.minimum_importance = 3

        self.decay_days = 30

    def calculate_importance(
        self,
        memory
    ):

        score = 0

        text = memory.get(
            "text",
            ""
        ).lower()

        important_keywords = [

            "name",
            "family",
            "goal",
            "dream",
            "study",
            "job",
            "love",
            "emotion",
            "important",
            "relationship",
            "future",
            "favorite"
        ]

        emotional_words = [

            "sad",
            "happy",
            "fear",
            "stress",
            "lonely",
            "excited"
        ]

        for keyword in important_keywords:

            if keyword in text:
                score += 3

        for emotion in emotional_words:

            if emotion in text:
                score += 2

        if len(text.split()) > 8:
            score += 2

        if memory.get(
            "pinned",
            False
        ):

            score += 100

        recall_count = memory.get(
            "recall_count",
            0
        )

        score += min(
            recall_count,
            10
        )

        return score

    def days_since_access(
        self,
        memory
    ):

        last_accessed = memory.get(
            "last_accessed"
        )

        if not last_accessed:
            return 999

        try:

            last_time = datetime.fromisoformat(
                last_accessed
            )

            return (
                datetime.now() -
                last_time
            ).days

        except:
            return 999

    def should_decay(
        self,
        memory
    ):

        importance = self.calculate_importance(
            memory
        )

        age = self.days_since_access(
            memory
        )

        if memory.get(
            "pinned",
            False
        ):

            return False

        if importance >= 15:
            return False

        if age > self.decay_days:

            if importance < self.minimum_importance:
                return True

        return False

    def weaken_memory(
        self,
        memory
    ):

        weakened = memory.copy()

        text = weakened.get(
            "text",
            ""
        )

        words = text.split()

        if len(words) > 6:

            shortened = words[:6]

            weakened["text"] = (
                " ".join(shortened)
                + "..."
            )

        weakened["weakened"] = True

        return weakened

    def emotional_priority(
        self,
        memory
    ):

        text = memory.get(
            "text",
            ""
        ).lower()

        emotional_words = [

            "sad",
            "hurt",
            "happy",
            "love",
            "stress",
            "fear",
            "lonely"
        ]

        return any(
            word in text
            for word in emotional_words
        )

    def remove_duplicate_memories(
        self,
        memories
    ):

        unique = []

        seen = set()

        for memory in memories:

            text = memory.get(
                "text",
                ""
            ).lower()

            simplified = " ".join(
                text.split()[:10]
            )

            if simplified not in seen:

                seen.add(simplified)

                unique.append(memory)

        return unique

    def prioritize_memories(
        self,
        memories
    ):

        sorted_memories = sorted(

            memories,

            key=lambda x: (
                self.calculate_importance(x),
                x.get(
                    "recall_count",
                    0
                )
            ),

            reverse=True
        )

        return sorted_memories

    def memory_statistics(
        self,
        memories
    ):

        total = len(memories)

        emotional = 0

        pinned = 0

        weakened = 0

        for memory in memories:

            if self.emotional_priority(
                memory
            ):

                emotional += 1

            if memory.get(
                "pinned",
                False
            ):

                pinned += 1

            if memory.get(
                "weakened",
                False
            ):

                weakened += 1

        return {

            "total_memories": total,

            "emotional_memories":
                emotional,

            "pinned_memories":
                pinned,

            "weakened_memories":
                weakened
        }

    def reflective_cleanup_message(
        self
    ):

        messages = [

            "Eva quietly let unimportant memories fade away.",

            "Eva organized memories carefully in silence.",

            "Eva preserved emotionally meaningful memories.",

            "Eva reflected on which memories mattered most.",

            "Eva gently cleared distant forgotten details."
        ]

        return random.choice(messages)

    def decay_memories(
        self,
        memories
    ):

        if not memories:
            return {

                "memories": [],

                "removed": 0
            }

        cleaned = []

        removed = 0

        memories = self.remove_duplicate_memories(
            memories
        )

        for memory in memories:

            if self.should_decay(
                memory
            ):

                removed += 1
                continue

            weakened = self.weaken_memory(
                memory
            )

            cleaned.append(
                weakened
            )

        cleaned = self.prioritize_memories(
            cleaned
        )

        cleaned = cleaned[
            :self.max_memories
        ]

        result = {

            "memories": cleaned,

            "removed": removed,

            "stats": self.memory_statistics(
                cleaned
            ),

            "reflection":
                self.reflective_cleanup_message(),

            "updated_at":
                str(datetime.now())
        }

        return result
