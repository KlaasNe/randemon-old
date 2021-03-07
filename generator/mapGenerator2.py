import ctypes
import datetime
import json
import os
import random
import time
from os import path
from threading import Thread

import image.spriteSheetManager as ssm
import utilities.parser as inputs
from utilities import *
from Layers import *
from generators import *
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

    def toJSON(self):
        resp = {
            'buildings': dictToObject(self.buildings.get_tiles()),
            'ground_layer': dictToObject(self.ground.get_tiles()),
            'secondary_ground': dictToObject(self.ground2.get_tiles()),
            'rain': dictToObject(self.rain.get_tiles()),
            'decoration_layer': dictToObject(self.decoration.get_tiles()),
            'npc_layer': dictToObject(self.npc.get_tiles()),
            'height_map': dictToObject(self.hills.get_tiles()),
            'grass_layer': dictToObject(self.plants.get_tiles()),
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
    path_type = ("pa", 0, 0)

    rmap = Map(map_size_x, map_size_y, args.max_hill_height, args.tall_grass_coverage, args.tree_coverage, 0.2)

    if args.headless_opt: os.environ["SDL_VIDEODRIVER"] = "dummy"

    visual = ssm.DrawSheet(screen_Size_X, screen_Size_Y)

    to_time = time()
    print("*creating landscape*")
    rmap.tile_heights = generate_height_map((rmap.width, rmap.height), rmap.max_hill_height, x_offset, y_offset)
    create_rivers(rmap.ground, rmap.tile_heights)
    create_beach(rmap.ground, rmap.tile_heights, x_offset, y_offset)
    add_random_ends(rmap, path_type)
    create_hill_edges(rmap, rmap.ground, rmap.tile_heights)
    # # house = time()
    spawn_house(rmap, rmap.buildings, "pokecenter", path_type)
    spawn_house(rmap, rmap.buildings, "pokemart", path_type)
    spawn_house(rmap, rmap.buildings, "gym", path_type)
    spawn_house(rmap, rmap.buildings, "powerplant", path_type)
    for x in range(1):
        for osso in range(22):
            house_type = random.randint(0, 21)
            spawn_house(rmap, rmap.buildings, house_type, path_type)
    # print("time = " + str(time() - house) + " seconds")
    random.shuffle(rmap.front_doors)
    rmap.front_doors += rmap.end_points
    generate_dijkstra_path(rmap, rmap.ground, path_type)
    apply_path_sprites(rmap, rmap.ground)

    create_hill_edges(rmap, rmap.ground, rmap.tile_heights, update=True)
    create_trees(rmap, rmap.ground, rmap.tree_coverage, x_offset, y_offset)
    # grow_snake_bushes(rmap.ground, 0.1, 0.9)
    all_pokemon = spawn_pokemons(rmap)
    spawn_npc(rmap, rmap.npc, 1)
    create_lanterns(rmap)
    spawn_truck(rmap, 0.05)
    spawn_rocks(rmap, 0.01)
    spawn_umbrellas(rmap)
    spawn_balloon(rmap)
    grow_grass(rmap, rmap.tall_grass_coverage, x_offset, y_offset)
    create_rain(rmap, rmap.rain, 0.1, rmap.rain_rate)

    print("*rendering*")
    render2(rmap.plants, visual.drawable())
    render2(rmap.ground, visual.drawable())
    render2(rmap.ground2, visual.drawable())
    render2(rmap.buildings, visual.drawable())
    render_npc(rmap.npc, visual.drawable())
    render2(rmap.decoration, visual.drawable())
    render2(rmap.rain, visual.drawable())
    print("time = " + str(time() - to_time) + " seconds")
    print("Seed: " + str(args.seed_opt))


    def prompt():
        if args.save_opt:
            save = "y"
        else:
            save = input("Save this image? (y/n/w): ")
        file_n = datetime.datetime.now().strftime("%G-%m-%d %H-%M-%S")
        if args.export_opt:
            json_string = rmap.toJSON()
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
        "* argparser by Bethune Bryant" + "\n" +
        "* Rocket balloon by Akhera" + "\n" +
        "* Some sprites from a spritesheet ripped by Heartlessdragoon" + "\n" +
        "* Npc sprites ripped by Silentninja" + "\n\n" +
        "(Cool ideas and some inspiration from nice redditors on r/pokemon)")
