import enum


class Key(enum.Enum):
    CLICK = 0
    KEYDOWN = 1

    def __str__(self):
        return self.name
