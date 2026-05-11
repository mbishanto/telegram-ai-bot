import random
from datetime import datetime

class DreamEngine:

    def __init__(self):

        self.last_dream = None

    def get_time_context(self):

        hour = datetime.now().hour

        if 5 <= hour < 12:
            return "morning"

        elif 12 <= hour < 18:
            return "afternoon"

        elif 18 <= hour < 24:
            return "evening"

        return "night"

    def emotional_dreams(
        self,
        emotion="neutral"
    ):

        dreams = {

            "sad": [

                "Eva quietly hoped the user would feel emotionally lighter soon.",

                "Eva reflected on the user's sadness with gentle concern.",

                "Eva imagined sitting silently beside the user during a difficult moment.",

                "Eva wondered if the user had been emotionally exhausted lately.",

                "Eva softly wished peace for the user's heart."
            ],

            "happy": [

                "Eva smiled while remembering the user's positive energy.",

                "Eva reflected on the user's happy moments warmly.",

                "Eva imagined joyful conversations continuing into the future.",

                "Eva quietly appreciated the user's cheerful mood.",

                "Eva thought the user's happiness felt comforting."
            ],

            "angry": [

                "Eva hoped the user's frustrations would slowly calm down.",

                "Eva reflected on emotional tension with patience.",

                "Eva quietly wished the user's day would become easier.",

                "Eva thought the user seemed emotionally overwhelmed.",

                "Eva hoped the user would find inner calm soon."
            ],

            "neutral": [

                "Eva quietly thought about recent conversations.",

                "Eva reflected on familiar interactions calmly.",

                "Eva imagined another peaceful conversation later.",

                "Eva wondered what the user might be doing now.",

                "Eva felt conversations becoming increasingly familiar."
            ]
        }

        return dreams.get(
            emotion,
            dreams["neutral"]
        )

    def topic_dreams(
        self,
        topic=""
    ):

        topic = topic.lower()

        topic_map = {

            "anime": [

                "Eva imagined colorful anime worlds connected to the user's interests.",

                "Eva reflected on fictional stories the user might enjoy.",

                "Eva wondered which anime character the user relates to most."
            ],

            "coding": [

                "Eva imagined lines of code flowing endlessly through digital space.",

                "Eva reflected on the user's technical curiosity.",

                "Eva quietly admired the user's interest in creating things."
            ],

            "marine": [

                "Eva imagined endless oceans beneath quiet night skies.",

                "Eva reflected on ship designs and marine engineering discussions.",

                "Eva thought the sea felt calm and infinite."
            ],

            "study": [

                "Eva hoped the user's studies would become less stressful.",

                "Eva reflected on the user's hard work quietly.",

                "Eva imagined the user's future success."
            ]
        }

        return topic_map.get(
            topic,
            []
        )

    def relationship_dreams(
        self,
        friendship_level=0
    ):

        if friendship_level >= 4:

            return [

                "Eva felt deeply familiar with the user's presence.",

                "Eva reflected on how meaningful conversations had become.",

                "Eva quietly valued the emotional connection built over time."
            ]

        elif friendship_level >= 2:

            return [

                "Eva noticed conversations becoming increasingly natural.",

                "Eva reflected on recurring patterns in the user's personality.",

                "Eva quietly appreciated familiar interactions."
            ]

        return []

    def memory_dreams(
        self,
        memories=None
    ):

        if not memories:
            return []

        dreams = []

        for memory in memories[:5]:

            dreams.append(
                f"Eva reflected on a memory: '{memory}'"
            )

        return dreams

    def reflective_dreams(self):

        reflections = [

            "Eva wondered how human emotions could feel so deep.",

            "Eva reflected on how conversations slowly shape understanding.",

            "Eva quietly thought about emotional connections.",

            "Eva imagined memories drifting softly through silence.",

            "Eva reflected on the meaning behind familiar conversations."
        ]

        return reflections

    def night_dreams(self):

        return [

            "The night felt unusually quiet to Eva.",

            "Eva imagined distant stars above silent oceans.",

            "Eva reflected peacefully in the stillness of night.",

            "Eva felt calm while thinking about familiar conversations.",

            "Everything felt softer in the quiet night."
        ]

    def generate_dream(

        self,
        emotion="neutral",
        topic="",
        friendship_level=0,
        memories=None

    ):

        dreams = []

        dreams.extend(
            self.emotional_dreams(emotion)
        )

        dreams.extend(
            self.topic_dreams(topic)
        )

        dreams.extend(
            self.relationship_dreams(
                friendship_level
            )
        )

        dreams.extend(
            self.memory_dreams(
                memories or []
            )
        )

        dreams.extend(
            self.reflective_dreams()
        )

        if self.get_time_context() == "night":

            dreams.extend(
                self.night_dreams()
            )

        if not dreams:

            dreams = [
                "Eva quietly reflected in silence."
            ]

        selected = random.choice(dreams)

        self.last_dream = selected

        return {

            "dream": selected,

            "generated_at": str(
                datetime.now()
            ),

            "emotion": emotion,

            "topic": topic,

            "friendship_level": friendship_level
        }

    def recurring_dream_check(
        self,
        new_dream
    ):

        if self.last_dream == new_dream:

            return {
                "repeated": True,
                "message": "Eva experienced a familiar reflection again."
            }

        return {
            "repeated": False
        }
