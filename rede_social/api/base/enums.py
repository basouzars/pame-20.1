# Models enums with choices

class Enum:
    class Meta:
        abstract = True

    choices = []

    @classmethod
    def get_label(cls, key):
        for k, v in cls.choices:
            if key == k:
                return v
        return None


class ProductCategories(Enum):
    COMPUTERS = 'COMPUTERS'
    BABY = 'BABY'
    TOYS = 'TOYS'
    VIDEO_GAMES = 'VIDEO_GAMES'

    choices = [
        (COMPUTERS, 'Computadores'),
        (BABY, 'Para bebês'),
        (TOYS, 'Brinquedos'),
        (VIDEO_GAMES, 'Videogames'),
    ]
