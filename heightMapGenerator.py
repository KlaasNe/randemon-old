import random
from math import floor
from noise import snoise2


def create_hill_map(map_size_x, map_size_y, max_hill_height):
    octaves = 1
    freq = 100
    off_x = random.random() * 1000000
    off_y = random.random() * 1000000

    tile_heights = dict()
    for y in range(0, map_size_y):
        for x in range(0, map_size_x):
            tile_heights[(x, y)] = abs(
                floor((snoise2((x + off_x) / freq, (y + off_y) / freq, octaves)) * max_hill_height))
    return tile_heights


def create_hill_edges(map_size_x, map_size_y, tile_heights):

    def define_hill_edge_texture(height_list, x, y):

        def get_hills_around(x, y):
            current_tile_height = height_list[(x, y)]
            hills_around = []
            for around in range(0, 9):
                tile_coordinate = (x + around % 3 - 1, y + around // 3 - 1)
                if height_list.get(tile_coordinate, current_tile_height) == current_tile_height: hills_around.append(0)
                if height_list.get(tile_coordinate, current_tile_height) < current_tile_height: hills_around.append(-1)
                if height_list.get(tile_coordinate, current_tile_height) > current_tile_height: hills_around.append(1)
            return hills_around

        hills_around = get_hills_around(x, y)
        if height_list.get((x, y), 0) < 2: return -1
        if hills_around[3] == 0 and hills_around[6] == -1 and hills_around[7] == 0: return 9
        if hills_around[5] == 0 and hills_around[7] == 0 and hills_around[8] == -1: return 10
        if hills_around[0] == -1 and hills_around[1] == 0 and hills_around[3] == 0: return 4
        if hills_around[1] == 0 and hills_around[2] == -1 and hills_around[5] == 0: return 4
        elif hills_around[1] == -1 and hills_around[3] == -1 and hills_around[5] == -1 and hills_around[7] == -1: return 15
        elif hills_around[1] == -1 and hills_around[3] == 0 and hills_around[5] == -1 and hills_around[7] == -1: return 15
        elif hills_around[1] == -1 and hills_around[3] == -1 and hills_around[5] == -1 and hills_around[7] == 0: return 15
        elif hills_around[1] == -1 and hills_around[3] == -1 and hills_around[5] == 0 and hills_around[7] == -1: return 15
        elif hills_around[1] == 0 and hills_around[3] == -1 and hills_around[5] == -1 and hills_around[7] == -1: return 15
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

    hill_edge_textures = dict()
    for y in range(0, map_size_y):
        for x in range(0, map_size_x):
            hill_edge_texture = str(define_hill_edge_texture(tile_heights, x, y))
            if not hill_edge_texture == "-1": hill_edge_textures[(x, y)] = "m_" + hill_edge_texture
    return hill_edge_textures


def generate_height_map(map_size_x, map_size_y, height_map):
    tile_heights = dict()
    for y in range(0, map_size_y):
        for x in range(0, map_size_x):
            height_map[(x, y)] = "height_" + str(tile_heights[(x, y)])
    return height_map

# tile_Heights = [] image_grayscale_to_dict("world_height_map_downscaled2.jpg")
