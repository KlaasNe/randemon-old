from noise import snoise2
import random


# Checks if enough space is available to plant a tree
# No trees above the highest path height
# Adds an overlay to decoration_layer if the top of the tree overlaps with another tree
def create_trees(pmap, spawn_rate, x_offset, y_offset):

    def mergeable(x, y):
        if (x, y - 1) not in pmap.ground_layer.keys() and (x + 1, y - 1) not in pmap.ground_layer.keys():
            if pmap.get_tile("ground_layer", x, y) == ("na", 2, 2) and pmap.get_tile("ground_layer", x + 1, y) == ("na", 2, 2):
                if pmap.get_tile("secondary_ground", x, y - 1) == ("na", 2, 1) and pmap.get_tile("secondary_ground", x + 1, y - 1) == ("na", 2, 1):
                    return True
        return False

    octaves = 2
    freq = 40
    for y in range(pmap.height):
        for x in range(pmap.width):
            if pmap.tile_heights.get((x, y), -1) <= pmap.highest_path:
                if (x, y) not in pmap.ground_layer.keys() and (x, y) not in pmap.secondary_ground.keys() and (x, y - 1) not in pmap.secondary_ground.keys() and (x, y) not in pmap.buildings.keys() and (x, y) not in pmap.decoration_layer.keys() and (x, y - 1) not in pmap.decoration_layer.keys():
                    if abs(snoise2((x + x_offset) / freq, (y + y_offset) / freq, octaves)) > 1 - (spawn_rate / 100) and random.random() > 0.5:
                        pmap.decoration_layer[(x, y - 2)] = ("na", 2, 0)
                        pmap.secondary_ground[(x, y - 1)] = ("na", 2, 1)
                        pmap.ground_layer[(x, y)] = ("na", 2, 2)

    for y in range(pmap.height):
        for x in range(pmap.width):
            if mergeable(x, y):
                pmap.decoration_layer[(x, y - 2)] = ("na", 1, 5)
                pmap.decoration_layer[(x + 1, y - 2)] = ("na", 2, 5)
                pmap.secondary_ground[(x, y - 1)] = ("na", 1, 6)
                pmap.secondary_ground[(x + 1, y - 1)] = ("na", 2, 6)
                pmap.ground_layer[(x, y)] = ("na", 1, 7)
                pmap.ground_layer[(x + 1, y)] = ("na", 2, 7)


# The whole map is filled with random green tiles
# Tall gras and flowers are spawned with a perlin noise field
def grow_grass(pmap, tall_grass_coverage, x_offset, y_offset):
    def random_grass(gx, gy):
        octaves = 2
        freq = 20
        sne_probability = abs(snoise2((gx + x_offset) / freq, (gy + y_offset) / freq, octaves))
        if pmap.tile_heights.get((gx, gy), -1) <= pmap.highest_path:
            if sne_probability < 1 - (tall_grass_coverage / 100) or "l_1" in pmap.decoration_layer.get((gx, gy), "") or "l_5" in pmap.decoration_layer.get((gx, gy), "") or (x, y - 1) in pmap.buildings.keys() or (x, y) in pmap.secondary_ground.keys():
                grass_type = random.randint(0, 7)
                return "na", 0, grass_type
            else:
                sne_type = random.randint(0, 1)
                # Turn 80 percent of the flowers into tall grass
                if sne_type == 1 and random.random() < 0.8: return "na", 1, 0
                # Turn 0.5 percent of the tall grass into tall grass with a hidden item
                if sne_type == 0 and random.random() < 0.005: return "na", 1, 4
                return "na", 1, sne_type
        else:
            return "hi", 0, 0

    for y in range(pmap.height):
        for x in range(pmap.width):
            if (x, y) not in pmap.ground_layer.keys():
                pmap.grass_layer[(x, y)] = random_grass(x, y)


# Creates an overlay for the entire map showing rain
# The amount of rain is given with rain_rate
def create_rain(pmap, odds,  rain_rate):
    if random.random() < odds:
        for y in range(pmap.height):
            for x in range(pmap.width):
                if random.random() < rain_rate:
                    if random.random() < 0.5 and "fe" != pmap.get_tile_type("secondary_ground", x, y) and "hi" != pmap.get_tile_type("ground_layer", x, y) and (x, y) not in pmap.npc_layer.keys():
                        pmap.rain[(x, y)] = ("ra", random.randint(0, 2), 1)
                    else:
                        pmap.rain[(x, y)] = ("ra", random.randint(1, 2), 0)
                else:
                    pmap.rain[(x, y)] = ("ra", 0, 0)
