from tiles import (
    AndTile, Has, HasTile, IsNoun, IsProperty, IsTile, MakeTile, OnTile, PropertyTile, NounTile,
    ALL_NOUN_TILE_CLASSES, ALL_PROPERTY_TILE_CLASSES
)


MOVE_ATTEMPTS = 10
END_SPRITE_INDEX = 6
# Basic parse tree but should work well enough
L0_PARSE_PATHS = {
    IsTile: {
        NounTile: IsNoun,
        PropertyTile: {
            None: IsProperty,
            AndTile: {
                PropertyTile: {
                    None: IsProperty,
                    AndTile: {PropertyTile: IsProperty},
                },
            }
        }
    },
    HasTile: {NounTile: Has},
    MakeTile: {NounTile: Has},
}
PARSE_PATHS = {
    NounTile: {
        AndTile: {
            NounTile: L0_PARSE_PATHS
        },
        OnTile: {
            NounTile: L0_PARSE_PATHS
        },
        **L0_PARSE_PATHS
    }
}


def check_command(command):
    options = PARSE_PATHS
    for tile in command:
        # TODO find how to match these
        if NounTile in options and type(tile) in ALL_NOUN_TILE_CLASSES:
            options = options[NounTile]
        elif PropertyTile in options and type(tile) in ALL_PROPERTY_TILE_CLASSES:
            options = options[PropertyTile]
        else:
            options = options.get(type(tile), None)
        if options is None:
            return False, False, None
    if None in options:
        options = options.get(None, None)
    return bool(options), True, options
