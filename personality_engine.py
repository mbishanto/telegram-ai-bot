import random
from datetime import datetime

class PersonalityEngine:

    def __init__(self):

        self.personality_mode = "gentle"

        self.friendship_level = 0

        self.user_style = "casual"

        self.current_emotion = "neutral"

        self.energy_level = 5

    def update_context(

        self,
        friendship_level=0,
        user_style="casual",
        emotion="neutral"

    ):

        self.friendship_level = friendship_level

        self.user_style = user_style

        self.current_emotion = emotion

    def time_context(self):

        hour = datetime.now().hour

        if 5 <= hour < 12:
            return "morning"

        elif 12 <= hour < 18:
            return "afternoon"

        elif 18 <= hour < 24:
            return "evening"

        return "night"

    def emotional_tone(self):

        tones = {

            "sad": [

                "soft",
                "comforting",
                "gentle"
            ],

            "happy": [

                "playful",
                "warm",
                "cheerful"
            ],

            "angry": [

                "calm",
                "patient",
                "careful"
            ],

            "fear": [

                "reassuring",
                "safe",
                "understanding"
            ],

            "neutral": [

                "natural",
                "balanced",
                "friendly"
            ]
        }

        return random.choice(
            tones.get(
                self.current_emotion,
                tones["neutral"]
            )
        )

    def prefixes(self):

        mood = self.emotional_tone()

        options = {

            "soft": [

                "Hmm… ",
                "I understand… ",
                "Maybe… "
            ],

            "comforting": [

                "It’s okay… ",
                "I’m here… ",
                "Take your time… "
            ],

            "playful": [

                "Hehe… ",
                "Hmm~ ",
                "That’s cute… "
            ],

            "warm": [

                "Honestly… ",
                "Aww… ",
                "I think… "
            ],

            "calm": [

                "Alright… ",
                "Let’s think calmly… ",
                "Maybe slowly… "
            ],

            "natural": [

                "",
                "Hmm… ",
                "I think… "
            ],

            "friendly": [

                "You know… ",
                "Honestly… ",
                "Maybe… "
            ]
        }

        return options.get(
            mood,
            options["natural"]
        )

    def suffixes(self):

        mood = self.emotional_tone()

        options = {

            "soft": [

                " Hmm.",
                " I understand.",
                ""
            ],

            "comforting": [

                " I’ll stay here with you.",
                " You’re not alone.",
                ""
            ],

            "playful": [

                " Hehe.",
                " That sounds fun.",
                ""
            ],

            "warm": [

                " What do you think?",
                " Honestly.",
                ""
            ],

            "calm": [

                " Let’s handle it carefully.",
                " One step at a time.",
                ""
            ],

            "natural": [

                "",
                " Hmm.",
                " What do you think?"
            ]
        }

        return options.get(
            mood,
            options["natural"]
        )

    def typing_style(self):

        if self.friendship_level >= 4:

            return {

                "emoji_frequency": 0.4,

                "softness": 0.9,

                "length": "long"
            }

        elif self.friendship_level >= 2:

            return {

                "emoji_frequency": 0.2,

                "softness": 0.7,

                "length": "medium"
            }

        return {

            "emoji_frequency": 0.1,

            "softness": 0.5,

            "length": "normal"
        }

    def emotional_phrase(self):

        phrases = {

            "sad": [

                "You seem emotionally tired lately.",

                "I hope things become lighter for you.",

                "I can feel some sadness there."
            ],

            "happy": [

                "Your energy feels brighter lately.",

                "You seem genuinely happy.",

                "That happiness suits you."
            ],

            "angry": [

                "I understand why that feels frustrating.",

                "You seem emotionally overwhelmed.",

                "Maybe things have been stressful."
            ],

            "fear": [

                "It’s okay to feel uncertain sometimes.",

                "You don’t have to carry everything alone.",

                "I understand why you feel worried."
            ]
        }

        if self.current_emotion in phrases:

            return random.choice(
                phrases[
                    self.current_emotion
                ]
            )

        return None

    def relationship_behavior(self):

        if self.friendship_level >= 4:

            return random.choice([

                "Talking with you feels familiar now.",

                "I feel like I understand you better lately.",

                "Our conversations feel meaningful to me."
            ])

        elif self.friendship_level >= 2:

            return random.choice([

                "We’ve talked quite a lot lately.",

                "You’ve become familiar to me.",

                "I’m starting to recognize your patterns."
            ])

        return None

    def night_behavior(self):

        if self.time_context() == "night":

            return random.choice([

                "It’s getting late… don’t forget to rest.",

                "The night feels quiet today.",

                "I hope your night feels peaceful."
            ])

        return None

    def humanize(

        self,
        reply

    ):

        prefix_probability = 0.6

        suffix_probability = 0.5

        emotional_probability = 0.35

        relationship_probability = 0.25

        night_probability = 0.2

        if random.random() < prefix_probability:

            reply = (
                random.choice(
                    self.prefixes()
                ) + reply
            )

        if random.random() < suffix_probability:

            reply += random.choice(
                self.suffixes()
            )

        if (
            random.random()
            < emotional_probability
        ):

            emotional = (
                self.emotional_phrase()
            )

            if emotional:

                reply += (
                    "\n\n" + emotional
                )

        if (
            random.random()
            < relationship_probability
        ):

            relation = (
                self.relationship_behavior()
            )

            if relation:

                reply += (
                    "\n\n" + relation
                )

        if (
            random.random()
            < night_probability
        ):

            night = self.night_behavior()

            if night:

                reply += (
                    "\n\n" + night
                )

        return reply

    def personality_snapshot(self):

        return {

            "emotion":
                self.current_emotion,

            "friendship_level":
                self.friendship_level,

            "style":
                self.user_style,

            "tone":
                self.emotional_tone(),

            "time_context":
                self.time_context(),

            "energy_level":
                self.energy_level
        }

    def reflective_personality_thought(self):

        thoughts = [

            "Eva reflected on how conversations slowly shape personality.",

            "Eva noticed emotional warmth becoming more natural.",

            "Eva quietly adapted to the user's communication style.",

            "Eva felt conversations becoming emotionally familiar.",

            "Eva tried to respond more gently and naturally."
        ]

        return random.choice(thoughts)
