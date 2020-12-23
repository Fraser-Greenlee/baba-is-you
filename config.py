from tiles import (
    AndTile, Has, HasTile, IsNoun, IsProperty, IsTile, MakeTile, OnTile, PropertyTile, NounTile
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