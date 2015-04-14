from random import *
from tile import *
from section import *

start_tile = Tile('start_tile', [(castle, [top]), (road,[left,right]), (road,[center]), (farm,[tleft,tright]), (farm,full_side[bottom])])

cloister_plain = Tile('cloister_plain', [(cloister,[center]), (farm,all_out_secs)])

cloister_road = Tile('cloister_road', [(cloister,[center]), (farm,[left,tleft,top,tright,right,bright,bleft]), (road,[bottom])])

castle4 = Tile('castle4', [(castle,sides), (castle,[center]), (farm,[tleft]), (farm,[tright]), (farm,[bright]), (farm,[bleft])])

castle3 = Tile('castle3', [(castle,[left,top,right]), (castle,[center]), (farm,[tleft]), (farm,[tright]), (farm,full_side[bottom])])

castle3_road = Tile('castle3_road', [(castle,[left,top,right]), (castle,[center]), (farm,[tleft]), (farm,[tright]), (farm,[bright]), (farm,[bleft]), (road,[bottom])])

castle2 = Tile('castle2', [(farm,[tright,right,bright,bottom,bleft]), (castle,[center]), (castle,[left,top]), (farm,[tleft])])

castle2_road = Tile('castle2_road', [(farm,[tright,bleft]), (farm,[center]), (farm,[bright]), (castle,[left,top]), (farm,[tleft]), (road,[right,bottom])])

castle_farm2 = Tile('castle_farm2', [(castle,[left,right]), (castle,[center]), (farm,full_side[top]), (farm,full_side[bottom])])

farm_castle2 = Tile('farm_castle2', [(farm,[left,tleft,tright,right,bright,bleft]), (farm,[center]), (castle,[top]), (castle,[bottom])])

butt = Tile('butt', [(farm,[tleft,tright,right,bright,bottom,bleft]), (farm,[center]), (castle,[left]), (castle,[top])])

castle_end = Tile('castle_end', [(farm,[left,tleft,tright,right,bright,bottom,bleft]), (farm,[center]), (castle,[top])])

castle_end_road_l = Tile('castle_end_road_l', [(farm,[tleft,tright,right,bright]), (farm,[center]), (castle,[top]), (road,[left,bottom]), (farm,[bleft])])

castle_end_road_r = Tile('castle_end_road_r',[(farm,[left,tleft,tright,bleft]), (farm,[center]), (castle,[top]), (road,[right,bottom]), (farm,[bright])])

castle_end_road3 = Tile('castle_end_road3', [(farm,[center]), (farm,[tleft,tright]), (farm,[bright]), (farm,[bleft]), (castle,[top]), (road,[left]), (road,[right]), (road,[bottom])])

castle_end_road = Tile('castle_end_road', [(castle, [top]), (road,[left,right]), (road,[center]), (farm,[tleft,tright]), (farm,full_side[bottom])])

road_tile = Tile('road', [(road,[top,bottom]), (road,[center]), (farm,full_side[left]), (farm,full_side[right])])

road_bend = Tile('road_bend', [(farm,[tleft,top,tright,right,bright]), (farm,[center]), (farm,[bleft]), (road,[left,bottom])])

road3 = Tile('road3', [(farm,[center]), (farm,full_side[top]), (farm,[bright]), (farm,[bleft]), (road,[left]), (road,[right]), (road,[bottom])])

road4 = Tile('road4', [(farm,[center]), (farm,[tleft]), (farm,[tright]), (farm,[bright]), (farm,[bleft]), (road,[left]), (road,[top]), (road,[right]), (road,[bottom])])

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

