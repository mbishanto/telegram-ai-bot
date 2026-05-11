class SemanticMemory:

    def __init__(self):

        self.memories = []

    def save_memory(self, text):

        self.memories.append(text)

    def search_memory(self, query):

        query = query.lower()

        results = []

        for memory in self.memories:

            if query in memory.lower():
                results.append(memory)

        return results[:5]
