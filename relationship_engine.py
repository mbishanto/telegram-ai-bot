class RelationshipEngine:

    def __init__(self):

        self.level = 0
        self.interactions = 0

    def update(self):

        self.interactions += 1

        if self.interactions > 10:
            self.level = 1

        if self.interactions > 30:
            self.level = 2

        if self.interactions > 60:
            self.level = 3

        if self.interactions > 120:
            self.level = 4

        return {
            "level": self.level,
            "interactions": self.interactions
        }
