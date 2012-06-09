from random import *
from tiles import *

start_tile = Tile('start_tile', road, castle, road, farm)
cloister_plain = Tile('cloister_plain', farm, farm, farm, farm)
cloister_road = Tile('cloister_road', farm, farm, farm, road)
castle4 = Tile('castle4', castle, castle, castle, castle, connected=True)
castle3 = Tile('castle3', castle, castle, castle, farm, connected=True)
castle3_road = Tile('castle3_road', castle, castle, castle, road, connected=True)
castle2 = Tile('castle2', castle, castle, farm, farm, connected=True)
castle2_road = Tile('castle2_road', castle, castle, road, road, connected=True)
castle_farm2 = Tile('castle_farm2', castle, farm, castle, farm, connected=True)
farm_castle2 = Tile('farm_castle2', castle, farm, castle, farm)
butt = Tile('butt', castle, castle, farm, farm)
castle_end = Tile('castle_end', castle, farm, farm, farm)
castle_end_road_l = Tile('castle_end_road_l', castle, farm, road, road)
castle_end_road_r = Tile('castle_end_road_r', castle, road, road, farm)
castle_end_road3 = Tile('castle_end_road3', castle, road, road, road)
castle_end_road = Tile('castle_end_road', castle, road, farm, road)
road_tile = Tile('road', road, farm, road, farm)
road_bend = Tile('road_bend', road, farm, farm, road)
road3 = Tile('road3', road, farm, road, road)
road4 = Tile('road4', road, road, road, road)

tile_types = [cloister_plain, cloister_road, castle4, castle3, castle3_road, castle2, castle2_road, castle_farm2, farm_castle2, butt, castle_end, castle_end_road_l, castle_end_road_r, castle_end_road3, castle_end_road, road_tile, road_bend, road3, road4]
tile_names = {}
for tile in tile_types:
    tile_names[tile.name] = tile

class Deck:
    
    def __init__(self):
        self.tiles_left = {}
        self.tiles_left[cloister_plain.name] = 4
        self.tiles_left[cloister_road.name] = 2
        self.tiles_left[castle4.name] = 1
        self.tiles_left[castle3.name] = 4
        self.tiles_left[castle3_road.name] = 3
        self.tiles_left[castle2.name] = 5
        self.tiles_left[castle2_road.name] = 5
        self.tiles_left[castle_farm2.name] = 3
        self.tiles_left[farm_castle2.name] = 3
        self.tiles_left[butt.name] = 2
        self.tiles_left[castle_end.name] = 5
        self.tiles_left[castle_end_road_l.name] = 3
        self.tiles_left[castle_end_road_r.name] = 3
        self.tiles_left[castle_end_road3.name] = 3
        self.tiles_left[castle_end_road.name] = 3
        self.tiles_left[road_tile.name] = 8
        self.tiles_left[road_bend.name] = 9
        self.tiles_left[road3.name] = 4
        self.tiles_left[road4.name] = 1

        self.pile = []
        for tile in tile_types:
            for i in range(self.tiles_left[tile.name]):
                self.pile.append(tile.copy())

    def num_left(self, tile):
        return self.tiles_left[tile.name]

    def draw(self):
        # print 'Tiles left:',len(self.pile)
        if len(self.pile) == 0:
            return None
        i = randint(0,len(self.pile)-1)
        tile = self.pile.pop(i)
        self.tiles_left[tile.name] -= 1
        return tile
