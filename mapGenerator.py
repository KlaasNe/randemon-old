import datetime, pygame, os, random, math, sys
from noise import pnoise2, snoise2
from time import sleep

seed = random.randint(0, sys.maxsize)
zaad = seed
random.seed(zaad)


def get_int(lower_bound, upper_bound, message):
    integer = int(input(message + " (" + str(lower_bound) + "-" + str(upper_bound) + "): "))
    while integer < lower_bound or integer > upper_bound:
        integer = int(input(message + " (" + str(lower_bound) + "-" + str(upper_bound) + "): "))
    return integer


def random_grass(decoration_rate, x, y, off_x, off_y):
    octaves = 1
    freq = 7

    sne_prob = snoise2((x + off_x) / freq, (y + off_y) / freq, octaves) + 0.5
    if sne_prob > (decoration_rate / 100):
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
            while not (temp_sne == 0 or temp_sne == 2):
                temp_sne = random.randint(0, 4)
            if temp_sne == 2 and random.random() < 0.8: temp_sne = 0
            if temp_sne == 0 and random.random() < 0.005: temp_sne = "0_p"
            return "sne_" + str(temp_sne)


def fill_up_grass(layer, decoration_rate, offset_x, offset_y):
    off_x = offset_x
    off_y = offset_y
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if not (x, y) in layer.keys():
                layer[(x, y)] = random_grass(decoration_rate, x, y, off_x, off_y)


def generate_path(layer, path_Type, path_width):
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
            start_y_horizontal = int(houses_Connecters[house]["Left_Connect"][1])
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
        if path_Type == "r":
            path_layout = random.randint(1, 3)
        else:
            path_layout = path_Type

#vertical path

        path_height = tile_Heights.get((start_x_vertical, start_y_vertical), 0)

        for path in range(path_width * y_difference + 2 * path_width):
            x = start_x_vertical + (path % path_width)
            y = start_y_vertical + math.floor(path / path_width)

            if path % 2 == 0:
                try_horizontal_stairs(x, y, path_height)
                try_backdoor(house_Tiles, x, y + 1)

            if "b_" not in layer.get((x, y), "") and (layer.get((x, y), "") == "pd_" or layer.get((x, y + 1), "") == "pd_"):
                layer[(x, y)] = "b_" + str((path % 2) + 3)
            else:
                if path % 2 == 0 and path_height > 0:
                    if tile_Heights.get((x - 1, y), path_height) < path_height and "p_" not in layer.get((x - 1, y), ""): tile_Heights[(x - 1, y)] = path_height
                    if tile_Heights.get((x + 2, y), path_height) < path_height and "p_" not in layer.get((x + 2, y), ""): tile_Heights[(x + 2, y)] = path_height

                if not (x, y) in layer.keys():
                    ground_Tiles[(x, y)] = "p_" + str(path_layout)

            path_height = tile_Heights.get((x, y + 1), path_height)

        finish_bridges(layer)

#horizontal path

        path_height = tile_Heights.get((start_x_horizontal, start_y_horizontal), path_height)
        for path in range(path_width * (x_difference + 2)):
            x = start_x_horizontal + (path % (x_difference + 2))
            y = start_y_horizontal + path // (x_difference + 2)

            if path // (x_difference + 2) == 0:
                try_vertical_stairs(x, y, path_height)

            if "b_" not in layer.get((x, y), "") and (layer.get((x, y), "") == "pd_" or layer.get((x + 1, y), "") == "pd_" or tile_Heights.get((x - 1, y), path_height) < 1):
                layer[(x, y)] = "b_" + str(path // (x_difference + 2) + 1)
            else:
                if path // (x_difference + 2) == 0 and path_height > 0:
                    if tile_Heights.get((x, y - 1), path_height) < path_height and "p_" not in layer.get((x, y - 1), ""):tile_Heights[(x, y - 1)] = path_height
                    if tile_Heights.get((x, y + 2), path_height) < path_height and "p_" not in layer.get((x, y + 2), ""): tile_Heights[(x, y + 2)] = path_height
                if not (x, y) in layer.keys():
                    ground_Tiles[(x, y)] = "p_" + str(path_layout)

            path_height = tile_Heights.get((x + 1, y), path_height)

        finish_bridges(layer)
        remove_half_stairs(layer)
        #move_faulty_stairs(layer)
        finish_stairs(layer)

    #remove_half_stairs(layer)
    calculate_platforms(layer)
    finish_hills(layer)
    finishing_touches_bridges(layer)


def try_horizontal_stairs(x, y, path_height):
    if not out_Of_Bounds(x + 1, y + 1) and not out_Of_Bounds(x, y):
        if tile_Heights[(x, y + 1)] != tile_Heights[(x + 1, y + 1)]:
            tile_Heights[(x, y + 1)] = min(tile_Heights[(x, y + 1)], tile_Heights[(x + 1, y + 1)])
            tile_Heights[(x + 1, y + 1)] = min(tile_Heights[(x, y + 1)], tile_Heights[(x + 1, y + 1)])
        if path_height > 0:
            if tile_Heights[(x, y + 1)] < path_height and tile_Heights[(x, y + 1)] > 0:
                ground_Tiles[(x, y)] = "sta_1_0"
                ground_Tiles[(x + 1, y)] = "sta_1_1"
            elif tile_Heights[(x, y + 1)] > path_height and tile_Heights[(x, y + 1)] > 0:
                ground_Tiles[(x, y + 1)] = "sta_8_0"
                ground_Tiles[(x + 1, y + 1)] = "sta_8_1"


def try_vertical_stairs(x, y, path_height):
    if not out_Of_Bounds(x + 1, y + 1) and not out_Of_Bounds(x, y):
        if tile_Heights[(x + 1, y)] != tile_Heights[(x + 1, y + 1)]:
            tile_Heights[(x + 1, y)] = min(tile_Heights[(x + 1, y)], tile_Heights[(x + 1, y + 1)])
            tile_Heights[(x + 1, y + 1)] = min(tile_Heights[(x + 1, y)], tile_Heights[(x + 1, y + 1)])
        if path_height > 0:
            if tile_Heights[(x + 1, y)] < path_height and tile_Heights[(x + 1, y)] > 0:
                ground_Tiles[(x, y)] = "sta_6_1"
                ground_Tiles[(x, y + 1)] = "sta_6_0"
            elif tile_Heights[(x + 1, y)] > path_height and tile_Heights[(x + 1, y)] > 0:
                ground_Tiles[(x + 1, y)] = "sta_3_1"
                ground_Tiles[(x + 1, y + 1)] = "sta_3_0"


def  try_backdoor(layer, x, y):
    if "h_" in layer.get((x, y), "") and "h_" in layer.get((x + 1, y), "") and not "h_" in layer.get((x, y - 1), ""):
        if "bd_" in decoration_Tiles.get((x - 1, y), ""):
            decoration_Tiles[(x, y)] = "bd_1"
            if decoration_Tiles.get((x - 1, y), "") == "bd_2": decoration_Tiles[(x - 1, y)] = "bd_1"
        else:
            decoration_Tiles[(x, y)] = "bd_0"
        if "bd_" in decoration_Tiles.get((x + 2, y), ""):
            decoration_Tiles[(x + 1, y)] = "bd_1"
            if decoration_Tiles.get((x + 1, y), "") == "bd_0": decoration_Tiles[(x + 1, y)] = "bd_1"
        else:
            decoration_Tiles[(x + 1, y)] = "bd_2"


def finish_stairs(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if "sta_" in layer.get((x, y),""):
                if layer.get((x, y), "") == "sta_1_0" and "sta_" in layer.get((x - 1, y), ""):
                    layer[(x, y)] = "sta_1_1"
                if layer.get((x, y), "") == "sta_3_0" and "sta_" in layer.get((x, y + 1), ""):
                    layer[(x, y)] = "sta_3_1"
                if layer.get((x, y), "") == "sta_6_0" and "sta_" in layer.get((x, y + 1), ""):
                    layer[(x, y)] = "sta_6_1"

                if "sta_3" in layer.get((x, y - 1), "") and "sta_" in layer.get((x, y + 1), ""):
                    layer[(x, y)] = "sta_3"
                if "sta_6" in layer.get((x, y - 1), "") and "sta_" in layer.get((x, y + 1), ""):
                    layer[(x, y)] = "sta_6"
                if "sta_8" in layer.get((x - 1, y), "") and "sta_" in layer.get((x + 1, y), ""):
                    layer[(x, y)] = "sta_8"
                if "sta_1" in layer.get((x - 1, y), "") and "sta_" in layer.get((x + 1, y), ""):
                    layer[(x, y)] = "sta_1_1"


def remove_half_stairs(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if "sta_" in layer.get((x, y), ""):
                stair_type = layer[(x, y)][4]
                if not check_stairs_around(layer, x, y, stair_type): layer[(x, y)] = "p_1"


def check_stairs_around(layer, x, y, stair_type):
    for tile in range(4):
        if "sta_" + stair_type in layer.get((x - 1 + ((2 * tile) + 1) % 3, y - 1 + ((2 * tile) + 1) // 3), ""): return True
    return False


def move_faulty_stairs(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if "sta_" in layer.get((x, y), ""):
                move_stair(layer, x, y)


def move_stair(layer, x, y):
    if "sta_" in layer.get((x, y), ""):
        stair = layer.get((x, y), "")
        stair_type = int(stair[4])
        try:
            stair_subtype = int(stair[6])
        except Exception as e:
            stair_subtype = -1
        move_stair_tile(layer, x, y, stair, stair_type)
        fix_adjacent_hill(layer, x, y, stair_type, stair_subtype)


def move_stair_tile(layer, x, y, stair, stair_type):
    if stair_type == 1:
        if tile_Heights.get((x, y), 0) < tile_Heights.get((x, y - 1), 0):
            move_stair_tile_to(layer, x, y, x, y - 1, "p_1", stair)
        elif tile_Heights.get((x, y), 0) == tile_Heights.get((x, y + 1), 0):
            move_stair_tile_to(layer, x, y, x, y + 1, "p_1", stair)
    elif stair_type == 3:
        if tile_Heights.get((x, y), 0) < tile_Heights.get((x + 1, y), 0):
            move_stair_tile_to(layer, x, y, x + 1, y, "p_1", stair)
        elif tile_Heights.get((x, y), 0) == tile_Heights.get((x - 1, y), 0):
            move_stair_tile_to(layer, x, y, x - 1, y, "p_1", stair)
    elif stair_type == 6:
        if tile_Heights.get((x, y), 0) < tile_Heights.get((x - 1, y), 0):
            move_stair_tile_to(layer, x, y, x - 1, y, "p_1", stair)
        elif tile_Heights.get((x, y), 0) == tile_Heights.get((x + 1, y), 0):
            move_stair_tile_to(layer, x, y, x + 1, y, "p_1", stair)
    elif stair_type == 8:
        if tile_Heights.get((x, y), 0) < tile_Heights.get((x, y + 1), 0):
            move_stair_tile_to(layer, x, y, x, y + 1, "p_1", stair)
        elif tile_Heights.get((x, y), 0) == tile_Heights.get((x, y - 1), 0):
            move_stair_tile_to(layer, x, y, x, y - 1, "p_1", stair)


def move_stair_tile_to(layer, x, y, new_x, new_y, replace_tile, stair):
    if "sta_" in layer.get((x, y), ""):
        stair_type = int(stair[4])
        layer[(new_x, new_y)] = stair
        layer[(x, y)] = replace_tile


def fix_adjacent_hill(layer, x, y, stair_type, stair_subtype):
    if stair_type == 1 or stair_type == 8:
        if stair_subtype == 0:
            tile_Heights[(x - 1, y)] = tile_Heights[(x, y)]
        elif stair_subtype == 1:
            tile_Heights[(x + 1, y)] = tile_Heights[(x, y)]
    elif stair_type == 3 or stair_type == 6:
        if stair_subtype == 1:
            tile_Heights[(x, y - 1)] = tile_Heights[(x, y)]
        elif stair_subtype == 0:
            tile_Heights[(x, y + 1)] = tile_Heights[(x, y)]


def out_Of_Bounds(x, y):
    if x < 0 or y < 0 or x >= map_Size_X or y >= map_Size_Y:
        return True
    else:
        return False


def random_adjacent_tile(layer, current_X, current_Y):
    direction = random.randint(0, 3)
    temp_x_change = direction_to_change(direction)[0]
    temp_y_change = direction_to_change(direction)[1]
    new_X = current_X
    new_Y = current_Y
    new_X += temp_x_change
    new_Y += temp_y_change
    while out_Of_Bounds(new_X, new_Y) or taken(layer, new_X, new_Y):
        new_X = current_X
        new_Y = current_Y
        direction = random.randint(0, 3)
        temp_x_change = direction_to_change(direction)[0]
        temp_y_change = direction_to_change(direction)[1]
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
    x_change = direction_to_change((direction + 1) % 4)[0]
    y_change = direction_to_change((direction + 1) % 4)[1]
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


def direction_to_change(direction):
    x_change = 0
    y_change = 0
    if direction == 0: x_change = 1
    if direction == 1: y_change = -1
    if direction == 2: x_change = -1
    if direction == 3: y_change = 1
    return (x_change, y_change)


def calculate_paths(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if (x, y) in layer and "p_" in layer[(x, y)]:
                path = calculate_path_look(layer, x, y)
                if not path == "_er":
                    layer[(x, y)] = str(layer[(x, y)]) + str(path)
                else:
                    layer[(x, y)] = "g_0"

    #finish_path_edges(layer)


def finish_bridges(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if layer.get((x, y), "") == "b_1" and "p_" in layer.get((x, y + 1), ""): layer[(x, y + 1)] = "b_2"
            if layer.get((x, y), "") == "b_2" and "p_" in  layer.get((x, y - 1), ""): layer[(x, y - 1)] = "b_1"
            if layer.get((x, y), "") == "b_3" and "p_" in layer.get((x + 1, y), ""): layer[(x + 1, y)] = "b_4"
            if layer.get((x, y), "") == "b_4" and "p_" in layer.get((x - 1, y), ""): layer[(x - 1, y)] = "b_3"
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if "b_" in layer.get((x, y), ""):
                if (layer.get((x - 1, y), "") == "b_3" or layer.get((x - 1, y), "") == "b_6") and (layer.get((x + 1, y), "") == "b_3" or layer.get((x + 1, y), "") == "b_4" or layer.get((x + 1, y), "") == "b_6"):
                    layer[(x, y)] = "b_6"
                if (layer.get((x, y - 1), "") == "b_1" or layer.get((x, y - 1), "") == "b_5") and (layer.get((x, y + 1), "") == "b_1" or layer.get((x, y + 1), "") == "b_2" or layer.get((x, y + 1), "") == "b_5"):
                    layer[(x, y)] = "b_5"


def finishing_touches_bridges(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if "b_" in layer.get((x, y - 1), "") and "pd_" in layer.get((x, y), ""):
                decoration_Tiles[(x, y)] = "bu_0"


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
        if "p_" in str(path_around) or "b_" in str(path_around) or "pl_" in str(path_around) or "sta_" in str(path_around) or "m_4_p" in str(path_around) or "pd_" in str(path_around) or out_Of_Bounds(x + (around % 3) - 1, y + math.floor(around / 3) - 1):
            tiles_around.append(1)
        else:
            tiles_around.append(0)
    if tiles_around == [1, 1, 1, 1, 1, 1, 0, 1, 1]: return "_9"
    if tiles_around == [1, 1, 1, 1, 1, 1, 1, 1, 0]: return "_10"
    if tiles_around == [1, 1, 0, 1, 1, 1, 1, 1, 1]: return "_11"
    if tiles_around == [0, 1, 1, 1, 1, 1, 1, 1, 1]: return "_12"
    if tiles_around == [1, 1, 1, 1, 1, 1, 1, 1, 1] or (tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1): return "_0"
    if tiles_around == [0, 1, 1, 0, 1, 1, 0, 1, 1] or tiles_around == [1, 1, 1, 0, 1, 1, 0, 1, 1] or tiles_around == [0, 1, 1, 0, 1, 1, 1, 1, 1] or tiles_around == [1, 1, 1, 0, 1, 1, 1, 1, 1]: return "_1"
    if tiles_around == [1, 1, 1, 1, 1, 1, 0, 0, 0] or tiles_around == [1, 1, 1, 1, 1, 1, 1, 0, 0] or tiles_around == [1, 1, 1, 1, 1, 1, 0, 0, 1] or tiles_around == [1, 1, 1, 1, 1, 1, 1, 0, 1]: return "_2"
    if tiles_around == [1, 1, 0, 1, 1, 0, 1, 1, 0] or tiles_around == [1, 1, 1, 1, 1, 0, 1, 1, 0] or tiles_around == [1, 1, 0, 1, 1, 0, 1, 1, 1] or tiles_around == [1, 1, 1, 1, 1, 0, 1, 1, 1]: return "_3"
    if tiles_around == [0, 0, 0, 1, 1, 1, 1, 1, 1] or tiles_around == [1, 0, 0, 1, 1, 1, 1, 1, 1] or tiles_around == [0, 0, 1, 1, 1, 1, 1, 1, 1] or tiles_around == [1, 0, 1, 1, 1, 1, 1, 1, 1]: return "_4"
    if tiles_around[5] == 1 and tiles_around[7] == 1 and tiles_around[8] == 1: return "_5"
    if tiles_around[1] == 1 and tiles_around[2] == 1 and tiles_around[5] == 1: return "_6"
    if tiles_around[0] == 1 and tiles_around[1] == 1 and tiles_around[3] == 1: return "_7"
    if tiles_around[3] == 1 and tiles_around[6] == 1 and tiles_around[7] == 1: return "_8"
    return "_er"


def finish_path_edges(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if tile_Heights.get((x, y), 0) > tile_Heights.get((x, y + 1), 0) and "p_" in layer.get((x, y), "") and "p_" in layer.get((x, y + 1), ""):
                layer[(x, y)] = "p_1_2_m"
            elif tile_Heights.get((x, y), 0) > tile_Heights.get((x, y - 1), 0) and "p_" in layer.get((x, y), "") and "p_" in layer.get((x, y - 1), ""):
                layer[(x, y)] = "p_1_4_m"
            elif tile_Heights.get((x, y), 0) > tile_Heights.get((x + 1, y), 0) and "p_" in layer.get((x, y), "") and "p_" in layer.get((x + 1, y), ""):
                layer[(x, y)] = "p_1_3_m"
            elif tile_Heights.get((x, y), 0) > tile_Heights.get((x - 1, y), 0) and "p_" in layer.get((x, y), "") and "p_" in layer.get((x + 1, y), ""):
                layer[(x, y)] = "p_1_1_m"


def generate_beach(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if check_for_water_around(layer, x, y, random.randint(3, 5)) and (x, y) not in layer.keys(): layer[(x, y)] = "p_4"


def check_for_water_around(layer, x, y, beachwidth):
    for around in range(0, (beachwidth + 2) ** 2):
        check_x = x + around % (beachwidth + 2) - beachwidth + 1
        check_y = y + around // (beachwidth + 2) - beachwidth + 1
        water_around = layer.get((check_x, check_y), "")
        if "pd_" in str(water_around): #or "p_4" in str(water_around):
            return True
    return False


def calculate_ponds(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if (x, y) in layer and (layer[(x, y)] == "pd_" or layer[(x, y)] == "b_"):
                pond = calculate_pond_look(layer, x, y)
                layer[(x, y)] = str(layer[(x, y)]) + str(pond)


def generate_ponds(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            tile_height = tile_Heights[(x, y)]
            if tile_height == 0:
                    layer[(x, y)] = "pd_"


def calculate_pond_look(layer, x, y):
    tiles_around = []
    for around in range(0, 9):
        path_around = (layer.get((x + (around % 3) - 1, y + math.floor(around / 3) - 1), "0"))
        if not "p_" in str(path_around) and ("pd_" in str(path_around) or "b_" in str(path_around) or "pl_" in str(path_around) or out_Of_Bounds(x + (around % 3) - 1, y + math.floor(around / 3) - 1)):
            tiles_around.append(1)
        else:
            tiles_around.append(0)
    if tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1:
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


def spawn_lapras(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if random.random() < 0.001 and check_availability_water(layer, x - 1, y - 1, 3, 4) and not layer["Lapras"]:
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
                layer[(x, y)] = "pd_l_" + str(direction)


def spawn_gyarados(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            shiny = 0
            if check_availability_water(layer, x - 1, y - 1, 4, 4) and random.random() < 0.001 and not layer["Gyarados"]:
                if random.random() < 0.02: shiny = 4
                layer["Gyarados"] = True
                layer[(x + 1, y)] = "pd_g_" + str(2 + shiny)
                layer[(x, y + 1)] = "pd_g_" + str(3 + shiny)
                layer[(x + 1, y + 1)] = "pd_g_" + str(4 + shiny)
                layer[(x, y)] = "pd_g_" + str(1 + shiny)


def spawn_mne(layer, spawn_rate, offset_x, offset_y):
    octaves = 3
    freq = 40
    off_x = offset_x
    off_y = offset_y
    for y in range(map_Size_Y):
        for x in range(map_Size_X):
            mne_biomes[(x, y)] = snoise2((x + off_x) / freq, (y + off_y) / freq, octaves) * 2

    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if not (x, y) in layer.keys() and not (x, y - 1) in layer.keys() and not (x, y - 2) in layer.keys() and not (x, y) in house_Tiles.keys() and not (x, y - 1) in house_Tiles.keys() and not (x, y - 2) in house_Tiles.keys():
                if mne_biomes[(x, y)] > 0 and random.random() < spawn_rate / 100:
                    layer[(x, y)] = "st_0"
                    layer[(x, y - 1)] = "st_1"
                    layer[(x, y - 2)] = "st_2"


def spawn_house(layer, house_type, house_size_x, house_size_y, amount):
    for houses in range(0, amount):
        house_x = random.randint(1, map_Size_X - house_size_y)
        house_y = random.randint(1, map_Size_Y - house_size_x)
        attempt = 0
        while not check_availability_zone(ground_Tiles, house_x, house_y, house_size_x + 1, house_size_y + 2) or not check_availability_zone(house_Tiles, house_x, house_y, house_size_x, house_size_y + 2) or not flat_surface(house_x - 3, house_y + 2, house_size_x + 6, house_size_y + 1):
            attempt += 1
            house_x = random.randint(1, map_Size_X - house_size_x)
            house_y = random.randint(1, map_Size_Y - house_size_y)
            if "h_" in layer.get((house_x, house_y), ""):
                house_x = find_lower_right(layer, house_x, house_y, house_size_y)[0]
                house_y = find_lower_right(layer, house_x, house_y, house_size_y)[1]
        for house_tile in range(1, house_size_x * house_size_y + 1):
            layer[(house_x + (house_tile - 1) % house_size_x, house_y  + math.floor((house_tile - 1) / house_size_x))] = "h_" + str(house_type) + "_" + str(house_tile)
        for front in range(4 * house_size_x):
            ground_Tiles[(house_x + front % house_size_x, house_y + math.floor(front / house_size_x) + house_size_y - 2)] = "p_3"
        houses_Connecters[len(houses_Connecters)] = {"Left_Connect": (house_x - 2, house_y + house_size_y), "Right_Connect": (house_x + house_size_x, house_y + house_size_y)}
        if random.randint(0, 1) == 1 and not taken(layer, house_x - 1, house_y + house_size_y - 2):
            layer[(house_x - 1, house_y + house_size_y - 1)] = "mbx_0"
            layer[(house_x - 1, house_y + house_size_y - 2)] = "mbx_1"


def flat_surface(x, y, x_size, y_size):
    reference_height = tile_Heights.get((x, y), -1)
    for tile in range(1, x_size * y_size + 1):
        if tile_Heights.get((x + (tile % x_size), y + (tile // x_size)), -1) != reference_height: return False

    return True



def find_lower_right(layer, x, y, size_y):
    while "h_" in layer.get((x - 1, y), "") or "h_" in layer.get((x, y - 1), ""):
        if "h_" in layer.get((x - 1, y), ""): y += 1
        if "h_" in layer.get((x, y - 1), ""): x += 1
    return (x, y - size_y)


def spawn_pokecenter(layer):
    house_x = random.randint(1, map_Size_X - 5)
    house_y = random.randint(1, map_Size_Y - 5)
    while not check_availability_zone(ground_Tiles, house_x - 1, house_y - 1, 5 + 1, 5 + 4) or not check_availability_zone(house_Tiles, house_x - 1, house_y - 1, 5 + 1, 5 + 4) or not flat_surface(house_x - 1, house_y + 1, 5 + 2, 5 + 2):
        house_x = random.randint(1, map_Size_X - 5)
        house_y = random.randint(1, map_Size_Y - 5)
    for house_tile in range(1, 5 * 5 + 1):
        layer[(
        house_x + (house_tile - 1) % 5, house_y + math.floor((house_tile - 1) / 5))] = "pc_" + str(house_tile)
    for front in range(4 * 5):
        ground_Tiles[(house_x + front % 5, house_y + math.floor(front / 5) + 5 - 2)] = "p_2"
    houses_Connecters[len(houses_Connecters)] = {"Left_Connect": (house_x - 2, house_y + 5), "Right_Connect": (house_x + 5, house_y + 5)}


def spawn_pokemarket(layer):
    house_x = random.randint(1, map_Size_X - 4)
    house_y = random.randint(1, map_Size_Y - 4)
    while not check_availability_zone(ground_Tiles, house_x - 1, house_y - 1, 4 + 1, 4 + 4) or not check_availability_zone(house_Tiles, house_x - 1, house_y - 1, 4 + 1, 4 + 4) or not flat_surface(house_x - 1, house_y + 1, 4 + 2, 4 + 2):
        house_x = random.randint(1, map_Size_X - 4)
        house_y = random.randint(1, map_Size_Y - 4)
    for house_tile in range(1, 4 * 4 + 1):
        layer[(
        house_x + (house_tile - 1) % 4, house_y + math.floor((house_tile - 1) / 4))] = "pm_" + str(house_tile)
    for front in range(4 * 4):
        ground_Tiles[(house_x + front % 4, house_y + math.floor(front / 4) + 4 - 2)] = "p_2"
    houses_Connecters[len(houses_Connecters)] = {"Left_Connect": (house_x - 2, house_y + 4), "Right_Connect": (house_x + 4, house_y + 4)}


def spawn_truck(layer):
    import math, random
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if random.random() < 0.05 and "p_" in ground_Tiles.get((x, y + 3), "") and "p_" in ground_Tiles.get((x + 2, y + 3), ""):
                if check_availability_zone(house_Tiles, x, y, 3, 3) and check_availability_zone(ground_Tiles, x, y, 3, 1) and flat_surface(x, y + 1, 3, 2) and not ground_Tiles["Truck"]:
                    for truck_tile in range(9):
                        layer[(x + truck_tile % 3, y + math.floor(truck_tile / 3))] = "t_" + str(truck_tile + 1)
                    ground_Tiles["Truck"] = True


def spawn_snorlax(layer):
    import math, random
    shiny = 0
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if ("b_" in ground_Tiles.get((x, y), "") or "pl_" in ground_Tiles.get((x, y), "")) and random.random() < 0.015:
                if check_bridge_space(ground_Tiles, x, y, 2, 2) and not ground_Tiles["Snorlax"]:
                    if random.random() < 0.02: shiny = 4
                    for snorlax_tile in range(4):
                        layer[(x + snorlax_tile % 2, y + math.floor(snorlax_tile / 2))] = "sn_" + str(snorlax_tile + 1 + shiny)
                        ground_Tiles["Snorlax"] = True


def spawn_pikachu(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if random.random() < 0.001 and layer.get((x, y), "") == "" and "pd_" not in ground_Tiles.get((x, y), "") and "m_" not in ground_Tiles.get((x, y), "") and not ground_Tiles["Pikachu"]:
                layer[(x, y)] = "pikachu_" + str(random.randint(1, 4))
                ground_Tiles["Pikachu"] = True


def spawn_exceguttor(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if random.random() < 0.001 and "p_4" in ground_Tiles.get((x, y), "") and not ground_Tiles["Exceguttor"]:
                shiny = 0
                if random.random() < 0.02: shiny = 2
                layer[(x, y)] = "exc_" + str(1 + shiny)
                layer[(x, y - 1)] = "exc_" + str(2 + shiny)
                ground_Tiles["Exceguttor"] = True


def spawn_lanterns(layer):
    import random
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if layer.get((x - 1, y), "") == "p_1_3" and random.random() < 0.05 and check_availability_zone(layer, x, y - 2, 2, 3):
                layer[(x, y)] = "l_1"
                layer[(x, y - 1)] = "l_2"
                layer[(x, y - 2)] = "l_3"
                layer[(x + 1, y)] = "l_4"
            if layer.get((x + 1, y), "") == "p_1_1" and random.random() < 0.05 and check_availability_zone(layer, x, y - 2, 1, 3):
                layer[(x, y)] = "l_5"
                layer[(x, y - 1)] = "l_6"
                layer[(x, y - 2)] = "l_7"


def spawn_fountain(layer):
    house_x = random.randint(1, map_Size_X - 5)
    house_y = random.randint(1, map_Size_Y - 5)
    while not check_availability_zone(ground_Tiles, house_x - 1, house_y - 1, 5, 5) or not check_availability_zone(house_Tiles, house_x - 1, house_y - 1, 5, 5) or not flat_surface(house_x - 2, house_y - 2, 5 + 2, 5 + 2):
        house_x = random.randint(1, map_Size_X - 5)
        house_y = random.randint(1, map_Size_Y - 5)

    for house_tile in range(1, 10):
        layer[(house_x + (house_tile - 1) % 3, house_y + math.floor((house_tile - 1) / 3) + 3)] = "f_" + str(house_tile)
    for front in range(25):
        ground_Tiles[(house_x - 1 + front % 5, (house_y - 1 + front // 5) + 5 - 2)] = "p_2"
    houses_Connecters[len(houses_Connecters)] = {"Left_Connect": (house_x - 2, house_y + 4), "Right_Connect": (house_x + 4, house_y + 4)}


def spawn_npc(layer, total_npcs, population, path_only):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            direction = random.randint(1, 4)
            if (x, y) not in layer.keys() and (x, y) not in house_Tiles.keys() and random.random() < 0.001 * population:
                npc_number = random.randint(1, total_npcs)
                if path_only:
                    if "p_" in ground_Tiles.get((x, y), ""): #or "b_" in ground_Tiles.get((x, y), ""):x
                        if npc_number not in off_Path_Npc: layer[(x, y)] = "npc_" + str(npc_number) + "_1"# + str(direction)
                        """
                        if random.random() < 0.5 and direction == 2:
                            if (x + 1, y) not in layer.keys() and (x + 1, y) not in house_Tiles.keys() and ("p_" in ground_Tiles.get((x + 1, y), "") or "b_" in ground_Tiles.get((x, y), "")):
                                layer[(x + 1, y)] = "npc_" + str(random.randint(1, total_npcs)) + "_4"
                        """
                elif random.randint(0, 4) == 0 and "m_" not in ground_Tiles.get((x, y), ""):
                    if "pd_" in ground_Tiles.get((x, y), ""):
                        npc_number = water_Npc[random.randint(1, len(water_Npc) - 1)]
                    elif "b_" in ground_Tiles.get((x, y), ""):
                        npc_number = bridge_Npc[random.randint(1, len(bridge_Npc) - 1)]
                    elif "p_" not in ground_Tiles.get((x, y), ""):
                        npc_number = outside_Npc[random.randint(1, len(outside_Npc) - 1)]
                    else:
                        while npc_number in off_Path_Npc:
                            npc_number = random.randint(1, total_npcs)
                    layer[(x, y)] = "npc_" + str(npc_number) + "_1" #+ str(direction)
                    """
                    if random.random() < 0.5 and direction == 2:
                        if (x + 1, y) not in layer.keys() and (x + 1, y) not in house_Tiles.keys():
                            layer[(x + 1, y)] = "npc_" + str(random.randint(1, total_npcs)) + "_4"
                    """


def check_bridge_space(layer, x, y, x_size, y_size):
    for bridge_tile in range(x_size * y_size):
        if "b_" not in layer.get((x + bridge_tile % x_size, y + math.floor(bridge_tile / x_size)), "") and not "pl_" in layer.get((x + bridge_tile % x_size, y + math.floor(bridge_tile / x_size)), ""):
            return False
    return True


def check_availability_zone(layer, start_x, start_y, x_size, y_size):
    availability = True
    for tile in range(x_size * y_size + 1):
        if (start_x + tile % x_size, start_y + (tile - 1) // x_size) in layer.keys() or out_Of_Bounds(start_x + tile % x_size, start_y + (tile - 1) // x_size): availability = False
    return availability


def check_availability_water(layer, start_x, start_y, x_size, y_size):
    availability = True
    for tile in range(x_size * y_size + 1):
        if not "pd_" in layer.get((start_x + tile % x_size, start_y + math.floor((tile - 1) / x_size)), ""): availability = False
    return availability


def generate_hills(layer, max_height, offset_x, offset_y):
    mountainize(tile_Heights, max_height, offset_x, offset_y)
    #finish_hills(layer)


def mountainize(layer, max_height, offset_x, offset_y):
    from math import floor
    octaves = 1
    freq = 100
    off_x = offset_x
    off_y = offset_y
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            tile_height = abs(floor((snoise2(round((x + off_x) / freq, 2), round((y + off_y) / freq, 2), octaves)) * max_height))
            layer[(x, y)] = tile_height



def generate_height_map(layer, height_list):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            layer[(x, y)] = "height_" + str(height_list[(x, y)])


def calculate_hill_texture(height_list, x, y):
    hills_around = test_hills_around(height_list, x, y)

    if height_list.get((x, y), 0) < 2: return -1

    if hills_around[3] == 0 and hills_around[6] == -1 and hills_around[7] == 0: return 9
    if hills_around[5] == 0 and hills_around[7] == 0 and hills_around[8] == -1: return 10
    if hills_around[0] == -1 and hills_around[1] == 0 and hills_around[3] == 0: return 4
    if hills_around[1] == 0 and hills_around[2] == -1 and hills_around[5] == 0: return 4

    if hills_around[1] == -1 and hills_around[3] == -1 and hills_around[5] == -1 and hills_around[7] == -1: return 15
    if hills_around[1] == -1 and hills_around[3] == 0 and hills_around[5] == -1 and hills_around[7] == -1: return 15
    if hills_around[1] == -1 and hills_around[3] == -1 and hills_around[5] == -1 and hills_around[7] == 0: return 15
    if hills_around[1] == -1 and hills_around[3] == -1 and hills_around[5] == 0 and hills_around[7] == -1: return 15
    if hills_around[1] == 0 and hills_around[3] == -1 and hills_around[5] == -1 and hills_around[7] == -1: return 15

    if hills_around[1] == 0 and hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == 0: return -1
    if hills_around[1] == 0 and hills_around[3] == -1 and hills_around[7] == 0: return 1
    if hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == -1: return 2
    if hills_around[1] == 0 and hills_around[5] == -1 and hills_around[7] == 0: return 3
    if hills_around[1] == -1 and hills_around[3] == 0 and hills_around[5] == 0: return 4
    if hills_around[1] == -1 and hills_around[3] == -1: return 5
    if hills_around[3] == -1 and hills_around[7] == -1: return 6
    if hills_around[5] == -1 and hills_around[7] == -1: return 7
    if hills_around[1] == -1 and hills_around[5] == -1: return 8
    return -1



def test_hills_around(height_list, x, y):
    current_tile_height = height_list[(x, y)]
    hills_around = []

    for around in range(0, 9):
        tile_coo = (x + around % 3 - 1, y + around // 3 - 1)
        if height_list.get(tile_coo, current_tile_height) == current_tile_height: hills_around.append(0)
        if height_list.get(tile_coo, current_tile_height) < current_tile_height: hills_around.append(-1)
        if height_list.get(tile_coo, current_tile_height) > current_tile_height: hills_around.append(1)

    return hills_around


def finish_hills(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            hill_texture = str(calculate_hill_texture(tile_Heights, x, y))
            if not hill_texture == "-1" and ((x, y) not in layer.keys() or "pd_" in layer.get((x, y), "")):
                layer[(x, y)] = "m_" + hill_texture


def generate_rain(layer, rain_rate, rain_chance):
    if random.randint(0, 100) < rain_chance:
        for x in range(0, map_Size_X):
            for y in range(0, map_Size_Y):
                if random.randint(0, 100) < rain_rate:
                    layer[(x, y)] = "r_" + str(random.randint(1, 2))
                elif (x, y) not in layer.keys():
                    layer[(x, y)] = "r_0"
        for x in range(0, map_Size_X):
            for y in range(0, map_Size_Y):
                if random.randint(0, 100) < rain_rate:
                    if not taken(house_Tiles, x, y) and not taken(decoration_Tiles, x, y) and not taken(npc_Layer, x, y) and "m_" not in ground_Tiles.get((x, y), "") and "pd_" not in ground_Tiles.get((x, y), "") and "l_" not in ground_Tiles.get((x, y), "") and "st" not in ground_Tiles.get((x, y), "") and "sne_" not in ground_Tiles.get((x, y), ""):
                        layer[(x, y)] = "r_" + str(random.randint(3, 5))


def render(layer, watermark):
    if watermark: add_watermark()
    correction = 0
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if (x, y) in layer.keys():
                tile = str(layer[(x, y)])
                if "npc_" in layer[(x, y)]: correction = 3
                try:
                    screen.blit(pygame.image.load(os.path.join("resources", tile + ".png")), (x * tile_Size, y * tile_Size - correction))
                except Exception as e:
                    screen.blit(pygame.image.load(os.path.join("resources", "missing.png")), (x * tile_Size, y * tile_Size - correction))
                    print(e)

    pygame.display.update()


def add_watermark():
    for amount in range(0, math.ceil(screen_Size_X / 48)):
        screen.blit(pygame.image.load(os.path.join("resources", "randemon watermark" + ".png")), (amount * 48, screen_Size_Y - 16))


tile_Size = 16
map_Size_X = 80 #get_int(10, 100, "Amount of tiles in x-direction")
map_Size_Y = 50 #get_int(10, 100, "Amount of tiles in y-direction")
screen_Size_X = tile_Size * map_Size_X
screen_Size_Y = tile_Size * map_Size_Y
sne_rate = 40 #get_int(0, 100, "Small size nature elements spawn rate")
mne_rate = 50 #get_int(0, 100, "Medium size nature elements spawn rate")

user_Path_Amount = 2 #get_int(0, 4, "Amount of paths to generate")
user_Path_Length = 25
#if user_Path_Amount != 0: user_Path_Length = get_int(1, 24, "Maximum length of a path")
x_offset = random.randint(0, 1000000)
y_offset = random.randint(0, 1000000)
x_Wallpapers = 1
y_Wallpapers = 1
friendshipgoals = x_Wallpapers * y_Wallpapers
"""
ground_Tiles = {"Lapras": False, "Diglet": False, "Gyarados": False, "Truck": False, "Snorlax": False, "Pikachu": False}
while not ground_Tiles["Lapras"] or not ground_Tiles["Gyarados"] or not ground_Tiles["Diglet"] or not ground_Tiles["Snorlax"]:
"""

for background in range(friendshipgoals):
    x_offset_friendship = x_offset + map_Size_X * (background % x_Wallpapers)
    y_offset_friendship = y_offset + map_Size_Y * (background // x_Wallpapers)
    ground_Tiles = {"Lapras": False, "Diglet": False, "Gyarados": False, "Truck": False, "Snorlax": False, "Pikachu": False, "Exceguttor": False}
    npc_Layer = {}
    tile_Heights = {}
    mne_biomes = {}
    house_Tiles = {}
    houses_Connecters = {}
    decoration_Tiles = {}
    rain = {}
    off_Path_Npc = [14, 15, 26, 27, 28, 29, 30, 31, 32, 36, 37, 38, 39, 49]
    water_Npc = [28, 29, 30]
    bridge_Npc = [31, 32, 36, 37, 38]
    outside_Npc = [14, 15, 26, 27, 39, 49]
    height_Tiles = {}
    generate_hills(ground_Tiles, 4, x_offset_friendship, y_offset_friendship)
    generate_ponds(ground_Tiles)

    #spawn_fountain(house_Tiles)
    spawn_house(house_Tiles, 1, 4, 4, 1)

    spawn_pokecenter(house_Tiles)
    spawn_pokemarket(house_Tiles)
    spawn_house(house_Tiles, 2, 5, 3, 1)
    spawn_house(house_Tiles, 3, 5, 4, 1)
    spawn_house(house_Tiles, 4, 4, 5, 1)
    spawn_house(house_Tiles, 5, 4, 7, 1)
    spawn_house(house_Tiles, 6, 5, 4, 1)
    spawn_house(house_Tiles, 7, 5, 4, 1)
    spawn_house(house_Tiles, 8, 4, 5, 1)
    spawn_house(house_Tiles, 9, 6, 4, 1)
    generate_path(ground_Tiles, "1", 2)
    spawn_truck(house_Tiles)
    generate_beach(ground_Tiles)
    calculate_paths(ground_Tiles)
    finish_hills(ground_Tiles)
    calculate_ponds(ground_Tiles)
    spawn_lapras(ground_Tiles)
    spawn_gyarados(ground_Tiles)
    spawn_snorlax(house_Tiles)
    spawn_pikachu(house_Tiles)
    spawn_exceguttor(house_Tiles)
    spawn_lanterns(ground_Tiles)
    spawn_mne(ground_Tiles, mne_rate, x_offset_friendship, y_offset_friendship)
    spawn_npc(npc_Layer, 55, 30, False)
    fill_up_grass(ground_Tiles, sne_rate, x_offset_friendship, y_offset_friendship)
    finish_hills(ground_Tiles)
    generate_rain(rain, 20, 10)

    screen = pygame.display.set_mode((screen_Size_X, screen_Size_Y))

    generate_height_map(height_Tiles, tile_Heights)
    render(height_Tiles, False)
    sleep(0.5)

    render(ground_Tiles, False)
    render(decoration_Tiles, False)
    render(house_Tiles, False)
    render(npc_Layer, False)

    render(rain, False)

    if friendshipgoals > 1:
        if background < 10:
            background_Number = "0" + str(background)
        else:
            background_Number = background
        pygame.image.save(screen, os.path.join("saved images", str(background_Number) + ".png"))

if friendshipgoals == 1:
    save = input("Save this image? (y/n/seed): ")
    while save == "seed" or save == "zaad":
        print(seed)
        save = input("Save this image? (y/n/seed): ")
    t = datetime.datetime.now().strftime("%G-%m-%d %H-%M-%S")
    if save == "y":
        pygame.image.save(screen, os.path.join("saved images", t+".png"))
        print("HOERA")
#sideways diagonal stairs (in src folder) are from pokemon gaia version (sta_2, sta_4, sta_5, sta_7)
