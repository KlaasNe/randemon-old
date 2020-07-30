from math import floor

from noise import snoise2


# Creates a perlin noise field to be used as height map with ints as height ranging from 0 to pmap.max_hill_height
def create_hills(pmap, x_offset, y_offset):
    octaves = 2
    freq = 80
    off_x = x_offset
    off_y = y_offset
    max_height = pmap.max_hill_height
    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            noise = snoise2((x // 4 + off_x) / freq, (y // 4 + off_y) / freq, octaves)
            pmap.tile_heights[(x, y)] = abs(floor(noise * max_height))


# Calculates where to draw edges of hills
def create_hill_edges(pmap, hill_type=0, update=False):
    # Determines which sprite to use at (x, y)
    def define_hill_edge_texture(x, y):

        # Looks for the tile heights around (x, y) and adds their relative height to an array. 1 means the tile is
        # situated higher than the central tile, 0 means equal height, -1 means lower
        def get_hills_around_tile():
            current_tile_height = pmap.tile_heights[(x, y)]
            hills_around_tile = []
            for around in range(0, 9):
                tile_coordinate = (x + around % 3 - 1, y + around // 3 - 1)
                curr_height = pmap.tile_heights.get(tile_coordinate, current_tile_height)
                if curr_height > current_tile_height:
                    hills_around_tile.append(1)
                elif curr_height < current_tile_height:
                    hills_around_tile.append(-1)
                elif curr_height == current_tile_height:
                    hills_around_tile.append(0)
            return hills_around_tile

        # using the array of relative heights, this calculates the sprite for the hill texture
        hills_around = get_hills_around_tile()
        if pmap.tile_heights.get((x, y), 0) < 2: return -1
        if hills_around[3] == 0 and hills_around[6] == -1 and hills_around[7] == 0:
            return "hi", 0 + (5 * hill_type), 1
        if hills_around[5] == 0 and hills_around[7] == 0 and hills_around[8] == -1:
            return "hi", 0 + (5 * hill_type), 2
        if hills_around[0] == -1 and hills_around[1] == 0 and hills_around[3] == 0:
            return "hi", 3 + (5 * hill_type), 0
        if hills_around[1] == 0 and hills_around[2] == -1 and hills_around[5] == 0:
            return "hi", 3 + (5 * hill_type), 0
        if hills_around[1] == 0 and hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == 0:
            return -1
        if hills_around[1] == 0 and hills_around[3] == -1 and hills_around[7] == 0:
            return "hi", 1 + (5 * hill_type), 0
        if hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == -1:
            return "hi", 4 + (5 * hill_type), 0
        if hills_around[1] == 0 and hills_around[5] == -1 and hills_around[7] == 0:
            return "hi", 2 + (5 * hill_type), 0
        if hills_around[1] == -1 and hills_around[3] == 0 and hills_around[5] == 0:
            return "hi", 3 + (5 * hill_type), 0
        if hills_around[1] == -1 and hills_around[3] == -1:
            return "hi", 1 + (5 * hill_type), 1
        if hills_around[3] == -1 and hills_around[7] == -1:
            return "hi", 3 + (5 * hill_type), 1
        if hills_around[5] == -1 and hills_around[7] == -1:
            return "hi", 4 + (5 * hill_type), 1
        if hills_around[1] == -1 and hills_around[5] == -1:
            return "hi", 2 + (5 * hill_type), 1
        return -1

    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            hill_edge_texture = define_hill_edge_texture(x, y)
            if hill_edge_texture != -1:
                if hill_edge_texture == ("hi", 3, 0) and pmap.tile_heights.get((x, y), -1) == pmap.highest_path + 1:
                    hill_edge_texture = ("hi", 0, 3)
                elif update and hill_edge_texture[1] in [1, 2, 3] \
                        and pmap.tile_heights.get((x, y), -1) > pmap.highest_path + 1:
                    hill_edge_texture = ("hi", hill_edge_texture[1], hill_edge_texture[2] + 2)

                if "ro" != pmap.get_tile_type("ground_layer", x, y) or pmap.get_tile("ground_layer", x, y)[1] < 2:
                    if update:
                        pmap.ground_layer[(x, y)] = hill_edge_texture
                    elif (x, y) not in pmap.ground_layer.keys():
                        pmap.ground_layer[(x, y)] = hill_edge_texture
            elif hill_edge_texture == -1 and "hi" == pmap.get_tile_type("ground_layer", x, y):
                pmap.ground_layer.pop((x, y))


# Creates a visual height map which can be rendered
# It's a feature for debugging (pls dont set max height over 15 when using this)
def generate_height_map(pmap):
    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            pmap.height_map[(x, y)] = "height_" + str(pmap.tile_heights[(x, y)])

# tile_Heights = [] image_grayscale_to_dict("world_height_map_downscaled2.jpg")
