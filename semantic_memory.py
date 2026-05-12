from datetime import datetime
from collections import Counter
import random
import math

class SemanticMemory:

    def __init__(self):

        self.memories = []

        self.max_memories = 1000

        self.memory_links = {}

        self.topic_frequency = {}

    def create_memory_object(

        self,
        text,
        emotion="neutral",
        topic="general"

    ):

        return {

            "text": text,

            "emotion": emotion,

            "topic": topic,

            "created_at":
                str(datetime.now()),

            "last_accessed":
                str(datetime.now()),

            "recall_count": 0,

            "importance": 1,

            "embedding_tags":
                self.extract_keywords(text)
        }

    def extract_keywords(
        self,
        text
    ):

        words = text.lower().split()

        ignored = [

            "the",
            "a",
            "an",
            "is",
            "are",
            "and",
            "or",
            "to",
            "of",
            "in"
        ]

        keywords = [

            word.strip(".,!?")

            for word in words

            if word not in ignored
        ]

        return list(set(keywords))

    def save_memory(

        self,
        text,
        emotion="neutral",
        topic="general"

    ):

        memory = self.create_memory_object(

            text,
            emotion,
            topic
        )

        self.memories.append(memory)

        self.memories = (
            self.memories[
                -self.max_memories:
            ]
        )

        self.update_topic_frequency(
            topic
        )

        self.link_related_memories(
            memory
        )

        return memory

    def update_topic_frequency(
        self,
        topic
    ):

        self.topic_frequency[topic] = (

            self.topic_frequency.get(
                topic,
                0
            ) + 1
        )

    def similarity_score(

        self,
        query_keywords,
        memory_keywords

    ):

        overlap = len(

            set(query_keywords)
            &
            set(memory_keywords)
        )

        total = max(

            len(set(query_keywords)),
            1
        )

        return overlap / total

    def search_memory(

        self,
        query,
        limit=5

    ):

        query_keywords = (
            self.extract_keywords(query)
        )

        scored = []

        for memory in self.memories:

            score = (
                self.similarity_score(

                    query_keywords,

                    memory[
                        "embedding_tags"
                    ]
                )
            )

            if score > 0:

                score += (
                    memory[
                        "recall_count"
                    ] * 0.1
                )

                scored.append((

                    score,
                    memory
                ))

        scored.sort(

            key=lambda x: x[0],

            reverse=True
        )

        results = []

        for score, memory in scored[:limit]:

            memory[
                "recall_count"
            ] += 1

            memory[
                "last_accessed"
            ] = str(datetime.now())

            results.append({

                "text":
                    memory["text"],

                "score":
                    round(score, 2),

                "emotion":
                    memory["emotion"],

                "topic":
                    memory["topic"]
            })

        return results

    def link_related_memories(
        self,
        new_memory
    ):

        new_keywords = (
            new_memory[
                "embedding_tags"
            ]
        )

        related = []

        for memory in self.memories[:-1]:

            similarity = (
                self.similarity_score(

                    new_keywords,

                    memory[
                        "embedding_tags"
                    ]
                )
            )

            if similarity >= 0.4:

                related.append(
                    memory["text"]
                )

        self.memory_links[
            new_memory["text"]
        ] = related[:10]

    def related_memories(
        self,
        text
    ):

        return self.memory_links.get(
            text,
            []
        )

    def memory_clusters(
        self
    ):

        clusters = {}

        for memory in self.memories:

            topic = memory["topic"]

            if topic not in clusters:

                clusters[topic] = []

            clusters[topic].append(
                memory["text"]
            )

        return clusters

    def emotional_memories(
        self,
        emotion
    ):

        return [

            memory

            for memory in self.memories

            if memory["emotion"]
            == emotion
        ]

    def strongest_memories(
        self,
        limit=10
    ):

        sorted_memories = sorted(

            self.memories,

            key=lambda x: (

                x["importance"],

                x["recall_count"]
            ),

            reverse=True
        )

        return sorted_memories[:limit]

    def memory_statistics(
        self
    ):

        emotions = [

            memory["emotion"]

            for memory in self.memories
        ]

        topics = [

            memory["topic"]

            for memory in self.memories
        ]

        return {

            "total_memories":
                len(self.memories),

            "emotion_distribution":
                dict(Counter(emotions)),

            "topic_distribution":
                dict(Counter(topics)),

            "top_topics":
                Counter(topics)
                .most_common(5)
        }

    def reflective_memory_thought(
        self
    ):

        reflections = [

            "Eva quietly connected related memories together.",

            "Eva reflected on recurring conversational patterns.",

            "Eva noticed certain memories becoming emotionally significant.",

            "Eva organized memories through semantic relationships.",

            "Eva felt familiar topics appearing repeatedly."
        ]

        return random.choice(
            reflections
        )

    def semantic_summary(
        self
    ):

        stats = self.memory_statistics()

        return {

            "memory_count":
                stats[
                    "total_memories"
                ],

            "top_topics":
                stats[
                    "top_topics"
                ],

            "reflection":
                self.reflective_memory_thought(),

            "generated_at":
                str(datetime.now())
        }

    def memory_evolution(
        self
    ):

        if len(self.memories) < 10:

            return "Memory system still developing."

        dominant_topics = (

            Counter(

                memory["topic"]

                for memory
                in self.memories
            )

            .most_common(3)
        )

        return {

            "dominant_topics":
                dominant_topics,

            "evolution_stage":
                "advanced semantic growth",

            "reflection":

                "Eva noticed semantic understanding evolving over time."
        }
