import datetime, pygame, os, random, sys, ctypes, time, getopt
# from worldMap import image_grayscale_to_dict
from heightMapGenerator import create_hills, create_hill_edges, generate_height_map
from waterGenerator import create_rivers, create_beach
from buildingGenerator import spawn_house, add_random_ends
from pathGenerator import apply_path_sprites, generate_dijkstra_path, create_lanterns
from plantGenerator import create_trees, grow_grass, create_rain
from pokemonGenerator import spawn_pokemon
from npcGenerator import spawn_npc
from decorationGenerator import spawn_truck, spawn_rocks
from threading import Thread


def render(layer):
    for tile_x, tile_y in layer.keys():
        current_tile = layer[(tile_x, tile_y)]
        correction = 6 if "npc_" in current_tile else 0  # npc's are slightly larger than a tile
        try_blit_tile(current_tile, tile_x, tile_y, correction)
    pygame.display.update()


def try_blit_tile(tile, blx, bly, correction=0):
    try:
        if tile in Map.default_buffer_tiles:
            if "g_" in tile or "sne_" in tile or "st_" in tile:
                screen.blit(Map.grass_tile_buffer[tile], (blx * Map.TILE_SIZE, bly * Map.TILE_SIZE - correction))
            elif "pd_" in tile:
                screen.blit(Map.water_tile_buffer[tile], (blx * Map.TILE_SIZE, bly * Map.TILE_SIZE - correction))
            elif "p_" in tile:
                screen.blit(Map.path_tile_buffer[tile], (blx * Map.TILE_SIZE, bly * Map.TILE_SIZE - correction))
            elif "r_" in tile:
                screen.blit(Map.rain_tile_buffer[tile], (blx * Map.TILE_SIZE, bly * Map.TILE_SIZE - correction))
            else:
                print("missing buffer tile " + tile)
        else:
            screen.blit(get_tile_file(tile), (blx * Map.TILE_SIZE, bly * Map.TILE_SIZE - correction))
    except Exception as e:
        screen.blit(get_tile_file("missing"), (blx * Map.TILE_SIZE, bly * Map.TILE_SIZE - correction))
        print(e)


def get_tile_file(tile):
    return pygame.image.load(os.path.join("resources", tile + ".png"))


class Map:

    TILE_SIZE = 16  # Length of 1 tile in pixels
    NB_SNE = 4  # The amount of different existing small nature elements
    EXCLUDED_SNE = [1, 3, 4]  # Small nature elements to keep out of the map

    # Tiles which are often used (faster rendering)
    default_buffer_tiles = ["g_0", "g_1", "g_2", "g_3", "sne_0", "sne_2", "pd_0", "st_0", "st_1", "st_2", "st_2_d", "r_0", "r_1", "r_2", "r_3", "r_4", "r_5", "p_4_0", "p_4_1", "p_4_2", "p_4_3", "p_4_4"]
    grass_tile_buffer = {}
    water_tile_buffer = {}
    path_tile_buffer = {}
    rain_tile_buffer = {}

    def __init__(self, width, height, max_hill_height, tall_grass_coverage, tree_coverage, rain_rate, seed=random.randint(0, sys.maxsize)):
        self.seed = seed
        self.width = width
        self.height = height
        self.max_hill_height = max_hill_height
        self.tall_grass_coverage = tall_grass_coverage
        self.tree_coverage = tree_coverage
        self.rain_rate = rain_rate

        self.raining = False
        self.front_doors = []
        self.end_points = []
        self.tile_heights = dict()
        self.ground_layer = dict()
        self.buildings = dict()
        self.rain = dict()
        self.decoration_layer = dict()
        self.npc_layer = dict()
        self.height_map = dict()
        self.grass_layer = dict()

        random.seed(seed)

    @staticmethod
    def setup_default_tile_buffer(tiles):
        for tile in tiles:
            if "g_" in tile or "sne_" in tile or "st_" in tile:
                Map.grass_tile_buffer[tile] = get_tile_file(tile)
            elif "pd_" in tile:
                Map.water_tile_buffer[tile] = get_tile_file(tile)
            elif "p_" in tile:
                Map.path_tile_buffer[tile] = get_tile_file(tile)
            elif "r_" in tile:
                Map.rain_tile_buffer[tile] = get_tile_file(tile)

    @staticmethod
    def has_tile_at_position(layer, x, y):
        return (x, y) in layer.keys()

    def out_of_bounds(self, x, y):
        return x < 0 or y < 0 or x >= self.width or y >= self.height


# get command line options
width_opt = None
height_opt = None
try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['width=', 'height='])
    for opt,arg in opts:
        if opt == "--width":
            width_opt = int(arg)
        if opt == "--height":
            height_opt = int(arg)
except getopt.GetoptError as err:
    print(err)


Map.setup_default_tile_buffer(Map.default_buffer_tiles)

# full hd -> 120,68; my phone -> 68,147
map_size_x = width_opt or 50  # The horizontal amount of tiles the map consists of
map_size_y = height_opt or 50  # The vertical amount of tiles the map consists of
all_pokemon = False
random_map = Map(map_size_x, map_size_y, 5, 40, 20, 20)
screen_Size_X = Map.TILE_SIZE * map_size_x
screen_Size_Y = Map.TILE_SIZE * map_size_y
x_offset = random.randint(0, 1000000)
y_offset = random.randint(0, 1000000)


os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.display.init()
screen = pygame.display.set_mode((screen_Size_X, screen_Size_Y))

to_time = time.time()
print("*creating landscape*")
create_hills(random_map)
create_rivers(random_map)
create_beach(random_map)
add_random_ends(random_map, "p_1")
create_hill_edges(random_map)
print("*builing houses*")
spawn_house(random_map, "pc", "p_1")
spawn_house(random_map, "pm", "p_1")
for house_type in range(1, 10):
    for x in range(1):
        spawn_house(random_map, house_type, "p_1")
# for house in range(100):
#     spawn_house(random_map, random.randint(1, 9), "p_1")
random.shuffle(random_map.front_doors)
random_map.front_doors += random_map.end_points
print("*dijkstra*")
generate_dijkstra_path(random_map, "p_1")
apply_path_sprites(random_map)

create_hill_edges(random_map, True)
create_lanterns(random_map)
print("*growing trees*")
create_trees(random_map, 30, x_offset, y_offset)
print("*spawning pokemon*")
all_pokemon = spawn_pokemon(random_map)
print("*spawning npc*")
spawn_npc(random_map, 1)
print("*spawning decorations")
spawn_truck(random_map, 0.05)
spawn_rocks(random_map, 0.01)
print("*growing grass*")
grow_grass(random_map, random_map.tall_grass_coverage, x_offset, y_offset)
print("*checking the weather forecast*")
create_rain(random_map, 10)

print("*rendering*")
render(random_map.grass_layer)
render(random_map.ground_layer)
render(random_map.buildings)
render(random_map.npc_layer)
render(random_map.decoration_layer)
render(random_map.rain)
print(random_map.buildings)
# generate_height_map(random_map)
# random_map.render(random_map.height_map)
print("time = " + str(time.time() - to_time) + "seconds")

print("Seed: " + str(random_map.seed))

def prompt():
    save = input("Save this image? (y/n/w): ")
    t = datetime.datetime.now().strftime("%G-%m-%d %H-%M-%S")
    if save == "y" or save == "w":
        if not os.path.isdir("saved images"):
            os.mkdir("saved images")
        pygame.image.save(screen, os.path.join("saved images", t + ".png"))
        cwd = os.getcwd()
        if save == "w": ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(cwd, "saved images", t + ".png"), 0)

t = Thread(target=prompt)
t.daemon = True
t.start()

# let pygame run in background
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

quit()
