import math

PATH_WEIGHT = 1
GRASS_WEIGHT = 4
HILL_WEIGHT = 64
WATER_WEIGHT = 32


def apply_path_sprites(pmap):
    def calculate_path_sprite(x, y):
        tiles_around = []
        for around in range(0, 9):
            path_around = pmap.ground_layer.get((x + (around % 3) - 1, y + math.floor(around / 3) - 1), 0)
            # if path_around == 0: path_around = pmap.buildings.get((x + (around % 3) - 1, y + math.floor(around / 3) - 1), 0)
            if "p_" in str(path_around) or "b_" in str(path_around) or "pl_" in str(path_around) or "sta_" in str(
                    path_around) or "m_4_p" in str(path_around) or "pd_" in str(path_around) or pmap.out_of_bounds(
                    x + (around % 3) - 1, y + math.floor(around / 3) - 1) or "mrk" in str(path_around):
                tiles_around.append(1)
            else:
                tiles_around.append(0)
        if tiles_around == [1, 1, 1, 1, 1, 1, 0, 1, 1]:
            return "_9"
        elif tiles_around == [1, 1, 1, 1, 1, 1, 1, 1, 0]:
            return "_10"
        elif tiles_around == [1, 1, 0, 1, 1, 1, 1, 1, 1]:
            return "_11"
        elif tiles_around == [0, 1, 1, 1, 1, 1, 1, 1, 1]:
            return "_12"
        elif tiles_around == [1, 1, 1, 1, 1, 1, 1, 1, 1] or (
                tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1):
            return "_0"
        elif tiles_around == [0, 1, 1, 0, 1, 1, 0, 1, 1] or tiles_around == [1, 1, 1, 0, 1, 1, 0, 1,
                                                                             1] or tiles_around == [0, 1, 1, 0, 1, 1, 1,
                                                                                                    1,
                                                                                                    1] or tiles_around == [
            1, 1, 1, 0, 1, 1, 1, 1, 1]:
            return "_1"
        elif tiles_around == [1, 1, 1, 1, 1, 1, 0, 0, 0] or tiles_around == [1, 1, 1, 1, 1, 1, 1, 0,
                                                                             0] or tiles_around == [1, 1, 1, 1, 1, 1, 0,
                                                                                                    0,
                                                                                                    1] or tiles_around == [
            1, 1, 1, 1, 1, 1, 1, 0, 1]:
            return "_2"
        elif tiles_around == [1, 1, 0, 1, 1, 0, 1, 1, 0] or tiles_around == [1, 1, 1, 1, 1, 0, 1, 1,
                                                                             0] or tiles_around == [1, 1, 0, 1, 1, 0, 1,
                                                                                                    1,
                                                                                                    1] or tiles_around == [
            1, 1, 1, 1, 1, 0, 1, 1, 1]:
            return "_3"
        elif tiles_around == [0, 0, 0, 1, 1, 1, 1, 1, 1] or tiles_around == [1, 0, 0, 1, 1, 1, 1, 1,
                                                                             1] or tiles_around == [0, 0, 1, 1, 1, 1, 1,
                                                                                                    1,
                                                                                                    1] or tiles_around == [
            1, 0, 1, 1, 1, 1, 1, 1, 1]:
            return "_4"
        elif tiles_around[5] == 1 and tiles_around[7] == 1 and tiles_around[8] == 1:
            return "_5"
        elif tiles_around[1] == 1 and tiles_around[2] == 1 and tiles_around[5] == 1:
            return "_6"
        elif tiles_around[0] == 1 and tiles_around[1] == 1 and tiles_around[3] == 1:
            return "_7"
        elif tiles_around[3] == 1 and tiles_around[6] == 1 and tiles_around[7] == 1:
            return "_8"
        return "_er"

    for x in range(0, pmap.width):
        for y in range(0, pmap.height):
            if (x, y) in pmap.ground_layer and "p_" in pmap.ground_layer[(x, y)]:
                path = calculate_path_sprite(x, y)
                if not path == "_er":
                    pmap.ground_layer[(x, y)] = str(pmap.ground_layer[(x, y)]) + str(path)
                else:
                    pmap.ground_layer[(x, y)] = "g_0"

    # finish_path_edges(decoration_Tiles)


def is_actual_path(pmap, x, y):
    try:
        return ("p_" in pmap.ground_layer.get((x, y), "") or "sta_" in pmap.ground_layer.get((x, y), "")) and "p_4" not in pmap.ground_layer.get((x, y), "")
    except Exception as e:
        print(e)
        print(pmap.ground_layer.get((x, y), ""))


def generate_dijkstra_path(pmap, house_path_type):
    import sys

    def initialize_dijkstra():
        for y in range(pmap.height):
            current_weight.append(pmap.width * [sys.maxsize])
            weight.append(weight_array[y])
            visited.append(pmap.width * [False])
            previous_tile.append(pmap.width * [(0, 0)])

    def handle_current_tile():
        current_x = current_tile[0]
        current_y = current_tile[1]
        visited[current_y][current_x] = True
        for tile_around in range(4):
            around_x = current_x - 1 + ((2 * tile_around) + 1) % 3
            around_y = current_y - 1 + ((2 * tile_around) + 1) // 3
            if not pmap.out_of_bounds(around_x, around_y):
                new_weight = current_weight[current_y][current_x] + weight[around_y][around_x]
                if not visited[around_y][around_x] and current_weight[around_y][around_x] > new_weight:
                    current_weight[around_y][around_x] = new_weight
                    previous_tile[around_y][around_x] = current_tile
                    handle_tiles[(around_x, around_y)] = new_weight
        handle_tiles.pop(current_tile)

    def find_min_tile():
        min_weight = sys.maxsize
        for tile in handle_tiles:
            if handle_tiles[tile] < min_weight:
                min_weight = handle_tiles[tile]
                min_tile = tile
        try:
            return min_tile
        except Exception as e:
            print(e)

    def find_closest_house(x, y):
        closest_distance = 999999
        closest_house = (x, y)
        for house in already_connected:
            if house != (x, y):
                if abs(house[0] - x) + abs(house[1] - y) < closest_distance:
                    closest_distance = abs(house[0] - x) + abs(house[1] - y)
                    closest_house = house
        return closest_house

    weight_array = {}
    for y in range(pmap.height):
        weight_array_row = []
        for x in range(pmap.width):
            weight_array_row.append(determine_weight(pmap, x, y))
        weight_array[y] = weight_array_row

    already_connected = set()
    for front_door in range(len(pmap.front_doors)):
        current_tile = pmap.front_doors[front_door]
        already_connected.add(current_tile)
        if not current_tile: print("broken")
        target_tile = find_closest_house(current_tile[0], current_tile[1])
        already_connected.add(target_tile)
        weight = []
        current_weight = []
        visited = []
        previous_tile = []
        handle_tiles = {}
        initialize_dijkstra()

        visited[current_tile[1]][current_tile[0]] = True
        current_weight[current_tile[1]][current_tile[0]] = 0
        previous_tile[current_tile[1]][current_tile[0]] = (0, 0)
        handle_tiles[(current_tile[0], current_tile[1])] = 0
        handle_current_tile()
        while not current_tile == target_tile:
            current_tile = find_min_tile()
            handle_current_tile()

        path = []
        while not previous_tile[current_tile[1]][current_tile[0]] == (0, 0):
            path.append(current_tile)
            if "p_" not in pmap.ground_layer.get((current_tile[0], current_tile[1]), ""):
                weight_array[current_tile[1]][current_tile[0]] = PATH_WEIGHT
                if "pd_" not in pmap.ground_layer.get((current_tile[0], current_tile[1]), "") and "b_" not in pmap.ground_layer.get((current_tile[0], current_tile[1]), ""):
                    pmap.ground_layer[current_tile] = house_path_type
            current_tile = previous_tile[current_tile[1]][current_tile[0]]

        path.append(current_tile)
        make_path_double(pmap, path, house_path_type)

    create_stairs(pmap, house_path_type, weight_array)
    create_bridges(pmap)

    # fixit(ground_Tiles)


def determine_weight(pmap, x, y):
    if "h_" in pmap.buildings.get((x - 1, y), "") or "pm_" in pmap.buildings.get((x - 1, y),  "") or "pc_" in pmap.buildings.get((x - 1, y), ""): return 999999
    if "h_" in pmap.buildings.get((x, y), "") or "h_" in pmap.buildings.get((x, y - 1), "") or "h_" in pmap.buildings.get((x - 1, y - 1), ""): return 999999
    if "pm_" in pmap.buildings.get((x, y), "") or "pm_" in pmap.buildings.get((x, y - 1), "") or "pm_" in pmap.buildings.get((x - 1, y - 1), ""): return 999999
    if "pc_" in pmap.buildings.get((x, y), "") or "pc_" in pmap.buildings.get((x, y - 1), "") or "pc_" in pmap.buildings.get((x - 1, y - 1), ""): return 999999
    if "sta_3_0" == pmap.ground_layer.get((x, y), "") or "sta_6_0" == pmap.ground_layer.get((x, y), ""): return PATH_WEIGHT
    if "sta_1_1" == pmap.ground_layer.get((x, y), "") or "sta_8_1" == pmap.ground_layer.get((x, y), ""): return PATH_WEIGHT
    if "sta_6" in pmap.ground_layer.get((x, y - 1), "") or "sta_6" in pmap.ground_layer.get((x, y + 1), "") or "sta_3" in pmap.ground_layer.get((x, y - 1), "") or "sta_3" in pmap.ground_layer.get((x, y + 1), ""): return 999999
    if "sta_8" in pmap.ground_layer.get((x - 1, y), "") or "sta_8" in pmap.ground_layer.get((x + 1, y), "") or "sta_1" in pmap.ground_layer.get((x - 1, y), "") or "sta_1" in pmap.ground_layer.get((x + 1, y), ""): return 999999
    if "m_" in pmap.ground_layer.get((x, y), ""): return HILL_WEIGHT
    if "m_" in pmap.ground_layer.get((x - 1, y), "") or "m_" in pmap.ground_layer.get((x, y - 1), "") or "m_" in pmap.ground_layer.get((x - 1, y - 1), ""): return round(HILL_WEIGHT / 2)
    if "pd_" in pmap.ground_layer.get((x, y), "") or "pd_" in pmap.ground_layer.get((x - 1, y), "") or "pd_" in pmap.ground_layer.get((x, y - 1), "") or "pd_" in pmap.ground_layer.get((x - 1, y - 1), ""): return WATER_WEIGHT
    if is_actual_path(pmap, x, y) or "b_" in pmap.ground_layer.get((x, y), "") or "mrk" in pmap.ground_layer.get((x, y), ""): return PATH_WEIGHT
    if pmap.ground_layer.get((x, y), "") == "" or "p_4" in pmap.ground_layer.get((x, y), ""): return GRASS_WEIGHT
    return 999999


def update_weight(pmap, weight, x1, y1, x2, y2):
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            if not pmap.out_of_bounds(x, y):
                weight[y][x] = determine_weight(pmap, x, y)


def make_path_double(pmap, path, house_path_type):
    path_extention = []
    for (x, y) in path:
        if "p_" not in pmap.ground_layer.get((x, y - 1), ""): path_extention.append((x, y - 1))
        if "p_" not in pmap.ground_layer.get((x - 1, y), ""): path_extention.append((x - 1, y))
        if "p_" not in pmap.ground_layer.get((x - 1, y - 1), ""): path_extention.append((x - 1, y - 1))

    for (x, y) in path_extention:
        if pmap.tile_heights.get((x, y), 0) < 1:
            pmap.ground_layer[(x, y)] = "b_"
        elif "p_" not in pmap.ground_layer.get((x, y), ""):
            pmap.ground_layer[(x, y)] = house_path_type


def create_bridges(pmap):
    for y in range(pmap.height):
        for x in range(pmap.width):
            if pmap.ground_layer.get((x, y), "") == "b_":
                if "pd_" in pmap.ground_layer.get((x, y - 1), ""):
                    pmap.ground_layer[(x, y)] = "b_1"
                    pmap.ground_layer[(x, y + 1)] = "b_2"
                elif "pd_" in pmap.ground_layer.get((x, y + 1), ""):
                    pmap.ground_layer[(x, y)] = "b_2"
                    pmap.ground_layer[(x, y - 1)] = "b_1"
                elif "pd_" in pmap.ground_layer.get((x - 1, y), ""):
                    pmap.ground_layer[(x, y)] = "b_3"
                    pmap.ground_layer[(x + 1, y)] = "b_4"
                elif "pd_" in pmap.ground_layer.get((x + 1, y), ""):
                    pmap.ground_layer[(x, y)] = "b_4"
                    pmap.ground_layer[(x - 1, y)] = "b_3"
                else:
                    pmap.ground_layer[(x, y)] = "p_4"

            if "b_" in pmap.ground_layer.get((x, y - 1), "") and "pd_" in pmap.ground_layer.get((x, y), ""):
                pmap.decoration_layer[(x, y)] = "bu_0"


def create_stairs(pmap, house_path_type, weight_array):

    def path_above(x, y):
        return is_actual_path(pmap, x, y - 1)

    def path_under(x, y):
        return is_actual_path(pmap, x, y + 1)

    def path_left(x, y):
        return is_actual_path(pmap, x - 1, y)

    def path_right(x, y):
        return is_actual_path(pmap, x + 1, y)

    def smooth_path_height(path_type):
        for y in range(pmap.height):
            for x in range(pmap.width):
                current_height = 0
                if path_type in pmap.ground_layer.get((x, y), ""):
                    if path_under(x, y) and not path_above(x, y):
                        for smooth_y in range(y, y + 2):
                            current_height = max(current_height, pmap.tile_heights.get((x, smooth_y), current_height))
                        for smooth_y in range(y - 1, y + 3):
                            pmap.tile_heights[(x, smooth_y)] = max(current_height, pmap.tile_heights.get((x, smooth_y), current_height))
                        current_height = 0
                        update_weight(pmap, weight_array, x, y - 1, x, y + 3)

                    if path_above(x, y) and not path_under(x, y):
                        for smooth_y in range(y - 1, y + 1):
                            current_height = max(current_height, pmap.tile_heights.get((x, smooth_y), current_height))
                        for smooth_y in range(y - 2, y + 2):
                            pmap.tile_heights[(x, smooth_y)] = max(current_height, pmap.tile_heights.get((x, smooth_y), current_height))
                        current_height = 0
                        update_weight(pmap, weight_array, x, y - 2, x, y + 2)

                    if path_right(x, y) and not path_left(x, y):
                        for smooth_x in range(x, x + 2):
                            current_height = max(current_height, pmap.tile_heights.get((smooth_x, y), current_height))
                        for smooth_x in range(x - 1, x + 3):
                            pmap.tile_heights[(smooth_x, y)] = max(current_height, pmap.tile_heights.get((smooth_x, y), current_height))
                        current_height = 0
                        update_weight(pmap, weight_array, x - 1, y, x + 3, y)

                    if path_left(x, y) and not path_right(x, y):
                        for smooth_x in range(x - 1, x + 1):
                            current_height = max(current_height, pmap.tile_heights.get((smooth_x, y), current_height))
                        for smooth_x in range(x - 2, x + 2):
                            pmap.tile_heights[(smooth_x, y)] = max(current_height, pmap.tile_heights.get((smooth_x, y), current_height))
                        update_weight(pmap, weight_array, x - 2, y, x + 2, y)

                    current_height = pmap.tile_heights.get((x, y), 0)
                    if path_above(x, y) and path_left(x, y) and not path_under(x, y) and not path_right(x, y):
                        pmap.tile_heights[(x + 1, y + 1)] = max(current_height, pmap.tile_heights.get((x + 1, y + 1), 0))
                    if path_above(x, y) and path_right(x, y) and not path_under(x, y) and not path_left(x, y):
                        pmap.tile_heights[(x - 1, y + 1)] = max(current_height, pmap.tile_heights.get((x - 1, y + 1), 0))
                    if path_under(x, y) and path_left(x, y) and not path_above(x, y) and not path_right(x, y):
                        pmap.tile_heights[(x + 1, y - 1)] = max(current_height, pmap.tile_heights.get((x + 1, y - 1), 0))
                    if path_under(x, y) and path_right(x, y) and not path_above(x, y) and not path_left(x, y):
                        pmap.tile_heights[(x - 1, y - 1)] = max(current_height, pmap.tile_heights.get((x - 1, y - 1), 0))

    smooth_path_height(house_path_type)

    for path_y in range(pmap.height):
        for path_x in range(pmap.width):
            if "p_" in pmap.ground_layer.get((path_x, path_y), ""):
                if path_above(path_x, path_y) and path_under(path_x, path_y) and (path_left(path_x, path_y) or path_right(path_x, path_y)):
                    if pmap.tile_heights.get((path_x, path_y), 0) > pmap.tile_heights.get((path_x, path_y - 1), 0):
                        pmap.ground_layer[(path_x, path_y)] = "sta_8_0"
                        pmap.ground_layer[(path_x + 1, path_y)] = "sta_8_1"

                    elif pmap.tile_heights.get((path_x, path_y), 0) > pmap.tile_heights.get((path_x, path_y + 1), 0):
                        pmap.ground_layer[(path_x, path_y)] = "sta_1_0"
                        pmap.ground_layer[(path_x + 1, path_y)] = "sta_1_1"

                elif path_left(path_x, path_y) and path_right(path_x, path_y) and path_under(path_x, path_y):
                    if pmap.tile_heights.get((path_x, path_y), 0) > pmap.tile_heights.get((path_x - 1, path_y), 0):
                        pmap.ground_layer[(path_x, path_y)] = "sta_3_1"
                        pmap.ground_layer[(path_x, path_y + 1)] = "sta_3_0"

                    elif pmap.tile_heights.get((path_x, path_y), 0) > pmap.tile_heights.get((path_x + 1, path_y), 0):
                        pmap.ground_layer[(path_x, path_y)] = "sta_6_1"
                        pmap.ground_layer[(path_x, path_y + 1)] = "sta_6_0"


def create_lanterns(pmap):
    from random import random

    def check_availability_zone(x1, y1, x2, y2):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if (x, y) in pmap.ground_layer.keys() or (x, y) in pmap.buildings.keys() or (x, y) in pmap.decoration_layer.keys():
                    return False
        return True

    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            if is_actual_path(pmap, x - 1, y) and (x - 1, y) not in pmap.buildings.keys():
                if random() < 0.05 and check_availability_zone(x, y - 2, x + 2, y + 1):
                    pmap.decoration_layer[(x, y)] = "l_1"
                    pmap.decoration_layer[(x, y - 1)] = "l_2"
                    pmap.decoration_layer[(x, y - 2)] = "l_3"
                    pmap.decoration_layer[(x + 1, y)] = "l_4"
            if is_actual_path(pmap, x + 1, y) and (x + 1, y) not in pmap.buildings.keys():
                if random() < 0.05 and check_availability_zone(x, y - 2, x, y + 1):
                    pmap.decoration_layer[(x, y)] = "l_5"
                    pmap.decoration_layer[(x, y - 1)] = "l_6"
                    pmap.decoration_layer[(x, y - 2)] = "l_7"

