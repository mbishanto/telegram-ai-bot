from datetime import datetime
from collections import Counter
import random

class RelationshipEngine:

    def __init__(self):

        self.friendship_level = 0

        self.interactions = 0

        self.trust_level = 0

        self.emotional_bond = 0

        self.comfort_level = 0

        self.favorite_topics = []

        self.shared_memories = []

        self.relationship_stage = "new"

        self.communication_style = "neutral"

        self.last_interaction = None

        self.interaction_history = []

        self.affection_score = 0

        self.loyalty_score = 0

    def update_interaction(

        self,
        message="",
        emotion="neutral",
        topic=None

    ):

        self.interactions += 1

        self.last_interaction = (
            str(datetime.now())
        )

        self.interaction_history.append({

            "message": message,

            "emotion": emotion,

            "topic": topic,

            "time": str(datetime.now())
        })

        self.interaction_history = (
            self.interaction_history[-300:]
        )

        self.calculate_friendship_level()

        self.update_emotional_bond(
            emotion
        )

        self.update_trust()

        self.update_comfort()

        if topic:
            self.track_topics(topic)

        self.detect_relationship_stage()

        self.communication_style = (
            self.detect_style(message)
        )

        return self.relationship_snapshot()

    def calculate_friendship_level(
        self
    ):

        score = (

            self.interactions +

            self.trust_level +

            self.emotional_bond +

            self.comfort_level
        )

        if score >= 250:
            self.friendship_level = 5

        elif score >= 180:
            self.friendship_level = 4

        elif score >= 120:
            self.friendship_level = 3

        elif score >= 60:
            self.friendship_level = 2

        elif score >= 20:
            self.friendship_level = 1

        else:
            self.friendship_level = 0

    def update_emotional_bond(
        self,
        emotion
    ):

        emotional_weights = {

            "sad": 4,

            "happy": 3,

            "fear": 5,

            "angry": 2,

            "neutral": 1
        }

        self.emotional_bond += (
            emotional_weights.get(
                emotion,
                1
            )
        )

        self.emotional_bond = min(
            self.emotional_bond,
            100
        )

    def update_trust(self):

        increment = max(

            1,

            int(
                self.interactions / 10
            )
        )

        self.trust_level += increment

        self.trust_level = min(
            self.trust_level,
            100
        )

    def update_comfort(self):

        self.comfort_level += 1

        self.comfort_level = min(
            self.comfort_level,
            100
        )

    def track_topics(
        self,
        topic
    ):

        topic = topic.lower()

        self.favorite_topics.append(
            topic
        )

        self.favorite_topics = (
            self.favorite_topics[-100:]
        )

    def top_topics(self):

        if not self.favorite_topics:
            return []

        counts = Counter(
            self.favorite_topics
        )

        return counts.most_common(5)

    def detect_relationship_stage(
        self
    ):

        level = self.friendship_level

        if level >= 5:

            self.relationship_stage = (
                "deep emotional connection"
            )

        elif level >= 4:

            self.relationship_stage = (
                "very close"
            )

        elif level >= 3:

            self.relationship_stage = (
                "comfortable friendship"
            )

        elif level >= 2:

            self.relationship_stage = (
                "growing familiarity"
            )

        elif level >= 1:

            self.relationship_stage = (
                "early connection"
            )

        else:

            self.relationship_stage = (
                "new interaction"
            )

    def detect_style(
        self,
        message
    ):

        text = message.lower()

        if len(text.split()) > 30:

            return "deep"

        if "haha" in text or "lol" in text:

            return "playful"

        if any(
            word in text
            for word in [
                "sad",
                "hurt",
                "cry"
            ]
        ):

            return "emotional"

        if any(
            word in text
            for word in [
                "code",
                "python",
                "system"
            ]
        ):

            return "technical"

        return "casual"

    def affection_analysis(
        self
    ):

        if self.friendship_level >= 5:

            return "deeply attached"

        elif self.friendship_level >= 4:

            return "strongly connected"

        elif self.friendship_level >= 3:

            return "emotionally comfortable"

        elif self.friendship_level >= 2:

            return "developing attachment"

        return "neutral"

    def interaction_frequency(
        self
    ):

        if len(
            self.interaction_history
        ) < 2:

            return "low"

        return "consistent"

    def relationship_reflection(
        self
    ):

        reflections = [

            "Eva noticed emotional familiarity growing slowly.",

            "Eva quietly reflected on repeated interactions.",

            "Eva felt conversations becoming more natural.",

            "Eva sensed increasing emotional trust.",

            "Eva noticed deeper conversational comfort."
        ]

        return random.choice(
            reflections
        )

    def shared_memory(

        self,
        memory

    ):

        self.shared_memories.append({

            "memory": memory,

            "time": str(datetime.now())
        })

        self.shared_memories = (
            self.shared_memories[-100:]
        )

    def emotional_synchronization(
        self
    ):

        if self.emotional_bond >= 80:

            return "high emotional synchronization"

        elif self.emotional_bond >= 50:

            return "moderate emotional synchronization"

        return "low emotional synchronization"

    def relationship_snapshot(
        self
    ):

        return {

            "friendship_level":
                self.friendship_level,

            "relationship_stage":
                self.relationship_stage,

            "trust_level":
                self.trust_level,

            "comfort_level":
                self.comfort_level,

            "emotional_bond":
                self.emotional_bond,

            "interaction_count":
                self.interactions,

            "favorite_topics":
                self.top_topics(),

            "communication_style":
                self.communication_style,

            "affection":
                self.affection_analysis(),

            "interaction_frequency":
                self.interaction_frequency(),

            "emotional_sync":
                self.emotional_synchronization(),

            "reflection":
                self.relationship_reflection(),

            "last_interaction":
                self.last_interaction
        }

    def detailed_relationship_report(
        self
    ):

        return {

            "snapshot":
                self.relationship_snapshot(),

            "shared_memories":
                self.shared_memories[-10:],

            "recent_interactions":
                self.interaction_history[-10:],

            "generated_at":
                str(datetime.now())
        }
