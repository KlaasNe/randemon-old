import time
import datetime
import pygame
import os
import random
import math
from noise import pnoise2, snoise2


def get_int(lower_bound, upper_bound, message):
    integer = int(input(message + " (" + str(lower_bound) + "-" + str(upper_bound) + "): "))
    while integer < lower_bound or integer > upper_bound:
        integer = int(input(message + " (" + str(lower_bound) + "-" + str(upper_bound) + "): "))
    return integer


def random_grass(decoration_rate):
    if random.random() > (decoration_rate / 100):
        temp_grass = random.randint(0, 3)
        return "g_" + str(temp_grass)
    else:
        if random.random() < 0.001 and not ground_Tiles["Diglet"]:
            ground_Tiles["Diglet"] = True
            if random.random() < 0.02:
                return "diglet_2"
            else:
                return "diglet_1"
        else:
            temp_sne = random.randint(0, 4)
            return "sne_" + str(temp_sne)


def fill_up_grass(layer, decoration_rate):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if not (x, y) in layer.keys():
                layer[(x, y)] = random_grass(decoration_rate)


def generate_path(layer, path_Type, path_Amount, path_Length):
    """
    //random path generation

    for path in range(0, path_Amount):
        start_coordinates = path_start_random(layer, path_Type)
        extend_Path(layer, path_Type, start_coordinates[0], start_coordinates[1], start_coordinates[2], start_coordinates[3], start_coordinates[4], random.randint(2, path_Length))
    calculate_bridges(layer)
    calculate_Paths(layer)
    """
    for house in range(0, len(houses_Connecters) - 1):
        distance1 = int(houses_Connecters[house]["Left_Connect"][0] - houses_Connecters[house + 1]["Right_Connect"][0])
        distance2 = int(houses_Connecters[house]["Right_Connect"][0] - houses_Connecters[house + 1]["Left_Connect"][0])
        if distance1 <= -2 and distance2 <= -2:
            x_difference = max(distance1, distance2)
            y_difference = houses_Connecters[house]["Left_Connect"][1] - houses_Connecters[house + 1]["Left_Connect"][1]
            start_x_horizontal = int(houses_Connecters[house]["Right_Connect"][0])
            start_y_horizontal = int(houses_Connecters[house + 1]["Left_Connect"][1])
            start_x_vertical = int(houses_Connecters[house]["Right_Connect"][0])
            start_y_vertical = min(int(houses_Connecters[house]["Left_Connect"][1]), houses_Connecters[house + 1]["Left_Connect"][1])
        elif distance1 >= 2 and distance2 >= 2:
            x_difference = min(distance1, distance2)
            y_difference = houses_Connecters[house]["Left_Connect"][1] - houses_Connecters[house + 1]["Left_Connect"][1]
            start_x_horizontal = int(houses_Connecters[house + 1]["Right_Connect"][0])
            start_y_horizontal =int(houses_Connecters[house]["Left_Connect"][1])
            start_x_vertical = int(houses_Connecters[house + 1]["Right_Connect"][0])
            start_y_vertical = min(int(houses_Connecters[house]["Left_Connect"][1]), houses_Connecters[house + 1]["Left_Connect"][1])
        elif distance1 <= 2 and distance2 >= 0:
            x_difference = int(houses_Connecters[house]["Left_Connect"][0] - houses_Connecters[house + 1]["Left_Connect"][0])
            y_difference = houses_Connecters[house]["Left_Connect"][1] - houses_Connecters[house + 1]["Left_Connect"][1]
            start_x_horizontal = int(houses_Connecters[house + 1]["Left_Connect"][0])
            start_y_horizontal = int(houses_Connecters[house]["Left_Connect"][1])
            start_x_vertical = int(houses_Connecters[house + 1]["Left_Connect"][0])
            start_y_vertical = min(int(houses_Connecters[house]["Left_Connect"][1]), houses_Connecters[house + 1]["Left_Connect"][1])
        else:
            x_difference = int(houses_Connecters[house]["Right_Connect"][0] - houses_Connecters[house + 1]["Right_Connect"][0])
            y_difference = houses_Connecters[house]["Left_Connect"][1] - houses_Connecters[house + 1]["Left_Connect"][1]
            start_x_horizontal = int(houses_Connecters[house]["Right_Connect"][0])
            start_y_horizontal = int(houses_Connecters[house]["Left_Connect"][1])
            start_x_vertical = int(houses_Connecters[house + 1]["Right_Connect"][0])
            start_y_vertical = min(int(houses_Connecters[house]["Left_Connect"][1]), houses_Connecters[house + 1]["Left_Connect"][1])

        x_difference = abs(x_difference)
        y_difference = abs(y_difference)
        for path in range(2 * y_difference + 4):
            x = start_x_vertical + (path % 2)
            y = start_y_vertical + math.floor(path / 2)
            if (x, y) in layer.keys() and ("pd_" in layer[(x, y)] or "b_" in layer[(x, y)]):
                layer[(x, y)] = "b_"
            else:
                if not (x, y) in layer.keys(): ground_Tiles[(x, y)] = "p_" + str(path_Type)

        for path in range(2 * x_difference + 4):
            x = start_x_horizontal + (path % (x_difference + 2))
            y = start_y_horizontal + math.floor(path / (x_difference + 2))
            if (x, y) in layer.keys() and ("pd_" in layer[(x, y)] or "b_" in layer[(x, y)]):
                layer[(x, y)] = "b_"
            else:
                if not (x, y) in layer.keys(): ground_Tiles[(x, y)] = "p_" + str(path_Type)

        calculate_bridges(layer)
        calculate_platforms(layer)


def out_Of_Bounds(x, y):
    if x < 0 or y < 0 or x >= map_Size_X or y >= map_Size_Y:
        return True
    else:
        return False


def random_adjacent_tile(layer, current_X, current_Y):
    direction = random.randint(0, 3)
    temp_x_change = direction_To_Change(direction)[0]
    temp_y_change = direction_To_Change(direction)[1]
    new_X = current_X
    new_Y = current_Y
    new_X += temp_x_change
    new_Y += temp_y_change
    while out_Of_Bounds(new_X, new_Y) or taken(layer, new_X, new_Y):
        new_X = current_X
        new_Y = current_Y
        direction = random.randint(0, 3)
        temp_x_change = direction_To_Change(direction)[0]
        temp_y_change = direction_To_Change(direction)[1]
        new_X += temp_x_change
        new_Y += temp_y_change

    return (current_X, current_Y, new_X, new_Y, direction)


def path_start_random(layer, path_Type):
    temp_path_point_X = random.randint(1, map_Size_X - 1)
    temp_path_point_Y = random.randint(1, map_Size_Y - 1)
    while (temp_path_point_X, temp_path_point_Y) in layer.keys():
        temp_path_point_X = random.randint(1, map_Size_X - 1)
        temp_path_point_Y = random.randint(1, map_Size_Y - 1)

    adjacent_Tile_Coordinates = random_adjacent_tile(layer, temp_path_point_X, temp_path_point_Y)
    layer[temp_path_point_X, temp_path_point_Y] = "p_" + str(path_Type)
    layer[(adjacent_Tile_Coordinates[2], adjacent_Tile_Coordinates[3])] = "p_" + str(path_Type)
    start_coordinates = extend_Path(layer, path_Type, temp_path_point_X, temp_path_point_Y, adjacent_Tile_Coordinates[2], adjacent_Tile_Coordinates[3], adjacent_Tile_Coordinates[4], 1)
    return start_coordinates


def taken(layer, x, y):
    if (x, y) in layer.keys():
        return True
    else:
        return False


def extend_Path(layer, path_Type, x1, y1, x2, y2, direction, length):
    x_change = direction_To_Change((direction + 1) % 4)[0]
    y_change = direction_To_Change((direction + 1) % 4)[1]
    new_x1 = x1
    new_y1 = y1
    new_x2 = x2
    new_y2 = y2
    for extending in range(0, length):
        new_x1 += x_change
        new_y1 += y_change
        new_x2 += x_change
        new_y2 += y_change
        walk_on_water = False
        if 1: #not "p_" in str(layer.get((new_x1, new_y1), 0)) and not "p_" in str(layer.get((new_x2, new_y2), 0)):
            if not (new_x1, new_y1) in layer.keys():
                layer[(new_x1, new_y1)] = "p_" + str(path_Type)
            elif layer[(new_x1, new_y1)] == "pd_":
                layer[(new_x1, new_y1)] = "b_"
                walk_on_water = True

            if not (new_x2, new_y2) in layer.keys():
                layer[(new_x2, new_y2)] = "p_" + str(path_Type)
            elif layer[(new_x2, new_y2)] == "pd_":
                layer[(new_x2, new_y2)] = "b_"
                walk_on_water = True
            if walk_on_water == True: extend_Path(layer, path_Type, new_x1, new_y1, new_x2, new_y2, direction, 2)

    new_coordinates = [new_x1, new_y1, new_x2, new_y2, direction]
    return new_coordinates


def direction_To_Change(direction):
    x_change = 0
    y_change = 0
    if direction == 0: x_change = 1
    if direction == 1: y_change = -1
    if direction == 2: x_change = -1
    if direction == 3: y_change = 1
    return (x_change, y_change)


def calculate_Paths(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if (x, y) in layer and "p_" in layer[(x, y)]:
                path = calculate_path_look(layer, x, y)
                layer[(x, y)] = str(layer[(x, y)]) + str(path)


def calculate_bridges(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if (x, y) in layer and layer[(x, y)] == "b_":
                bridge = calculate_bridge_look(layer, x, y)
                if bridge == 0:
                    layer[(x, y)] = "pl_"
                else:
                    layer[(x, y)] = "b_" + str(bridge)
                if bridge == 1: layer[(x, y + 1)] = "b_2"
                if bridge == 2: layer[(x, y - 1)] = "b_1"
                if bridge == 3: layer[(x + 1, y)] = "b_4"
                if bridge == 4: layer[(x - 1, y)] = "b_3"
    finish_bridges(layer)


def finish_bridges(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if "b_" in layer.get((x, y), ""):
                if (layer.get((x - 1, y), "") == "b_3" or layer.get((x - 1, y), "") == "b_6") and (layer.get((x + 1, y), "") == "b_3" or layer.get((x + 1, y), "") == "b_4"):
                    layer[(x, y)] = "b_6"
                if (layer.get((x, y - 1), "") == "b_1" or layer.get((x, y - 1), "") == "b_5") and (layer.get((x, y + 1), "") == "b_1" or layer.get((x, y + 1), "") == "b_2"):
                    layer[(x, y)] = "b_5"


def calculate_bridge_look(layer, x, y):
    if layer.get((x - 1, y), 0) == "pd_":
        if not (x + 2, y) in layer.keys(): layer[(x + 2, y)] = "pd_"
        return 3
    if layer.get((x + 1, y), 0) == "pd_":
        if not (x - 2, y) in layer.keys(): layer[(x - 2, y)] = "pd_"
        return 4
    if layer.get((x, y - 1), 0) == "pd_":
        if not (x, y + 2) in layer.keys(): layer[(x, y + 2)] = "pd_"
        return 1
    if layer.get((x, y + 1), 0) == "pd_":
        if not (x, y - 2) in layer.keys(): layer[(x, y - 2)] = "pd_"
        return 2
    return 0


def calculate_platforms(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if layer.get((x, y), "") == "pl_":
                layer[(x, y)] = "pl_1"
                layer[(x + 1, y)] = "pl_2"
                layer[(x, y + 1)] = "pl_3"
                layer[(x + 1, y + 1)] = "pl_4"


def calculate_path_look(layer, x, y):
    tiles_around = []
    for around in range(0, 9):
        path_around = layer.get((x + (around % 3) - 1, y + math.floor(around / 3) - 1), 0)
        if path_around == 0: path_around = house_Tiles.get((x + (around % 3) - 1, y + math.floor(around / 3) - 1), 0)
        if "p_" in str(path_around) or "b_" in str(path_around) or "pd_" in str(path_around) or "h_" in str(path_around) or "pl_" in str(path_around):
            tiles_around.append(1)
        else:
            tiles_around.append(0)
    if tiles_around == [1, 1, 1, 1, 1, 1, 0, 1, 1]: return "_9"
    if tiles_around == [1, 1, 1, 1, 1, 1, 1, 1, 0]: return "_10"
    if tiles_around == [1, 1, 0, 1, 1, 1, 1, 1, 1]: return "_11"
    if tiles_around == [0, 1, 1, 1, 1, 1, 1, 1, 1]: return "_12"
    if tiles_around == [1, 1, 1, 1, 1, 1, 1, 1, 1] or tiles_around == [0, 1, 0, 1, 0, 1, 0, 1, 0]: return "_0"
    if tiles_around == [0, 1, 1, 0, 1, 1, 0, 1, 1] or tiles_around == [1, 1, 1, 0, 1, 1, 0, 1, 1] or tiles_around == [0, 1, 1, 0, 1, 1, 1, 1, 1] or tiles_around == [1, 1, 1, 0, 1, 1, 1, 1, 1]: return "_1"
    if tiles_around == [1, 1, 1, 1, 1, 1, 0, 0, 0] or tiles_around == [1, 1, 1, 1, 1, 1, 1, 0, 0] or tiles_around == [1, 1, 1, 1, 1, 1, 0, 0, 1] or tiles_around == [1, 1, 1, 1, 1, 1, 1, 0, 1]: return "_2"
    if tiles_around == [1, 1, 0, 1, 1, 0, 1, 1, 0] or tiles_around == [1, 1, 1, 1, 1, 0, 1, 1, 0] or tiles_around == [1, 1, 0, 1, 1, 0, 1, 1, 1] or tiles_around == [1, 1, 1, 1, 1, 0, 1, 1, 1]: return "_3"
    if tiles_around == [0, 0, 0, 1, 1, 1, 1, 1, 1] or tiles_around == [1, 0, 0, 1, 1, 1, 1, 1, 1] or tiles_around == [0, 0, 1, 1, 1, 1, 1, 1, 1] or tiles_around == [1, 0, 1, 1, 1, 1, 1, 1, 1]: return "_4"
    if tiles_around[5] == 1 and tiles_around[7] == 1 and tiles_around[8] == 1: return "_5"
    if tiles_around[1] == 1 and tiles_around[2] == 1 and tiles_around[5] == 1: return "_6"
    if tiles_around[0] == 1 and tiles_around[1] == 1 and tiles_around[3] == 1: return "_7"
    if tiles_around[3] == 1 and tiles_around[6] == 1 and tiles_around[7] == 1: return "_8"
    return "_0"


def calculate_ponds(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if (x, y) in layer and (layer[(x, y)] == "pd_" or layer[(x, y)] == "b_"):
                pond = calculate_pond_look(layer, x, y)
                layer[(x, y)] = str(layer[(x, y)]) + str(pond)


def generate_ponds(layer, land_rate):
    """
    for ponds in range(0, amount):
        pool_point_x = random.randint(0, map_Size_X - 1)
        pool_point_y = random.randint(0, map_Size_Y - 1)
        while (pool_point_x, pool_point_y) in layer.keys():
            pool_point_x = random.randint(1, map_Size_X - 1)
            pool_point_y = random.randint(1, map_Size_Y - 1)

        opposing_corner = (pool_point_x + random.randint(2, maximum_size), pool_point_y + (random.randint(2, maximum_size)))
        for pond in range(0, (opposing_corner[0] - pool_point_x) * (opposing_corner[1] - pool_point_y)):
            layer[pool_point_x + (pond % (opposing_corner[0] - pool_point_x)), pool_point_y + math.floor(pond / (opposing_corner[0] - pool_point_x))] = "pd_"
    """
    octaves = 2
    freq = 70
    off_x = random.random() * 1000000
    off_y = random.random() * 1000000

    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            tile_height = snoise2((x + off_x) / freq, (y + off_y) / freq, octaves)
            if tile_height < 0 - land_rate and tile_height > land_rate - 0.4:
                    layer[(x, y)] = "pd_"


def calculate_pond_look(layer, x, y):
    tiles_around = []
    for around in range(0, 9):
        path_around = (layer.get((x + (around % 3) - 1, y + math.floor(around / 3) - 1), "0"))
        if not "p_" in str(path_around) and ("pd_" in str(path_around) or "b_" in str(path_around) or "pl_" in str(path_around)):
            tiles_around.append(1)
        else:
            tiles_around.append(0)
    if tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1:
        if random.random() < 0.001 and layer.get((x, y + 2), 0) == "pd_" and not layer["Lapras"]:
            layer["Lapras"] = True

            if random.randint(1, 2) == 1:
                direction = 1
            else:
                direction = 3

            if random.random() < 0.02:
                if random.randint(1, 2) == 1:
                    direction = 5
                else:
                    direction = 7
            layer[(x, y + 1)] = "pd_l_" + str(direction + 1)
            return "l_" + str(direction)
        elif random.random() < 0.001 and not layer["Gyarados"]:
            layer["Gyarados"] = True
            layer[(x + 1, y)] = "pd_g_2"
            layer[(x, y + 1)] = "pd_g_3"
            layer[(x + 1, y + 1)] = "pd_g_4"
            return "g_1"
        else:
            return 0
    if tiles_around[1] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1: return "1"
    if tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1: return "2"
    if tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[7] == 1: return "3"
    if tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1: return "4"
    if tiles_around[5] == 1 and tiles_around[7] == 1: return "5"
    if tiles_around[1] == 1 and tiles_around[5] == 1: return "6"
    if tiles_around[1] == 1 and tiles_around[3] == 1: return "7"
    if tiles_around[3] == 1 and tiles_around[7] == 1: return "8"
    if tiles_around[3] == 1 and tiles_around[5] == 1: return "13"
    if tiles_around[1] == 1 and tiles_around[7] == 1: return "14"
    if tiles_around[1] == 1: return "9"
    if tiles_around[3] == 1: return "10"
    if tiles_around[5] == 1: return "12"
    if tiles_around[7] == 1: return "11"
    return "15"


def spawn_mne(layer, spawn_rate):
    octaves = 3
    freq = 40
    off_x = random.random() * 1000000
    off_y = random.random() * 1000000
    for y in range(map_Size_Y):
        for x in range(map_Size_X):
            mne_biomes[(x, y)] = snoise2((x + off_x) / freq, (y + off_y) / freq, octaves) * 2 + (spawn_rate / 100)

    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if not (x, y) in layer.keys() and not (x, y - 1) in layer.keys() and not (x, y - 2) in layer.keys() and not (x, y) in house_Tiles.keys() and not (x, y - 1) in house_Tiles.keys() and not (x, y - 2) in house_Tiles.keys():
                if mne_biomes[(x, y)] > 0.5 and random.random() > 0.6:
                    layer[(x, y)] = "st_0"
                    layer[(x, y - 1)] = "st_1"
                    layer[(x, y - 2)] = "st_2"

def spawn_house(layer, house_type, house_size_x, house_size_y, amount):
    for houses in range(0, amount):
        house_x = random.randint(1, map_Size_X - house_size_y)
        house_y = random.randint(1, map_Size_Y - house_size_x)
        while not check_availability_zone(ground_Tiles, house_x - 1, house_y - 1, house_size_x + 1, house_size_y + 4) or not check_availability_zone(house_Tiles, house_x - 1, house_y - 1, house_size_x + 1, house_size_y + 4):
            house_x = random.randint(1, map_Size_X - house_size_x)
            house_y = random.randint(1, map_Size_Y - house_size_y)
        for house_tile in range(1, house_size_x * house_size_y + 1):
            layer[(house_x + (house_tile - 1) % house_size_x, house_y  + math.floor((house_tile - 1) / house_size_x))] = "h_" + str(house_type) + "_" + str(house_tile)
        for front in range(2 * house_size_x):
            ground_Tiles[(house_x + front % house_size_x, house_y + math.floor(front / house_size_x) + house_size_y)] = "p_2"
        houses_Connecters[len(houses_Connecters)] = {"Left_Connect": (house_x - 2, house_y + house_size_y), "Right_Connect": (house_x + house_size_x, house_y + house_size_y)}


def check_availability_zone(layer, start_x, start_y, x_size, y_size):
    availability = True
    for tile in range(x_size * y_size):
        if (start_x + tile % x_size, start_y + math.floor(tile / y_size)) in layer.keys() or out_Of_Bounds(start_x + tile % x_size, start_y + math.floor(tile / y_size)): availability = False
    return availability


def render(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if (x, y) in layer.keys():
                tile = str(layer[(x, y)])
                screen.blit(pygame.image.load(os.path.join("resources", tile + ".png")), (x * tile_Size, y * tile_Size))
    pygame.display.update()

ground_Tiles = {"Lapras": False, "Diglet": False, "Gyarados": False}
#while not ground_Tiles["Lapras"] or not ground_Tiles["Gyarados"] or not ground_Tiles["Diglet"]:

tile_Size = 16
map_Size_X = 50 #get_int(10, 100, "Amount of tiles in x-direction")
map_Size_Y = 50 #get_int(10, 100, "Amount of tiles in y-direction")
screen_Size_X = tile_Size * map_Size_X
screen_Size_Y = tile_Size * map_Size_Y
sne_rate = 7 #get_int(0, 100, "Small size nature elements spawn rate")
mne_rate = 20 #get_int(0, 100, "Medium size nature elements spawn rate")

user_Path_Amount = 2 #get_int(0, 4, "Amount of paths to generate")
user_Path_Length = 25
#if user_Path_Amount != 0: user_Path_Length = get_int(1, 24, "Maximum length of a path")

ground_Tiles = {"Lapras": False, "Diglet": False, "Gyarados": False}
mne_biomes = {}
house_Tiles = {}
houses_Connecters = {}
generate_ponds(ground_Tiles, 0.0)
spawn_house(house_Tiles, 1, 4, 4, 4)
spawn_house(house_Tiles, 2, 5, 3, 4)
generate_path(ground_Tiles, 1, user_Path_Amount, user_Path_Length)
calculate_Paths(ground_Tiles)
calculate_ponds(ground_Tiles)
spawn_mne(ground_Tiles, mne_rate)
fill_up_grass(ground_Tiles, sne_rate)

screen = pygame.display.set_mode((screen_Size_X, screen_Size_Y))
render(ground_Tiles)
render(house_Tiles)

save = input("Save this image? (y/n): ")
t = datetime.datetime.now().strftime("%G-%m-%d %H-%M-%S")
if save == "y": pygame.image.save(screen, os.path.join("saved images", t+".png"))
