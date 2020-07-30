import math

from noise import snoise2


# Creates rivers for pmap
def create_rivers(pmap):
    # Chooses the right name for water tiles (pd_*)
    def apply_water_sprites():

        # Given which tiles around coordinates (x, y) are water and which land, choses the right sprite
        def calculate_water_sprite(x, y):

            tiles_around = []
            for around in range(0, 9):
                path_around = pmap.get_tile_type("ground_layer", x + (around % 3) - 1, y + math.floor(around / 3) - 1)
                if "pa" not in path_around and "wa" in path_around \
                        or pmap.out_of_bounds(x + (around % 3) - 1, y + math.floor(around / 3) - 1):
                    tiles_around.append(1)
                else:
                    tiles_around.append(0)

            if tiles_around[0] == 0 and tiles_around[1:9] == 8 * [1]:
                return "wa", 2, 2
            elif tiles_around[2] == 0 and tiles_around[0:2] + tiles_around[3:9] == 8 * [1]:
                return "wa", 1, 2
            elif tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1:
                return "wa", 0, 0
            elif tiles_around[1] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1:
                return "wa", 1, 0
            elif tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1:
                return "wa", 4, 0
            elif tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[7] == 1:
                return "wa", 2, 0
            elif tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1:
                return "wa", 3, 0
            elif tiles_around[5] == 1 and tiles_around[7] == 1:
                return "wa", 3, 1
            elif tiles_around[1] == 1 and tiles_around[5] == 1:
                return "wa", 1, 1
            elif tiles_around[1] == 1 and tiles_around[3] == 1:
                return "wa", 2, 1
            elif tiles_around[3] == 1 and tiles_around[7] == 1:
                return "wa", 4, 1
            return "wa", 0, 0

        for x, y in pmap.ground_layer.keys():
            if "wa" == pmap.get_tile_type("ground_layer", x, y) or "ro" == pmap.ground_layer.get((x, y), ""):
                pmap.ground_layer[(x, y)] = calculate_water_sprite(x, y)

    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            if pmap.tile_heights[(x, y)] == 0:
                pmap.ground_layer[(x, y)] = ("wa", 0, 0)

    apply_water_sprites()


# Creates sandy path around rivers; inside a perlin noise field
def create_beach(pmap, x_offset, y_offset):
    def check_for_water_around(x, y, beach_width):
        for around in range(0, (beach_width + 2) ** 2):
            check_x = x + around % (beach_width + 2) - beach_width + 1
            check_y = y + around // (beach_width + 2) - beach_width + 1
            if pmap.get_tile_type("ground_layer", check_x, check_y) == "wa":
                return True
        return False

    octaves = 1
    freq = 100
    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            beach = snoise2((x + x_offset) / freq, (y + y_offset) / freq, octaves) + 0.5 > 0.5
            if beach and ((x, y) not in pmap.ground_layer.keys()
                          and pmap.tile_heights.get((x, y), 0) == 1
                          and check_for_water_around(x, y, 4)):
                pmap.ground_layer[(x, y)] = ("pa", 0, 9)
