import re

from tiles import (
    Has, Make, IsNoun, IsProperty
)


MOVE_ATTEMPTS = 10
END_SPRITE_INDEX = 6
PARSE_REGEX = {
    r'(noun(.* and noun)?( on noun)? is( not)? noun)': IsNoun,
    r'(noun(.* and noun)?( on noun)? has noun)': Has,
    r'(noun(.* and noun)?( on noun)? make noun)': Make,
    r'(noun(.* and noun)?( on noun)? is( not)? property(.* and property)?)': IsProperty,
}


def parse_text(tiles):
    text_str = ' '.join(str(tile) for tile in tiles)
    logic_with_args = []

    for regex, logic_class in PARSE_REGEX.items():
        matches = [recursive_matches[0] for recursive_matches in re.findall(regex, text_str)]
        for match in matches:
            logic_with_args.append([
                logic_class, match
            ])
    import pdb; pdb.set_trace()
    return logic_with_args
