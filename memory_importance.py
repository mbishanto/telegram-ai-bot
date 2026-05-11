def calculate_importance(memory):

    score = 0

    important_words = [

        "family",
        "dream",
        "goal",
        "important",
        "relationship",
        "love",
        "study",
        "job",
        "emotion"
    ]

    memory_lower = memory.lower()

    for word in important_words:

        if word in memory_lower:
            score += 2

    if len(memory.split()) > 6:
        score += 1

    return score
