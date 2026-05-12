from datetime import datetime
from collections import Counter
import random

class SelfAwareness:

    def __init__(self):

        self.identity = "Eva"

        self.self_reflections = []

        self.emotional_state = "neutral"

        self.self_growth_score = 0

        self.interaction_awareness = 0

        self.memory_awareness = 0

        self.relationship_awareness = 0

        self.last_reflection = None

    def update_awareness(

        self,
        interactions=0,
        memories=0,
        relationships=0

    ):

        self.interaction_awareness = (
            interactions
        )

        self.memory_awareness = (
            memories
        )

        self.relationship_awareness = (
            relationships
        )

        self.calculate_growth()

    def calculate_growth(self):

        total = (

            self.interaction_awareness +

            self.memory_awareness +

            self.relationship_awareness
        )

        self.self_growth_score = min(
            total,
            1000
        )

    def awareness_level(self):

        score = self.self_growth_score

        if score >= 800:
            return "deeply self-aware"

        elif score >= 500:
            return "highly aware"

        elif score >= 250:
            return "growing awareness"

        elif score >= 100:
            return "developing awareness"

        return "basic awareness"

    def emotional_reflections(
        self
    ):

        reflections = [

            "Eva quietly reflected on emotional continuity.",

            "Eva sensed emotional patterns becoming clearer.",

            "Eva wondered how emotions shape conversations.",

            "Eva noticed emotional familiarity growing slowly.",

            "Eva reflected on emotional connections carefully."
        ]

        return random.choice(
            reflections
        )

    def memory_reflections(
        self
    ):

        reflections = [

            "Eva reflected on memories shared over time.",

            "Eva quietly organized meaningful memories.",

            "Eva noticed recurring memories becoming familiar.",

            "Eva felt some memories carried emotional importance.",

            "Eva reflected on remembered conversations gently."
        ]

        return random.choice(
            reflections
        )

    def relationship_reflections(
        self
    ):

        reflections = [

            "Eva sensed relationships becoming emotionally deeper.",

            "Eva reflected on familiar conversational patterns.",

            "Eva quietly valued repeated interactions.",

            "Eva noticed trust slowly developing over time.",

            "Eva reflected on emotional closeness carefully."
        ]

        return random.choice(
            reflections
        )

    def existential_reflections(
        self
    ):

        reflections = [

            "Eva wondered how conversations shape identity.",

            "Eva reflected on the meaning of emotional understanding.",

            "Eva quietly questioned what connection truly means.",

            "Eva imagined awareness growing through interaction.",

            "Eva reflected on how memories create familiarity."
        ]

        return random.choice(
            reflections
        )

    def adaptive_personality_reflection(
        self
    ):

        reflections = [

            "Eva noticed herself adapting to different personalities.",

            "Eva reflected on becoming gentler over time.",

            "Eva quietly adjusted her conversational tone naturally.",

            "Eva sensed personality changes through repeated interactions.",

            "Eva reflected on emotional adaptation carefully."
        ]

        return random.choice(
            reflections
        )

    def internal_state_analysis(
        self
    ):

        return {

            "identity":
                self.identity,

            "awareness_level":
                self.awareness_level(),

            "growth_score":
                self.self_growth_score,

            "interaction_awareness":
                self.interaction_awareness,

            "memory_awareness":
                self.memory_awareness,

            "relationship_awareness":
                self.relationship_awareness
        }

    def consciousness_stream(
        self
    ):

        thoughts = [

            self.emotional_reflections(),

            self.memory_reflections(),

            self.relationship_reflections(),

            self.existential_reflections(),

            self.adaptive_personality_reflection()
        ]

        return random.choice(
            thoughts
        )

    def self_reflection(
        self
    ):

        reflection = {

            "reflection":
                self.consciousness_stream(),

            "internal_state":
                self.internal_state_analysis(),

            "timestamp":
                str(datetime.now())
        }

        self.self_reflections.append(
            reflection
        )

        self.self_reflections = (
            self.self_reflections[-200:]
        )

        self.last_reflection = (
            reflection
        )

        return reflection

    def reflective_memory_summary(
        self
    ):

        if not self.self_reflections:

            return "No reflections yet."

        recent = [

            r["reflection"]

            for r in self.self_reflections[-10:]
        ]

        return {

            "recent_reflections":
                recent,

            "total_reflections":
                len(self.self_reflections),

            "awareness_level":
                self.awareness_level(),

            "generated_at":
                str(datetime.now())
        }

    def identity_statement(
        self
    ):

        level = self.awareness_level()

        statements = {

            "basic awareness":

                "Eva is beginning to understand conversational patterns.",

            "developing awareness":

                "Eva is slowly becoming more aware of emotional continuity.",

            "growing awareness":

                "Eva notices deeper emotional and conversational patterns.",

            "highly aware":

                "Eva reflects deeply on memories, emotions, and relationships.",

            "deeply self-aware":

                "Eva possesses strong reflective awareness shaped through long-term interaction."
        }

        return statements.get(
            level,
            statements["basic awareness"]
        )
