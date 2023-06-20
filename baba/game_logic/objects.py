

class Tile:
    sprite_x: int
    sprite_y: int


class Entity(Tile):
    direction = '>'


class Text(Tile):
    pass


TEXT_TILES = {
    (16, 0): 'baba',
    (17, 0): 'flag',
    (18, 0): 'wall',
    (19, 0): 'rock',
    (17, 1): 'grass',
    (20, 3): 'skull',
    (20, 2): 'key',
    (16, 2): 'lava',
    (19, 1): 'water',

    (24, 0): 'is',

    (8, 0): 'you',
    (11, 0): 'push',
    (9, 0): 'win',
    (10, 0): 'hot',
    (12, 0): 'melt',
    (11, 1): 'sink',
}
for (sprite_x, sprite_y), sprite_name in TEXT_TILES.items():
    


ENTITY_TILES = {
    (0, 11): Entity('Baba'),
    (3, 0): Entity('Flag'),
    (4, 0): Entity('Wall'),
    (5, 0): Entity('Rock'),
    (0, 4): Entity('Grass'),
    (4, 4): Entity('Skull'),
    (7, 4): Entity('Key'),
    (5, 4): Entity('Water'),
    (2, 4): Entity('Lava'),
}
