from collections import deque
from itertools import chain, repeat


__all__ = [
    "PROPERTIES",
    "NOUNS",
    "ENTITIES",
    "isproperty",
    "isnoun",
    "isentity",
    "SYMBOLS",
    "issymbol",
    "isis",
    "istext",
    "isempty",
    "grid_to_string",
    "string_to_grid",
    "default_grid_string",
    "default_grid",
    "transpose",
    "fliplr",
    "rotate_p90",
    "rotate_m90",
    "rotate_180",
    "empty_NM",
    "make_behaviour",
    "isvalidgrid",
    "symbol_to_name",
]


PROPERTIES = ("y", "p", "n")
PROPERTY_NAMES = ("you", "push", "win")

NOUNS = ("b", "w", "f", "r")
NOUN_NAMES = ("baba", "wall", "flag", "rock")

ENTITIES = tuple(n.upper() for n in NOUNS)
ENTITY_NAMES = tuple(n.capitalize() for n in NOUN_NAMES)

# Helper functions
isproperty = lambda symbol: symbol in PROPERTIES
isnoun = lambda symbol: symbol in NOUNS
isentity = lambda symbol: symbol in ENTITIES

SYMBOLS = (*PROPERTIES, *NOUNS, *ENTITIES, "i")
SYMBOL_NAMES = (*PROPERTY_NAMES, *NOUN_NAMES, *ENTITY_NAMES, "is")
issymbol = lambda symbol: symbol in SYMBOLS
isis = lambda symbol: symbol == "i"

TEXT = (*PROPERTIES, *NOUNS, "i")
TEXT_NAMES = (*PROPERTY_NAMES, *NOUN_NAMES, "is")
istext = lambda symbol: symbol in TEXT
isempty = lambda cell: cell == "."


def windowed(seq, n, fillvalue=None, step=1):
    if n < 0:
        raise ValueError('n must be >= 0')
    if n == 0:
        yield tuple()
        return

    window = deque(maxlen=n)
    i = n
    for _ in map(window.append, seq):
        i -= 1
        if not i:
            i = step
            yield tuple(window)

    size = len(window)
    if size == 0:
        return
    elif size < n:
        yield tuple(chain(window, repeat(fillvalue, n - size)))
    elif 0 < i < min(step, n):
        window += (fillvalue,) * i
        yield tuple(window)


def flatten(listOfLists):
    return chain.from_iterable(listOfLists)


def grid_to_string(grid, row_delimiter="\n", col_delimiter=""):
    """Convert grid to multiline string"""
    return row_delimiter.join(col_delimiter.join(row) for row in grid)



def string_to_grid(string, row_delimiter="\n", col_delimiter=""):
    """Convert multiline string to grid"""
    return [
        [cell for cell in row.replace(col_delimiter, "")]
        for row in string.split(row_delimiter)
    ]



def default_grid_string():
    """Hardcoded default grid string"""
    return ".............\n.rip....RRR..\n.......R...R.\n.biy.B.R.F.R.\n.......R...R.\n.fin....RRR..\n............."


def default_grid():
    """Hardcoded default grid"""
    return [
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", "r", "i", "p", ".", ".", ".", ".", "R", "R", "R", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "R", ".", ".", ".", "R", "."],
        [".", "b", "i", "y", ".", "B", ".", "R", ".", "F", ".", "R", "."],
        [".", ".", ".", ".", ".", ".", ".", "R", ".", ".", ".", "R", "."],
        [".", "f", "i", "n", ".", ".", ".", ".", "R", "R", "R", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    ]



def transpose(grid):
    return [list(col) for col in zip(*grid)]


def fliplr(grid):
    return [list(reversed(row)) for row in grid]


def rotate_p90(grid):
    """Rotate grid 90 deg clockwise"""
    return fliplr(transpose(grid))


def rotate_m90(grid):
    """Rotate grid 90 deg counterclockwise"""
    return transpose(fliplr(grid))


def rotate_180(grid):
    """Rotate grid 180 deg"""
    return rotate_p90(rotate_p90(grid))





def empty_NM(N, M, element="."):
    """Make an empty NxM grid"""
    return [[element for _ in range(M)] for _ in range(N)]


def make_behaviour(you=False, push=False, win=False):
    """Helper to make a behaviour"""
    return dict(zip(PROPERTIES, (you, push, win)))





def isvalidgrid(grid):
    """A pile of assertion to check that the grid is valid"""

    # Make sure grid is a list of lists
    assert isinstance(grid, list), "Grid is not a list"
    assert len(grid) > 0, "Grid is an empty list"
    assert isinstance(grid[0], list), "Grid must be a list of lists"

    N, M = len(grid), len(grid[0])

    assert M > 0, "Grid has zero width"

    for row in grid:
        assert len(row) == M, "Grid must be rectangular"
        for cell in row:
            assert cell in (*SYMBOLS, "."), f"'{cell}' is not a valid symbol"


def symbol_to_name(symbol):
    """Give a full name of a symbol"""
    for s, name in zip(SYMBOLS, SYMBOL_NAMES):
        if symbol == s:
            return name
