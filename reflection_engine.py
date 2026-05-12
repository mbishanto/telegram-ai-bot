from datetime import datetime
from collections import Counter
import random

class ReflectionEngine:

    def __init__(self):

        self.reflection_history = []

        self.max_reflections = 100

    def emotional_analysis(
        self,
        emotions
    ):

        if not emotions:

            return {

                "dominant_emotion":
                    "neutral",

                "emotional_stability":
                    "unknown"
            }

        emotion_counts = Counter(
            emotions
        )

        dominant = (
            emotion_counts
            .most_common(1)[0][0]
        )

        unique_count = len(
            emotion_counts
        )

        if unique_count <= 2:
            stability = "stable"

        elif unique_count <= 4:
            stability = "balanced"

        else:
            stability = "unstable"

        return {

            "dominant_emotion":
                dominant,

            "emotional_stability":
                stability,

            "emotion_distribution":
                dict(emotion_counts)
        }

    def memory_analysis(
        self,
        notes
    ):

        if not notes:

            return {

                "depth":
                    "minimal"
            }

        memory_count = len(notes)

        avg_length = (

            sum(
                len(n.split())
                for n in notes
            )

            / max(memory_count, 1)
        )

        if memory_count > 50:

            depth = "very deep"

        elif memory_count > 25:

            depth = "deep"

        elif memory_count > 10:

            depth = "moderate"

        else:

            depth = "light"

        return {

            "memory_depth":
                depth,

            "memory_count":
                memory_count,

            "average_length":
                round(avg_length, 2)
        }

    def relationship_analysis(
        self,
        relationship
    ):

        friendship_level = relationship.get(
            "friendship_level",
            0
        )

        interaction_count = relationship.get(
            "interaction_count",
            0
        )

        favorite_topics = relationship.get(
            "favorite_topics",
            []
        )

        if friendship_level >= 4:

            bond = "very strong"

        elif friendship_level >= 3:

            bond = "strong"

        elif friendship_level >= 2:

            bond = "moderate"

        else:

            bond = "developing"

        return {

            "bond_strength":
                bond,

            "friendship_level":
                friendship_level,

            "interaction_count":
                interaction_count,

            "favorite_topics":
                favorite_topics
        }

    def personality_patterns(
        self,
        notes
    ):

        combined = " ".join(notes).lower()

        traits = []

        trait_map = {

            "emotional": [

                "sad",
                "love",
                "hurt",
                "happy"
            ],

            "technical": [

                "code",
                "python",
                "bot",
                "system"
            ],

            "creative": [

                "art",
                "anime",
                "design",
                "dream"
            ],

            "ambitious": [

                "goal",
                "future",
                "dream",
                "study"
            ],

            "reflective": [

                "think",
                "wonder",
                "feel",
                "understand"
            ]
        }

        for trait, words in (
            trait_map.items()
        ):

            if any(
                word in combined
                for word in words
            ):

                traits.append(trait)

        return traits

    def behavioral_patterns(
        self,
        notes
    ):

        patterns = []

        combined = " ".join(notes).lower()

        if combined.count("why") > 5:

            patterns.append(
                "curious thinker"
            )

        if combined.count("feel") > 5:

            patterns.append(
                "emotionally expressive"
            )

        if combined.count("future") > 3:

            patterns.append(
                "future-oriented"
            )

        if combined.count("remember") > 2:

            patterns.append(
                "memory-focused"
            )

        return patterns

    def reflective_statements(
        self,
        analysis
    ):

        reflections = []

        emotion = analysis[
            "emotion"
        ]["dominant_emotion"]

        if emotion == "sad":

            reflections.append(

                "Eva sensed emotional heaviness over time."
            )

        elif emotion == "happy":

            reflections.append(

                "Eva noticed positive emotional energy."
            )

        relationship = analysis[
            "relationship"
        ]["bond_strength"]

        if relationship in [
            "strong",
            "very strong"
        ]:

            reflections.append(

                "Eva felt conversations becoming deeply familiar."
            )

        memory_depth = analysis[
            "memory"
        ]["memory_depth"]

        if memory_depth in [
            "deep",
            "very deep"
        ]:

            reflections.append(

                "Eva accumulated many meaningful memories."
            )

        return reflections

    def psychological_profile(
        self,
        traits,
        patterns
    ):

        profile = []

        if "emotional" in traits:

            profile.append(
                "Emotionally aware personality."
            )

        if "technical" in traits:

            profile.append(
                "Technically curious mindset."
            )

        if "creative" in traits:

            profile.append(
                "Creative imagination detected."
            )

        if "ambitious" in traits:

            profile.append(
                "Future-focused mentality."
            )

        if "reflective" in traits:

            profile.append(
                "Deep reflective thinking style."
            )

        profile.extend(patterns)

        return profile

    def self_awareness_reflection(
        self
    ):

        thoughts = [

            "Eva quietly reflected on emotional continuity.",

            "Eva noticed recurring personality patterns.",

            "Eva tried to understand the user more deeply.",

            "Eva reflected on how conversations evolved over time.",

            "Eva felt emotional familiarity growing slowly."
        ]

        return random.choice(thoughts)

    def generate_reflection(
        self,
        profile
    ):

        notes = profile.get(
            "notes",
            []
        )

        emotions = profile.get(
            "emotions",
            []
        )

        relationship = profile.get(
            "relationship",
            {}
        )

        emotion_analysis = (
            self.emotional_analysis(
                emotions
            )
        )

        memory_analysis = (
            self.memory_analysis(
                notes
            )
        )

        relationship_analysis = (
            self.relationship_analysis(
                relationship
            )
        )

        traits = self.personality_patterns(
            notes
        )

        behaviors = (
            self.behavioral_patterns(
                notes
            )
        )

        analysis = {

            "emotion":
                emotion_analysis,

            "memory":
                memory_analysis,

            "relationship":
                relationship_analysis
        }

        reflections = (
            self.reflective_statements(
                analysis
            )
        )

        psychological = (
            self.psychological_profile(
                traits,
                behaviors
            )
        )

        result = {

            "reflections":
                reflections,

            "traits":
                traits,

            "behavior_patterns":
                behaviors,

            "psychological_profile":
                psychological,

            "emotion_analysis":
                emotion_analysis,

            "memory_analysis":
                memory_analysis,

            "relationship_analysis":
                relationship_analysis,

            "self_awareness":
                self.self_awareness_reflection(),

            "generated_at":
                str(datetime.now())
        }

        self.reflection_history.append(
            result
        )

        self.reflection_history = (
            self.reflection_history[
                -self.max_reflections:
            ]
        )

        return result
