def decay_memories(memories):

    cleaned = []

    for memory in memories:

        if len(memory.split()) >= 3:
            cleaned.append(memory)

    return cleaned[-100:]
