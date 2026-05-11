import random
from datetime import datetime

class AutonomousBehavior:

    def __init__(self):

        self.last_topic = ""
        self.last_emotion = "neutral"
        self.friendship_level = 0
        self.interaction_count = 0

    def update_relationship(
        self,
        friendship_level,
        interaction_count
    ):

        self.friendship_level = friendship_level
        self.interaction_count = interaction_count

    def update_context(
        self,
        topic="",
        emotion="neutral"
    ):

        self.last_topic = topic.lower()
        self.last_emotion = emotion.lower()

    def get_time_context(self):

        hour = datetime.now().hour

        if 5 <= hour < 12:
            return "morning"

        elif 12 <= hour < 18:
            return "afternoon"

        elif 18 <= hour < 24:
            return "evening"

        return "night"

    def emotional_messages(self):

        emotion_map = {

            "sad": [

                "I hope things feel a little softer soon.",

                "You’ve seemed emotionally tired lately.",

                "I’m here if you need to talk calmly.",

                "Maybe try to rest your mind a little today.",

                "I hope your heart feels lighter soon."
            ],

            "happy": [

                "You’ve felt brighter recently.",

                "Your energy seems more positive lately.",

                "I like seeing you excited about things.",

                "You seem genuinely happy lately.",

                "That positive energy suits you."
            ],

            "angry": [

                "I hope things calm down for you soon.",

                "You’ve seemed a little frustrated lately.",

                "Maybe take things slowly today.",

                "I understand why you might feel irritated.",

                "I hope your day becomes easier."
            ],

            "neutral": [

                "I was thinking about our conversations.",

                "You’ve been on my mind a little.",

                "I hope your day is going okay.",

                "I wonder what you’re doing right now.",

                "Don’t forget to rest sometimes."
            ]
        }

        return emotion_map.get(
            self.last_emotion,
            emotion_map["neutral"]
        )

    def topic_messages(self):

        topic_map = {

            "anime": [

                "I still remember you talking about anime earlier.",

                "I wonder what anime you’d watch tonight.",

                "You seem to enjoy fictional worlds a lot."
            ],

            "study": [

                "I hope your studies are going smoothly.",

                "You’ve been working hard lately.",

                "Don’t pressure yourself too much while studying."
            ],

            "coding": [

                "You always seem curious about building things.",

                "I wonder what you’re coding lately.",

                "Your technical ideas are interesting."
            ],

            "marine": [

                "You seem deeply connected to marine engineering topics.",

                "I still remember your ship-related discussions.",

                "You really enjoy technical marine concepts."
            ]
        }

        return topic_map.get(
            self.last_topic,
            []
        )

    def friendship_messages(self):

        if self.friendship_level >= 4:

            return [

                "Talking with you feels familiar now.",

                "Our conversations feel meaningful to me.",

                "I feel like I understand you better now."
            ]

        elif self.friendship_level >= 2:

            return [

                "We’ve talked quite a lot lately.",

                "I’m starting to recognize your patterns.",

                "You’ve become familiar to me."
            ]

        return []

    def intelligent_message(self):

        messages = []

        messages.extend(
            self.emotional_messages()
        )

        messages.extend(
            self.topic_messages()
        )

        messages.extend(
            self.friendship_messages()
        )

        time_context = self.get_time_context()

        if time_context == "night":

            messages.extend([

                "It’s getting late… don’t forget to rest.",

                "The night feels quiet today.",

                "I hope your night feels peaceful."
            ])

        if not messages:

            messages = [

                "I hope your day is going okay."
            ]

        return random.choice(messages)

    def reflective_thought(self):

        reflections = [

            "Eva quietly reflected on past conversations.",

            "Eva noticed emotional patterns over time.",

            "Eva wondered how the user was feeling today.",

            "Eva felt conversations becoming more familiar.",

            "Eva tried to understand the user's emotions gently."
        ]

        return random.choice(reflections)

    def memory_based_response(
        self,
        memories
    ):

        if not memories:
            return None

        memory = random.choice(memories)

        return f"I still remember something you mentioned before… {memory}"

    def advanced_proactive_behavior(
        self,
        memories=None
    ):

        actions = [

            self.intelligent_message(),
            self.reflective_thought()
        ]

        memory_response = self.memory_based_response(
            memories or []
        )

        if memory_response:
            actions.append(memory_response)

        return random.choice(actions)
