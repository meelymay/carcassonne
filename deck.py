from random import *
from tile import *
from section import *
from territory import *

START_TILE = Tile('start_tile', [(CASTLE, FULL_SIDE[N]),
                                 (ROAD,[W, E]),
                                 (ROAD,[C]),
                                 (FARM, [WNW, ENE]),
                                 (FARM, FULL_SIDE[S] + [ESE, WSW])])

CLOISTER_PLAIN = Tile('cloister_plain', [(CLOISTER, [C]),
                                         (FARM, ALL_SIDES)])
CLOISTER_ROAD = Tile('cloister_road', [(CLOISTER, [C]),
                                       (FARM, FULL_SIDE[W] + FULL_SIDE[N] + FULL_SIDE[E] + [SSW, SSE]),
                                       (ROAD, [S])])
CASTLE4 = Tile('CASTLE4', [(CASTLE, ALL_SIDES),
                           (CASTLE, [C])])
CASTLE3 = Tile('CASTLE3', [(CASTLE, reduce(lambda x, y: x+y, [FULL_SIDE[dir] for dir in [W, N, E]])),
                           (CASTLE, [C]),
                           (FARM, FULL_SIDE[S])])
CASTLE3_ROAD = Tile('CASTLE3_ROAD', [(CASTLE, reduce(lambda x, y: x+y, [FULL_SIDE[dir] for dir in [W, N, E]])),
                                     (ROAD, [S]),
                                     (CASTLE, [C]),
                                     (FARM, [SSW]),
                                     (FARM, [SSE])])
CASTLE2 = Tile('CASTLE2', [(FARM, FULL_SIDE[N] + FULL_SIDE[E]),
                           (CASTLE, [C]),
                           (CASTLE, FULL_SIDE[S] + FULL_SIDE[W])])
CASTLE2_ROAD = Tile('CASTLE2_ROAD', [(FARM, [ENE, SSW]),
                                     (FARM, [SSE, ESE]),
                                     (FARM, [C]),
                                     (CASTLE, FULL_SIDE[W] + FULL_SIDE[N]),
                                     (ROAD, [E, S])])
CASTLE_FARM2 = Tile('CASTLE_FARM2', [(CASTLE, FULL_SIDE[W] + FULL_SIDE[E]),
                                     (FARM, [C]),
                                     (FARM, FULL_SIDE[N]),
                                     (FARM, FULL_SIDE[S])])
FARM_CASTLE2 = Tile('FARM_CASTLE2', [(FARM, FULL_SIDE[E] + FULL_SIDE[W]),
                                     (FARM, [C]),
                                     (CASTLE, FULL_SIDE[N]),
                                     (CASTLE, FULL_SIDE[S])])
BUTT = Tile('BUTT', [(FARM, FULL_SIDE[S] + FULL_SIDE[E]),
                     (FARM, [C]),
                     (CASTLE, FULL_SIDE[W]),
                     (CASTLE, FULL_SIDE[N])])
CASTLE_END = Tile('CASTLE_END', [(FARM, reduce(lambda x, y: x+y, [FULL_SIDE[dir] for dir in [W, S, E]])),
                                 (FARM, [C]),
                                 (CASTLE, FULL_SIDE[N])])
CASTLE_END_ROAD_L = Tile('CASTLE_END_ROAD_L', [(FARM, FULL_SIDE[E] + [WNW, SSE]),
                                               (ROAD, [C]),
                                               (CASTLE, FULL_SIDE[N]),
                                               (ROAD, [W, S]),
                                               (FARM, [SSW, WSW])])
CASTLE_END_ROAD_R = Tile('CASTLE_END_ROAD_R', [(FARM, FULL_SIDE[W] + [ENE, SSW]),
                                               (ROAD, [C]),
                                               (CASTLE, FULL_SIDE[N]),
                                               (ROAD, [E, S]),
                                               (FARM, [SSE, ESE])])
CASTLE_END_ROAD3 = Tile('CASTLE_END_ROAD3', [(ROAD, [C]),
                                             (FARM, [WSW, SSW,]),
                                             (FARM, [ESE, SSE]),
                                             (FARM, [ENE, WNW]),
                                             (CASTLE, FULL_SIDE[N]),
                                             (ROAD, [W]),
                                             (ROAD, [E]),
                                             (ROAD, [S])])
CASTLE_END_ROAD = Tile('CASTLE_END_ROAD', [(CASTLE, FULL_SIDE[N]),
                                           (ROAD, [W, E]),
                                           (ROAD, [C]),
                                           (FARM, [WNW, ENE]),
                                           (FARM, FULL_SIDE[S] + [ESE, WSW])])
ROAD_TILE = Tile('ROAD', [(ROAD, [N, S]),
                          (ROAD, [C]),
                          (FARM, FULL_SIDE[W] + [NNW, SSW]),
                          (FARM, FULL_SIDE[E] + [NNE, SSE])])
ROAD_BEND = Tile('ROAD_BEND', [(FARM, FULL_SIDE[N] + FULL_SIDE[E] + [SSE, WNW]),
                               (ROAD, [C]),
                               (FARM, [SSW, WSW]),
                               (ROAD, [W, S])])
ROAD3 = Tile('ROAD3', [(ROAD, [C]),
                       (FARM, FULL_SIDE[N] + [WNW, ENE]),
                       (FARM, [SSE, ESE]),
                       (FARM, [SSW, WSW]),
                       (ROAD, [W]),
                       (ROAD, [E]),
                       (ROAD, [S])])
ROAD4 = Tile('ROAD4', [(ROAD, [C]),
                       (FARM, [NNW, WNW]),
                       (FARM, [NNE, ENE]),
                       (FARM, [SSE, ESE]),
                       (FARM, [SSW, WSW]),
                       (ROAD, [W]),
                       (ROAD, [N]),
                       (ROAD, [E]),
                       (ROAD, [S])])

TILE_TYPES = [CLOISTER_PLAIN, CLOISTER_ROAD, CASTLE4, CASTLE3, CASTLE3_ROAD, CASTLE2, CASTLE2_ROAD, CASTLE_FARM2, FARM_CASTLE2, BUTT, CASTLE_END, CASTLE_END_ROAD_L, CASTLE_END_ROAD_R, CASTLE_END_ROAD3, CASTLE_END_ROAD, ROAD_TILE, ROAD_BEND, ROAD3, ROAD4]
TILE_NAMES = {}

for tile in TILE_TYPES:
    TILE_NAMES[tile.name] = tile

class Deck:
    
    def __init__(self):
        self.tiles_left = {}
        self.tiles_left[CLOISTER_PLAIN.name] = 4
        self.tiles_left[CLOISTER_ROAD.name] = 2
        self.tiles_left[CASTLE4.name] = 1
        self.tiles_left[CASTLE3.name] = 4
        self.tiles_left[CASTLE3_ROAD.name] = 3
        self.tiles_left[CASTLE2.name] = 5
        self.tiles_left[CASTLE2_ROAD.name] = 5
        self.tiles_left[CASTLE_FARM2.name] = 3
        self.tiles_left[FARM_CASTLE2.name] = 3
        self.tiles_left[BUTT.name] = 2
        self.tiles_left[CASTLE_END.name] = 5
        self.tiles_left[CASTLE_END_ROAD_L.name] = 3
        self.tiles_left[CASTLE_END_ROAD_R.name] = 3
        self.tiles_left[CASTLE_END_ROAD3.name] = 3
        self.tiles_left[CASTLE_END_ROAD.name] = 3
        self.tiles_left[ROAD_TILE.name] = 8
        self.tiles_left[ROAD_BEND.name] = 9
        self.tiles_left[ROAD3.name] = 4
        self.tiles_left[ROAD4.name] = 1

        self.pile = []
        for tile in TILE_TYPES:
            for i in range(self.tiles_left[tile.name]):
                self.pile.append(tile.copy())

    def num_left(self, tile):
        return self.tiles_left[tile.name]

    def draw(self):
        # print 'Tiles W:',len(self.pile)
        if len(self.pile) == 0:
            return None
        i = randint(0,len(self.pile)-1)
        tile = self.pile.pop(i)
        self.tiles_left[tile.name] -= 1
        return tile

if __name__ == '__main__':
    deck = Deck()
    for i in range(50):
        tile = deck.draw()
        print tile.name
        tile.display()
