from math import floor

from noise import snoise2


# Creates a perlin noise field to be used as height map with ints as height ranging from 0 to pmap.max_hill_height
def generate_height_map(size, max_height, off_x, off_y):
    sx, sy = size
    height_map = dict()
    octaves = 2
    freq = 80
    for y in range(0, sy):
        for x in range(0, sx):
            noise = snoise2((x // 4 + off_x) / freq, (y // 4 + off_y) / freq, octaves)
            height_map[(x, y)] = abs(floor(noise * max_height + 1))
    return height_map

# Creates a visual height map which can be rendered
# It's a feature for debugging (pls don't set max height over 15 when using this)
def generate_visual_height_map(pmap):
    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            pmap.height_map[(x, y)] = "height_" + str(pmap.tile_heights[(x, y)])
