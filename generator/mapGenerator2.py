import ctypes
import datetime
import json
import os
import random
import time
from os import path
from threading import Thread

from PIL import Image

import utilities.parser as inputs
import image.spriteSheetManager as ssm
from generators import *
from Layers import *
from image.render import render2, render_npc


def tupleToArray(tup):
    return [x for x in tup]


def dictToObject(dic, value_convert=True):
    obj = {}
    for key, val in dic.items():
        if not key[0] in obj:
            obj[key[0]] = {}
        val2 = tupleToArray(val) if value_convert else val
        obj[int(key[0])][int(key[1])] = val2
    return obj


class Map:
    TILE_SIZE = 16  # Side of a tile in pixels

    def __init__(self, width, height, max_hill_height, tall_grass_coverage, tree_coverage, rain_rate):
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
        size = (self.width, self.height)
        self.ground = Layer("ground", size)
        self.ground2 = Layer("ground2", size)
        self.buildings = Layer("buildings", size)
        self.rain = Layer("rain", size)
        self.decoration = Layer("decoration", size)
        self.npc = Layer("npc", size)
        self.hills = Layer("hills", size)
        self.plants = Layer("plants", size)

        self.highest_path = 0

    def out_of_bounds(self, x, y):
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def get_tile(self, layer, x, y, default=""):
        try:
            return getattr(self, layer)[(x, y)]
        except KeyError:
            return default
        except AttributeError as a:
            print(a)

    def get_tile_type(self, layer, x, y, default=""):
        try:
            return self.get_tile(layer, x, y, default)[0]
        except IndexError:
            return default

    def toJSON(self):
        resp = {
            'buildings': dictToObject(self.buildings),
            'ground_layer': dictToObject(self.ground),
            'secondary_ground': dictToObject(self.ground2),
            'rain': dictToObject(self.rain),
            'decoration_layer': dictToObject(self.decoration),
            'npc_layer': dictToObject(self.npc),
            'height_map': dictToObject(self.height_map),
            'grass_layer': dictToObject(self.grass_layer),
            'tile_heights': dictToObject(self.tile_heights, False)
        }
        return json.dumps(resp, sort_keys=True, indent=2, separators=(',', ': '))


# Here starts the main program

# get command line options
parser = inputs.make_parser()
args = parser.parse_args()

if not args.credits_opt:


    random.seed(args.seed_opt)
    x_maps, y_maps = args.x_split, args.y_split
    map_size_x, map_size_y = args.map_size_x * x_maps, args.map_size_y * y_maps
    screen_Size_X, screen_Size_Y = Map.TILE_SIZE * map_size_x, Map.TILE_SIZE * map_size_y
    x_offset, y_offset = random.randint(0, 1000000), random.randint(0, 1000000)

    random_map = Map(map_size_x, map_size_y, args.max_hill_height, args.tall_grass_coverage, args.tree_coverage, 0.2)

    if args.headless_opt: os.environ["SDL_VIDEODRIVER"] = "dummy"

    visual = ssm.DrawSheet(screen_Size_X, screen_Size_Y)

    to_time = time.time()
    print("*creating landscape*")
    create_hills(random_map, x_offset, y_offset)
    create_rivers(random_map.ground, random_map.tile_heights)
    create_beach(random_map.ground, random_map.tile_heights, x_offset, y_offset)
    add_random_ends(random_map, ("pa", 0, 0))
    create_hill_edges(random_map)
    house = time.time()
    spawn_house(random_map, "pokecenter", ("pa", 0, 0))
    spawn_house(random_map, "pokemart", ("pa", 0, 0))
    spawn_house(random_map, "gym", ("pa", 0, 0))
    spawn_house(random_map, "powerplant", ("pa", 0, 0))
    for x in range(1):
        for house_type in range(22):
            spawn_house(random_map, house_type, ("pa", 0, 0))
    random.shuffle(random_map.front_doors)
    random_map.front_doors += random_map.end_points
    generate_dijkstra_path(random_map, ("pa", 0, 0))
    apply_path_sprites(random_map)

    create_hill_edges(random_map, update=True)
    create_trees(random_map, random_map.tree_coverage, x_offset, y_offset)
    all_pokemon = spawn_pokemons(random_map)
    spawn_npc(random_map, 1)
    create_lanterns(random_map)
    spawn_truck(random_map, 0.05)
    spawn_rocks(random_map, 0.01)
    spawn_balloon(random_map)
    grow_grass(random_map, random_map.tall_grass_coverage, x_offset, y_offset)
    create_rain(random_map, 0.1, random_map.rain_rate)

    print("*rendering*")
    render2(random_map, "grass_layer", visual.drawable())
    render2(random_map, "ground_layer", visual.drawable())
    render2(random_map, "secondary_ground", visual.drawable())
    render2(random_map, "buildings", visual.drawable())
    render_npc(random_map, "npc_layer", visual.drawable())
    render2(random_map, "decoration_layer", visual.drawable())
    render2(random_map, "rain", visual.drawable())
    print("time = " + str(time.time() - to_time) + " seconds")
    print("Seed: " + str(args.seed_opt))


    def prompt():
        if args.save_opt:
            save = "y"
        else:
            save = input("Save this image? (y/n/w): ")
        file_n = datetime.datetime.now().strftime("%G-%m-%d %H-%M-%S")
        if args.export_opt:
            json_string = random_map.toJSON()
            file_n = open(path.join("saved images", file_n + ".json"), "w")
            file_n.write(json_string)
            file_n.close()
        if save == "y" or save == "w":
            if not os.path.isdir("saved images"):
                os.mkdir("saved images")
            if x_maps * y_maps == 1:
                visual.save(file_n)
            else:
                visual.save_split(file_n, x_maps, y_maps)
            if save == "w":
                cwd = os.getcwd()
                file_path = os.path.join(cwd, "saved images", file_n + ".png")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 0)

        visual.close()
        quit()


    def image_thread():
        if not args.headless_opt:
            visual.show()


    t = Thread(target=prompt)
    t.daemon = True
    img_t = Thread(target=image_thread)
    img_t.daemon = True
    t.start()
    img_t.start()
    t.join()
    img_t.join()

else:
    print(
        "\n"
        "C R E D I T S" + "\n\n" +
        "* Map generator by Klaas" + "\n" +
        "* Javascript stuff and various assistance by Dirk" + "\n" +
        "* inputs argparser by Bethune Bryant" + "\n" +
        "* Rocket balloon by Akhera" + "\n" +
        "* Npc sprites ripped by Silentninja" + "\n\n" +
        "(Cool ideas and some inspiration from nice redditors on r/pokemon)")
