def generate_reflection(profile):

    notes = profile.get("notes", [])
    emotions = profile.get("emotions", [])

    reflection = []

    if len(notes) > 10:
        reflection.append(
            "User shares many personal memories."
        )

    if len(emotions) > 5:
        reflection.append(
            "User shows emotional consistency."
        )

    relationship = profile.get(
        "relationship",
        {}
    )

    if relationship.get(
        "friendship_level",
        0
    ) >= 3:

        reflection.append(
            "Strong bond detected with user."
        )

    return reflection
