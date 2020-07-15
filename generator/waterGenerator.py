import math
from noise import snoise2


# Creates rivers for pmap
def create_rivers(pmap):

    # Chooses the right name for water tiles (pd_*)
    def apply_water_sprites(layer):

        # Given which tiles around coordinates (x, y) are water and which land, choses the right sprite
        def calculate_water_sprite(x, y):

            tiles_around = []
            for around in range(0, 9):
                path_around = (layer.get((x + (around % 3) - 1, y + math.floor(around / 3) - 1), "0"))
                if "p_" not in str(path_around) and (
                        "pd_" in str(path_around) or "b_" in str(path_around) or "pl_" in str(
                        path_around) or pmap.out_of_bounds(x + (around % 3) - 1, y + math.floor(around / 3) - 1)):
                    tiles_around.append(1)
                else:
                    tiles_around.append(0)

            if tiles_around[0] == 0 and tiles_around[1:9] == 8 * [1]:
                return "16"
            elif tiles_around[2] == 0 and tiles_around[0:2] + tiles_around[3:9] == 8 * [1]:
                return "17"
            elif tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1:
                return "0"
            elif tiles_around[1] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1:
                return "1"
            elif tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1:
                return "2"
            elif tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[7] == 1:
                return "3"
            elif tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1:
                return "4"
            elif tiles_around[5] == 1 and tiles_around[7] == 1:
                return "5"
            elif tiles_around[1] == 1 and tiles_around[5] == 1:
                return "6"
            elif tiles_around[1] == 1 and tiles_around[3] == 1:
                return "7"
            elif tiles_around[3] == 1 and tiles_around[7] == 1:
                return "8"
            elif tiles_around[3] == 1 and tiles_around[5] == 1:
                return "13"
            elif tiles_around[1] == 1 and tiles_around[7] == 1:
                return "14"
            elif tiles_around[1] == 1:
                return "9"
            elif tiles_around[3] == 1:
                return "10"
            elif tiles_around[5] == 1:
                return "12"
            elif tiles_around[7] == 1:
                return "11"
            return "15"

        for (x, y) in layer:
            if "pd_" in layer.get((x, y), "") or "b_" in layer.get((x, y), ""):
                water_sprite = calculate_water_sprite(x, y)
                if 0 < int(water_sprite) <= 8 or int(water_sprite) == 16 or int(water_sprite) == 17:
                    water_sprite += "_d"
                layer[(x, y)] = "pd_" + str(water_sprite)

    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            tile_height = pmap.tile_heights[(x, y)]
            if tile_height == 0:
                pmap.ground_layer[(x, y)] = "pd_"

    apply_water_sprites(pmap.ground_layer)


# Creates sandy path around rivers; inside a perlin noise field
def create_beach(pmap, x_offset, y_offset):

    def check_for_water_around(x, y, beach_width):
        for around in range(0, (beach_width + 2) ** 2):
            check_x = x + around % (beach_width + 2) - beach_width + 1
            check_y = y + around // (beach_width + 2) - beach_width + 1
            water_around = pmap.ground_layer.get((check_x, check_y), "")
            if "pd_" in str(water_around):
                return True
        return False

    octaves = 2
    freq = 150
    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            beach = snoise2((x + x_offset) / freq, (y + y_offset) / freq, octaves) + 0.5 > 0.5
            if beach and ((x, y) not in pmap.ground_layer.keys() and pmap.tile_heights.get((x, y), 0) == 1 and check_for_water_around(x, y, 4)): pmap.ground_layer[(x, y)] = "p_4"
