from datetime import datetime
import random

class VoiceSystem:

    def __init__(self):

        self.voice_style = "natural"

        self.current_emotion = "neutral"

        self.voice_energy = 5

        self.speaking_speed = 1.0

        self.voice_history = []

    def update_voice_context(

        self,
        emotion="neutral",
        style="natural",
        energy=5

    ):

        self.current_emotion = emotion

        self.voice_style = style

        self.voice_energy = energy

        self.adjust_speaking_speed()

    def adjust_speaking_speed(
        self
    ):

        emotion_speed = {

            "sad": 0.8,

            "happy": 1.2,

            "angry": 1.3,

            "fear": 0.9,

            "neutral": 1.0
        }

        self.speaking_speed = (
            emotion_speed.get(
                self.current_emotion,
                1.0
            )
        )

    def emotional_tone(
        self
    ):

        tones = {

            "sad": [

                "soft",
                "gentle",
                "comforting"
            ],

            "happy": [

                "warm",
                "cheerful",
                "bright"
            ],

            "angry": [

                "controlled",
                "firm",
                "intense"
            ],

            "fear": [

                "careful",
                "hesitant",
                "reassuring"
            ],

            "neutral": [

                "balanced",
                "natural",
                "calm"
            ]
        }

        return random.choice(

            tones.get(
                self.current_emotion,
                tones["neutral"]
            )
        )

    def breathing_pattern(
        self
    ):

        patterns = {

            "sad":
                "slow breathing",

            "happy":
                "light energetic breathing",

            "angry":
                "heavy breathing",

            "fear":
                "slightly unstable breathing",

            "neutral":
                "steady breathing"
        }

        return patterns.get(

            self.current_emotion,

            patterns["neutral"]
        )

    def pause_pattern(
        self
    ):

        pauses = {

            "sad":
                random.uniform(1.2, 2.5),

            "happy":
                random.uniform(0.3, 1.0),

            "angry":
                random.uniform(0.2, 0.8),

            "fear":
                random.uniform(0.8, 1.8),

            "neutral":
                random.uniform(0.5, 1.3)
        }

        return round(

            pauses.get(
                self.current_emotion,
                1.0
            ),

            2
        )

    def speech_expression(
        self
    ):

        expressions = {

            "sad": [

                "quiet emotional tone",

                "slightly fragile voice"
            ],

            "happy": [

                "bright expressive tone",

                "gentle cheerful voice"
            ],

            "angry": [

                "controlled emotional intensity",

                "firm speaking tone"
            ],

            "fear": [

                "careful hesitant speech",

                "slightly uncertain tone"
            ],

            "neutral": [

                "natural conversational tone",

                "balanced voice expression"
            ]
        }

        return random.choice(

            expressions.get(
                self.current_emotion,
                expressions["neutral"]
            )
        )

    def pronunciation_style(
        self
    ):

        styles = {

            "natural":

                "smooth pronunciation",

            "deep":

                "slow thoughtful articulation",

            "playful":

                "light expressive articulation",

            "formal":

                "clear structured pronunciation",

            "comforting":

                "soft careful articulation"
        }

        return styles.get(

            self.voice_style,

            styles["natural"]
        )

    def emotional_voice_reflection(
        self
    ):

        reflections = [

            "Eva adjusted her voice gently.",

            "Eva reflected emotion through vocal tone.",

            "Eva softened her speaking style naturally.",

            "Eva carefully controlled emotional expression.",

            "Eva adapted vocal warmth to the conversation."
        ]

        return random.choice(
            reflections
        )

    def voice_analysis(
        self,
        text=""
    ):

        words = len(
            text.split()
        )

        if words > 50:

            complexity = "deep response"

        elif words > 20:

            complexity = "moderate response"

        else:

            complexity = "short response"

        return {

            "response_complexity":
                complexity,

            "word_count":
                words,

            "recommended_pause":
                self.pause_pattern()
        }

    def emotional_voice_profile(
        self
    ):

        return {

            "emotion":
                self.current_emotion,

            "voice_tone":
                self.emotional_tone(),

            "voice_style":
                self.voice_style,

            "speech_expression":
                self.speech_expression(),

            "pronunciation":
                self.pronunciation_style(),

            "breathing":
                self.breathing_pattern(),

            "speaking_speed":
                self.speaking_speed,

            "energy":
                self.voice_energy
        }

    def process_voice(
        self,
        text=""
    ):

        profile = (
            self.emotional_voice_profile()
        )

        analysis = self.voice_analysis(
            text
        )

        result = {

            "voice_ready": True,

            "voice_profile":
                profile,

            "speech_analysis":
                analysis,

            "reflection":
                self.emotional_voice_reflection(),

            "timestamp":
                str(datetime.now())
        }

        self.voice_history.append(
            result
        )

        self.voice_history = (
            self.voice_history[-200:]
        )

        return result

    def voice_memory_summary(
        self
    ):

        if not self.voice_history:

            return {

                "summary":
                    "No voice activity yet."
            }

        emotions = [

            v["voice_profile"]["emotion"]

            for v
            in self.voice_history
        ]

        dominant = max(

            set(emotions),

            key=emotions.count
        )

        return {

            "dominant_voice_emotion":
                dominant,

            "voice_interactions":
                len(self.voice_history),

            "last_voice_state":
                self.voice_history[-1],

            "generated_at":
                str(datetime.now())
        }

    def adaptive_voice_evolution(
        self
    ):

        total = len(
            self.voice_history
        )

        if total >= 200:

            stage = "highly adaptive voice"

        elif total >= 100:

            stage = "emotionally adaptive voice"

        elif total >= 50:

            stage = "developing vocal personality"

        else:

            stage = "basic voice adaptation"

        return {

            "evolution_stage":
                stage,

            "reflection":

                "Eva's vocal personality evolved through interaction.",

            "interaction_count":
                total
        }
