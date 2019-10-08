import datetime, pygame, os, random, math, sys, ctypes
from noise import snoise2
from time import sleep
from worldMap import image_grayscale_to_dict
from heightMapGenerator import create_hill_map, create_hill_edges
from waterGenerator import create_rivers, create_beach
from buildingGenerator import spawn_house
from pathGenerator import apply_path_sprites


def is_taken(layer, x, y):
    return (x, y) in layer.keys()


def out_of_bounds(x, y):
    return x < 0 or y < 0 or x >= map_Size_X or y >= map_Size_Y


def create_rain(layer, rain_rate):
    for y in range(0, map_Size_Y):
        for x in range(0, map_Size_X):
            if random.randint(0, 100) < rain_rate:
                layer[(x, y)] = "r_" + str(random.randint(1, 2))
            elif (x, y) not in layer.keys():
                layer[(x, y)] = "r_0"
    for y in range(0, map_Size_Y):
        for x in range(0, map_Size_X):
            if random.randint(0, 100) < rain_rate:
                if "sne_" not in ground_Layer.get((x, y), ""):
                    layer[(x, y)] = "r_" + str(random.randint(3, 5))


def render(layer, grass_fill):

    def random_grass(decoration_rate, offset_x, offset_y):

        def choose_sne_type(excluded_sne):
            sne_type = random.randint(0, NB_SNE)
            while sne_type in excluded_sne:
                sne_type = random.randint(0, NB_SNE)

            # Turn 80 percent of the flowers into tall grass
            if sne_type == 2 and random.random() < 0.8: sne_type = 0
            # Turn 0.5 percent of the tall grass into tall grass with a hidden item
            if sne_type == 0 and random.random() < 0.005: sne_type = "0_p"

            return "sne_" + str(sne_type)

        octaves = 1
        freq = 7
        sne_probability = snoise2((x + offset_x) / freq, (y + offset_y) / freq, octaves) + 0.5

        if sne_probability > (decoration_rate / 100):
            grass_type = random.randint(0, 3)
            return "g_" + str(grass_type)
        else:
            return choose_sne_type(excludedSne)

    def try_blit_tile(tile):
        try:
            screen.blit(get_tile_file(tile), (x * TILE_SIZE, y * TILE_SIZE - correction))
        except Exception as e:
            screen.blit(get_tile_file("missing"), (x * TILE_SIZE, y * TILE_SIZE - correction))
            print(e)

    def get_tile_file(tile):
        return pygame.image.load(os.path.join("resources", tile + ".png"))

    for y in range(0, map_Size_Y):
        for x in range(0, map_Size_X):
            if (x, y) in layer.keys():
                current_tile = str(layer[(x, y)])
                if "npc_" in layer[(x, y)]:
                    correction = 3  # npc's are slightly larger than a tile
                else:
                    correction = 0
                try_blit_tile(current_tile)
            elif grass_fill:
                screen.blit(get_tile_file(random_grass(sne_decoration_rate, x_offset, y_offset)), (x * TILE_SIZE, y * TILE_SIZE))

    pygame.display.update()


seed = random.randint(0, sys.maxsize)
random.seed(seed)

TILE_SIZE = 16  # Length of 1 tile in pixels
NB_SNE = 4  # The amount of different existing small nature elements

sne_decoration_rate = 50  # The percentage of land covered by small nature elements
excludedSne = [1, 3, 4]  # Small nature elements to keep from te map

map_Size_X = 50  # The horizontal amount of tiles the map consists of
map_Size_Y = 50  # The vertical amount of tiles the map consists of
screen_Size_X = TILE_SIZE * map_Size_X
screen_Size_Y = TILE_SIZE * map_Size_Y
x_offset = random.randint(0, 1000000)
y_offset = random.randint(0, 1000000)

screen = pygame.display.set_mode((screen_Size_X, screen_Size_Y))

rain = dict()
buildings = dict()
hill_map = create_hill_map(map_Size_X, map_Size_Y, 4)
ground_Layer = create_hill_edges(map_Size_X, map_Size_Y, hill_map)
create_rivers(ground_Layer, map_Size_X, map_Size_Y, hill_map)
create_beach(ground_Layer, map_Size_X, map_Size_Y, hill_map)
for house_number in range(10):
    spawn_house(buildings, ground_Layer, map_Size_X, map_Size_Y, house_number, hill_map)
apply_path_sprites(ground_Layer, map_Size_X, map_Size_Y)

render(ground_Layer, True)
render(buildings, False)
# create_rain(rain, 0)
# render(rain, False)
sleep(5)
quit()
