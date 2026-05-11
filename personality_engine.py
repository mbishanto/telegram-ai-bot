import random

def add_human_style(reply):

    prefixes = [

        "",
        "Hmm… ",
        "I think… ",
        "Maybe… ",
        "Honestly… "
    ]

    suffixes = [

        "",
        " What do you think?",
        " Hmm.",
        ""
    ]

    if random.random() > 0.5:
        reply = random.choice(prefixes) + reply

    if random.random() > 0.7:
        reply += random.choice(suffixes)

    return reply
