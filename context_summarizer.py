def summarize_conversation(messages):

    if len(messages) < 10:
        return "Conversation too short."

    summary = []

    for msg in messages[-10:]:

        if msg["role"] == "user":

            summary.append(
                msg["content"]
            )

    return " | ".join(summary[:5])
