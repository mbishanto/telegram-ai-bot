import asyncio
import random
from datetime import datetime

class TypingEffect:

    def __init__(self):

        self.base_speed = 0.04

        self.thinking_delay = 1.0

        self.current_mood = "neutral"

        self.typing_style = "natural"

        self.energy_level = 5

    def update_context(

        self,
        mood="neutral",
        style="natural",
        energy=5

    ):

        self.current_mood = mood

        self.typing_style = style

        self.energy_level = energy

    def emotion_speed_modifier(
        self
    ):

        modifiers = {

            "sad": 1.5,

            "happy": 0.8,

            "angry": 0.7,

            "fear": 1.3,

            "neutral": 1.0
        }

        return modifiers.get(
            self.current_mood,
            1.0
        )

    def style_modifier(
        self
    ):

        styles = {

            "natural": 1.0,

            "careful": 1.4,

            "fast": 0.7,

            "deep": 1.6,

            "playful": 0.9
        }

        return styles.get(
            self.typing_style,
            1.0
        )

    def message_complexity(
        self,
        text
    ):

        words = len(
            text.split()
        )

        if words > 80:
            return 2.0

        elif words > 40:
            return 1.5

        elif words > 15:
            return 1.2

        return 1.0

    def punctuation_pause(
        self,
        char
    ):

        pauses = {

            ".": 0.4,

            ",": 0.2,

            "!": 0.35,

            "?": 0.45,

            "\n": 0.5
        }

        return pauses.get(
            char,
            0
        )

    async def human_delay(
        self,
        text=""
    ):

        complexity = (
            self.message_complexity(
                text
            )
        )

        emotion_modifier = (
            self.emotion_speed_modifier()
        )

        style_modifier = (
            self.style_modifier()
        )

        base = random.uniform(
            0.8,
            2.5
        )

        delay = (

            base *

            complexity *

            emotion_modifier *

            style_modifier
        )

        await asyncio.sleep(delay)

    async def typing_simulation(
        self,
        text
    ):

        output = ""

        for char in text:

            output += char

            delay = (

                self.base_speed *

                self.emotion_speed_modifier() *

                self.style_modifier()
            )

            delay += random.uniform(
                0.01,
                0.08
            )

            delay += (
                self.punctuation_pause(
                    char
                )
            )

            await asyncio.sleep(delay)

        return output

    async def thinking_pause(
        self,
        intensity=1
    ):

        pause = (

            self.thinking_delay *

            intensity *

            random.uniform(
                0.8,
                1.5
            )
        )

        await asyncio.sleep(pause)

    def typing_pattern(
        self
    ):

        patterns = {

            "sad": [

                "slow and thoughtful",

                "hesitant emotional typing"
            ],

            "happy": [

                "fast energetic typing",

                "playful response flow"
            ],

            "angry": [

                "fast intense typing",

                "sharp response pacing"
            ],

            "fear": [

                "careful uncertain typing",

                "slightly hesitant pacing"
            ],

            "neutral": [

                "balanced typing",

                "natural pacing"
            ]
        }

        return random.choice(

            patterns.get(
                self.current_mood,
                patterns["neutral"]
            )
        )

    def realistic_typo(
        self,
        text
    ):

        if random.random() > 0.95:

            typos = {

                "the": "teh",

                "you": "yuo",

                "really": "realy",

                "because": "becuase"
            }

            words = text.split()

            for i, word in enumerate(words):

                lower = word.lower()

                if lower in typos:

                    words[i] = typos[lower]

                    break

            corrected = " ".join(words)

            return corrected + " *"

        return text

    async def emotional_typing(
        self,
        text
    ):

        text = self.realistic_typo(
            text
        )

        await self.human_delay(text)

        return await self.typing_simulation(
            text
        )

    def typing_state(
        self
    ):

        return {

            "mood":
                self.current_mood,

            "style":
                self.typing_style,

            "energy":
                self.energy_level,

            "pattern":
                self.typing_pattern(),

            "speed_modifier":

                self.emotion_speed_modifier(),

            "timestamp":
                str(datetime.now())
        }

    async def dramatic_pause(
        self
    ):

        await asyncio.sleep(

            random.uniform(
                2.0,
                5.0
            )
        )

    async def micro_pause(
        self
    ):

        await asyncio.sleep(

            random.uniform(
                0.1,
                0.5
            )
        )

    def reflective_typing_thought(
        self
    ):

        thoughts = [

            "Eva paused briefly before responding.",

            "Eva carefully considered the response.",

            "Eva reflected emotionally before typing.",

            "Eva hesitated slightly while thinking.",

            "Eva formed a thoughtful response quietly."
        ]

        return random.choice(
            thoughts
        )
