import tiles
from coordinate import *
from model import *

class Board:

    def __init__(self):
        self.grid = {}
        Grid(self.grid)
        self.grid[Coordinate(0,0).val] = start_tile
        start_tile.activate(Coordinate(0,0))
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.deck = tiles.Deck()

    def draw(self):
        piece = self.deck.draw()
        while piece and not self.piece_playable(piece):
            piece = self.deck.draw()
        return piece

    def add(self, tile, coordinate):
        if not self.playable(tile, coordinate):
            return False

        self.grid[coordinate] = tile
        for neighbor in self.get_neighbors(coordinate):
            tiles.combine_territories(tile, neighbor[0], neighbor[1])

        # update dimensions of grid
        self.expand_grid(coordinate.x, coordinate.y)
            
        return True

    def expand_grid(self, x, y):
        if x > self.max_x:
            self.max_x = x
        if x < self.min_x:
            self.min_x = x
        if y > self.max_y:
            self.max_y = y
        if y < self.min_y:
            self.min_y = y

    def playable(self, tile, coordinate):
        if coordinate.val in self.grid or not self.has_adjacent(coordinate):
            return False

        for pos in sides:
            co = coordinate.neighbor(pos).val
            if co in self.grid:
                neighbor = self.grid[co]
                if not neighbor.secs[opp_pos(pos, pos in hor_sides)].connectable(tile.secs[pos]):
                    return False
            else:
                continue
        return True
            
    def get_neighbors(self, coordinate):
        neighbors = []
        for side in sides:
            neighbor_coord = coordinate.neighbor(side).val
            if neighbor_coord in self.grid:
                neighbors.append((self.grid[neighbor_coord], side))
        return neighbors

    def has_adjacent(self, coordinate):
        return len(self.get_neighbors(coordinate)) != 0

    def fitting_pieces(self, coordinate):
        pieces = 0
        for tile in tile_types:
            for i in range(4):
                if self.playable(tile, coordinate):
                    pieces += self.deck.num_left(tile)
                    break
                tile.rotate()
        return pieces

    def piece_playable(self, tile):
        if not tile:
            return False
        playable = False
        for i in range(4):
            for x in range(self.min_x-1, self.max_x+2):
                for y in range(self.min_y-1, self.max_y+2):
                    coordinate = Coordinate(x, y)
                    if self.playable(tile, coordinate):
                        playable = True
                        break
                if playable:
                    break
            if playable:
                break
            tile.rotate()
        return playable

    def get_model_sections(self):
        models = set([])
        for coord in self.grid:
            tile = self.grid[coord]
            for pos in all_secs:
                section = tile.secs[pos]
                if pos == (0,0) and section.marker != cloister:
                    continue
                models.add(section)
        return models

    def get_models(self):
        model_sections = self.get_model_sections()
        return [m.model for m in model_sections]
