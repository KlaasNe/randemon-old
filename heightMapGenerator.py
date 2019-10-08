import random
from math import floor
from noise import snoise2


def create_hills(pmap):
    octaves = 1
    freq = 100
    off_x = random.random() * 1000000
    off_y = random.random() * 1000000

    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            pmap.tile_heights[(x, y)] = abs(floor((snoise2((x + off_x) / freq, (y + off_y) / freq, octaves)) * pmap.max_hill_height))

    create_hill_edges(pmap)


def create_hill_edges(pmap):

    def define_hill_edge_texture(x, y):

        def get_hills_around_tile():
            current_tile_height = pmap.tile_heights[(x, y)]
            hills_around_tile = []
            for around in range(0, 9):
                tile_coordinate = (x + around % 3 - 1, y + around // 3 - 1)
                if pmap.tile_heights.get(tile_coordinate, current_tile_height) == current_tile_height: hills_around_tile.append(0)
                if pmap.tile_heights.get(tile_coordinate, current_tile_height) < current_tile_height: hills_around_tile.append(-1)
                if pmap.tile_heights.get(tile_coordinate, current_tile_height) > current_tile_height: hills_around_tile.append(1)
            return hills_around_tile

        hills_around = get_hills_around_tile()
        if pmap.tile_heights.get((x, y), 0) < 2: return -1
        if hills_around[3] == 0 and hills_around[6] == -1 and hills_around[7] == 0: return 9
        if hills_around[5] == 0 and hills_around[7] == 0 and hills_around[8] == -1: return 10
        if hills_around[0] == -1 and hills_around[1] == 0 and hills_around[3] == 0: return 4
        if hills_around[1] == 0 and hills_around[2] == -1 and hills_around[5] == 0: return 4
        if hills_around[1] == -1 and hills_around[3] == -1 and hills_around[5] == -1 and hills_around[7] == -1: return 15
        if hills_around[1] == -1 and hills_around[3] == 0 and hills_around[5] == -1 and hills_around[7] == -1: return 15
        if hills_around[1] == -1 and hills_around[3] == -1 and hills_around[5] == -1 and hills_around[7] == 0: return 15
        if hills_around[1] == -1 and hills_around[3] == -1 and hills_around[5] == 0 and hills_around[7] == -1: return 15
        if hills_around[1] == 0 and hills_around[3] == -1 and hills_around[5] == -1 and hills_around[7] == -1: return 15
        if hills_around[1] == 0 and hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == 0: return -1
        if hills_around[1] == 0 and hills_around[3] == -1 and hills_around[7] == 0: return 1
        if hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == -1: return 2
        if hills_around[1] == 0 and hills_around[5] == -1 and hills_around[7] == 0: return 3
        if hills_around[1] == -1 and hills_around[3] == 0 and hills_around[5] == 0: return 4
        if hills_around[1] == -1 and hills_around[3] == -1: return 5
        if hills_around[3] == -1 and hills_around[7] == -1: return 6
        if hills_around[5] == -1 and hills_around[7] == -1: return 7
        if hills_around[1] == -1 and hills_around[5] == -1: return 8
        return -1

    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            hill_edge_texture = str(define_hill_edge_texture(x, y))
            if not hill_edge_texture == "-1": pmap.ground_layer[(x, y)] = "m_" + hill_edge_texture


def generate_height_map(pmap):
    tile_heights = dict()
    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            pmap.height_map[(x, y)] = "height_" + str(tile_heights[(x, y)])

# tile_Heights = [] image_grayscale_to_dict("world_height_map_downscaled2.jpg")
