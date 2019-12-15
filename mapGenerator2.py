import datetime, pygame, os, random, math, sys, ctypes
from noise import snoise2
# from time import sleep
# from worldMap import image_grayscale_to_dict
from heightMapGenerator import create_hills, create_hill_edges
from waterGenerator import create_rivers, create_beach
from buildingGenerator import spawn_house
from pathGenerator import apply_path_sprites, generate_dijkstra_path, create_stairs
from plantGenerator import create_trees


class Map:

    TILE_SIZE = 16  # Length of 1 tile in pixels
    NB_SNE = 4  # The amount of different existing small nature elements
    EXCLUDED_SNE = [1, 3, 4]  # Small nature elements to keep from te map

    def __init__(self, width, height, max_hill_height, tall_grass_coverage, tree_coverage, rain_rate, seed):
        self.seed = seed
        self.width = width
        self.height = height
        self.max_hill_height = max_hill_height
        self.tall_grass_coverage = tall_grass_coverage
        self.tree_coverage = tree_coverage
        self.rain_rate = rain_rate

        self.front_doors = []
        self.tile_heights = dict()
        self.ground_layer = dict()
        self.buildings = dict()
        self.rain = dict()
        self.decoration_layer = dict()

        random.seed(seed)

    @staticmethod
    def has_tile_at_position(layer, x, y):
        return (x, y) in layer.keys()

    def out_of_bounds(self, x, y):
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def create_rain(self):
        for y in range(0, map_size_y):
            for x in range(0, map_size_x):
                if random.randint(0, 100) < self.rain_rate:
                    self.rain[(x, y)] = "r_" + str(random.randint(1, 2))
                elif (x, y) not in self.rain.keys():
                    self.rain[(x, y)] = "r_0"
        for y in range(0, map_size_y):
            for x in range(0, map_size_x):
                if random.randint(0, 100) < self.rain_rate:
                    if "sne_" not in self.ground_layer.get((x, y), ""):
                        self.rain[(x, y)] = "r_" + str(random.randint(3, 5))

    def render(self, layer):

        def random_grass(offset_x, offset_y):

            def choose_sne_type(excluded_sne):
                sne_type = random.randint(0, self.NB_SNE)
                while sne_type in excluded_sne:
                    sne_type = random.randint(0, self.NB_SNE)

                # Turn 80 percent of the flowers into tall grass
                if sne_type == 2 and random.random() < 0.8: sne_type = 0
                # Turn 0.5 percent of the tall grass into tall grass with a hidden item
                if sne_type == 0 and random.random() < 0.005: sne_type = "0_p"

                return "sne_" + str(sne_type)

            octaves = 1
            freq = 7
            sne_probability = snoise2((x + offset_x) / freq, (y + offset_y) / freq, octaves) + 0.5

            if sne_probability > (self.tall_grass_coverage / 100):
                grass_type = random.randint(0, 3)
                return "g_" + str(grass_type)
            else:
                return choose_sne_type(self.EXCLUDED_SNE)

        def try_blit_tile(tile):
            try:
                screen.blit(get_tile_file(tile), (x * self.TILE_SIZE, y * self.TILE_SIZE - correction))
            except Exception as e:
                screen.blit(get_tile_file("missing"), (x * self.TILE_SIZE, y * self.TILE_SIZE - correction))
                print(e)

        def get_tile_file(tile):
            return pygame.image.load(os.path.join("resources", tile + ".png"))

        for y in range(0, map_size_y):
            for x in range(0, map_size_x):
                if (x, y) in layer.keys():
                    current_tile = str(layer[(x, y)])
                    if "npc_" in layer[(x, y)]:
                        correction = 3  # npc's are slightly larger than a tile
                    else:
                        correction = 0
                    try_blit_tile(current_tile)
                elif layer == self.ground_layer:
                    screen.blit(get_tile_file(random_grass(x_offset, y_offset)), (x * self.TILE_SIZE, y * self.TILE_SIZE))

        pygame.display.update()


map_size_x = math.ceil(50)  # The horizontal amount of tiles the map consists of
map_size_y = math.ceil(50)  # The vertical amount of tiles the map consists of
random_map = Map(map_size_x, map_size_y, 4, 50, 20, 20, random.randint(0, sys.maxsize))
#random.randint(0, sys.maxsize)
screen_Size_X = Map.TILE_SIZE * map_size_x
screen_Size_Y = Map.TILE_SIZE * map_size_y
x_offset = random.randint(0, 1000000)
y_offset = random.randint(0, 1000000)

screen = pygame.display.set_mode((screen_Size_X, screen_Size_Y))

print("*creating landscape*")
create_hills(random_map)
create_rivers(random_map)
create_beach(random_map)
print("*builing houses*")
for house_type in range(1, 10):
    for x in range(1):
        spawn_house(random_map, house_type, "p_3")
print("*dijkstra*")
generate_dijkstra_path(random_map, "p_1")
apply_path_sprites(random_map)

create_hill_edges(random_map)
print("*growing trees*")
create_trees(random_map, 30, x_offset, y_offset)
print("*rendering*")
random_map.render(random_map.ground_layer)
random_map.render(random_map.buildings)
random_map.render(random_map.decoration_layer)
# render(buildings, False)
# create_rain(rain, 0)
# render(rain, False)
print("Seed: " + str(random_map.seed))

save = input("Save this image? (y/n/w): ")

t = datetime.datetime.now().strftime("%G-%m-%d %H-%M-%S")
if save == "y" or save == "w":
    pygame.image.save(screen, os.path.join("saved images", t + ".png"))
    cwd = os.getcwd()
    if save == "w": ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(cwd, "saved images", t + ".png"), 0)

quit()
