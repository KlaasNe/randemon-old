class Layer:

    def __init__(self, name, size):
        self.name = name
        self.sx, self.sy = size
        self.tiles = dict()

    def get_name(self):
        return self.name

    def get_tile(self, pos, default=""):
        return self.tiles.get(pos, default)

    def get_tile_type(self, pos, default=""):
        try:
            return self.tiles.get(pos, default)[0]
        except IndexError:
            return default

    def set_tile(self, pos, tile):
        self.tiles[pos] = tile

    def rm_tile(self, pos):
        self.tiles.pop(pos)

    def has_tile_at(self, pos):
        return self.get_tile(pos) != ""

    def get_tiles(self):
        return self.tiles

    def empty_area(self, pos1, pos2):
        for y in range(pos1[1], pos2[1]):
            for x in range(pos1[0], pos2[0]):
                if (x, y) in self.get_ex_pos():
                    return False
        return True

    def filled_area(self, pos1, pos2):
        for y in range(pos1[1], pos2[1]):
            for x in range(pos1[0], pos2[0]):
                if (x, y) not in self.get_ex_pos():
                    return False
        return True

    def get_ex_pos(self):
        return self.tiles.keys()

    def out_of_bounds(self, x, y):
        return any((x < 0, y < 0, x >= self.sx, y >= self.sy))
