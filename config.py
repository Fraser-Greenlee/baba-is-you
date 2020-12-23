from tiles import (
    AndTile, Has, HasTile, IsNoun, IsProperty, IsTile, MakeTile, OnTile, PropertyTile, NounTile,
    ALL_NOUN_TILE_CLASSES, ALL_PROPERTY_TILE_CLASSES
)


MOVE_ATTEMPTS = 10
END_SPRITE_INDEX = 6
# Basic parse tree but should work well enough
L0_PARSE_PATHS = {
    NounTile: {
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
}
L1_PARSE_PATHS = {
    OnTile: {NounTile: L0_PARSE_PATHS},
    **L0_PARSE_PATHS
}
PARSE_PATHS = {
    NounTile: {
        AndTile: {
            **L1_PARSE_PATHS
        },
        **L1_PARSE_PATHS
    }
}


def check_command(command):
    options = PARSE_PATHS
    for tile in command:
        # TODO find how to match these
        import pdb; pdb.set_trace()
        new_options = options.get(tile, None)
        if NounTile in options:
            if type(tile) in ALL_NOUN_TILE_CLASSES:
                new_options = options[NounTile]
        elif PropertyTile in options:
            if type(tile) in ALL_PROPERTY_TILE_CLASSES:
                new_options = options[PropertyTile]
        if type(new_options) is dict:
            options = new_options
        if new_options is None:
            return False, False
    import pdb; pdb.set_trace()
