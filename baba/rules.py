from baba.utils import (
    windowed,
    isnoun, isis, isproperty,
    make_behaviour,
    NOUNS
)


def rulefinder(grid):
    """Find all the rules in the grid"""
    N, M = len(grid), len(grid[0])
    rules = []

    # Check every candidate against the grammar
    # Noun is (Noun OR Property)
    isrule = lambda t: (
        isnoun(t[0]) and isis(t[1]) and (isnoun(t[2]) or isproperty(t[2]))
    )

    # Horizontal rules
    if M >= 3:
        for row in grid:
            for t in windowed(row, 3):
                if isrule(t):
                    rules.append((t[0], t[2]))

    # Vertical rules
    if N >= 3:
        for col in zip(*grid):
            for t in windowed(col, 3):
                if isrule(t):
                    rules.append((t[0], t[2]))

    # Sort according to the first letter
    # rules = sorted(rules,key=lambda x:x[0])
    rules = sorted(rules)
    return rules


def ruleparser(rules):
    """Parse valid rules into behaviours and swaps"""

    behaviours = {noun: (make_behaviour()) for noun in NOUNS}
    swaps = []

    # Parse the rules
    for subject, action in rules:
        # Noun is (Noun OR Property)
        if isproperty(action):  # Noun is a Property
            behaviours[subject][action] = True
        else:  # (Noun is Noun)
            swaps.append((subject, action))

    swaps = sorted(swaps)

    # Add entry for text behaviour
    behaviours["text"] = make_behaviour(push=True)

    return behaviours, swaps
