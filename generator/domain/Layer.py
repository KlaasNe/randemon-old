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

    def get_tiles(self):
        return self.tiles

    def get_ex_pos(self):
        return self.tiles.keys()

    def out_of_bounds(self, x, y):
        return any((x < 0, y < 0, x >= self.sx, y >= self.sy))
