import enum


class Key(enum.Enum):
    CLICK = 0
    KEYDOWN = 1


    @staticmethod
    def to_dict():
        d = {}
        for i, n in enumerate(Key.__members__):
            d[n] = i
        return d

    @staticmethod
    def get_names() -> [str]:
        out = []
        for i in Key.__members__:
            out.append(i)
        return out

    @staticmethod
    def get_val(entry):
        for i in Key.__members__.items():
            if entry == i[0]:
                return i[1]

    # def __str__(self):
    #     return self.name


if __name__ == '__main__':
    k = Key.KEYDOWN
    # for i in Key.__members__.items():
    #     print(type(i[1]))
    # print(Key.__members__.items())
    # print(Key.to_dict())
