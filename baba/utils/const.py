
BOARD_SIZE = 8
PIXELS_PER_CELL = 9

PROPERTIES = ('you', 'push', 'win', 'hot', 'melt', 'sink')

NOUNS = (
    'baba',
    'flag',
    'wall',
    'rock',
    'grass',
    'skull',
    'key',
    'lava',
    'water',
    'empty'
)

class Entity(str):
    dir = '>'


ENTITIES = tuple(Entity(n.capitalize()) for n in NOUNS)

# Helper functions
isproperty = lambda symbol: symbol in PROPERTIES
isnoun = lambda symbol: symbol in NOUNS
isentity = lambda symbol: symbol in ENTITIES

SYMBOLS = (*PROPERTIES, *NOUNS, *ENTITIES, "is")
issymbol = lambda symbol: symbol in SYMBOLS
isis = lambda symbol: symbol == "is"

TEXT = (*PROPERTIES, *NOUNS, "is")
istext = lambda symbol: symbol in TEXT
isempty = lambda cell: cell == "."
