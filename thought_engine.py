def internal_thought(user_text):

    thought = {

        "emotion_detected": "neutral",
        "needs_search": False,
        "reply_style": "calm"
    }

    text = user_text.lower()

    if "sad" in text:
        thought["emotion_detected"] = "sad"
        thought["reply_style"] = "comforting"

    if "news" in text or "latest" in text:
        thought["needs_search"] = True

    return thought
