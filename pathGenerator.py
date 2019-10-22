import math


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
        return "p_" in pmap.ground_layer.get((x, y), "") and "p_4" not in pmap.ground_layer.get((x, y), "")
    except Exception as e:
        print(e)
        print(pmap.ground_layer.get((x, y), ""))


def generate_dijkstra_path(pmap, house_path_type):
    import sys

    PATH_WEIGHT = 1
    GRASS_WEIGHT = 3
    HILL_WEIGHT = 20
    WATER_WEIGHT = 40

    def initialize_dijkstra():
        for y in range(pmap.height):
            current_weight.append(pmap.width * [sys.maxsize])
            weight.append(weight_array[y])
            visited.append(pmap.width * [False])
            previous_tile.append(pmap.width * [(0, 0)])

    def determine_weight(x, y):
        if "h_" in pmap.buildings.get((x - 1, y), "") or "pm_" in pmap.buildings.get((x - 1, y),  "") or "pc_" in pmap.buildings.get((x - 1, y), ""): return 999999
        if "h_" in pmap.buildings.get((x, y), "") and ("h_" in pmap.buildings.get((x, y + 1), "") or "h_" in pmap.buildings.get((x, y - 1), "")) or "h_" in pmap.buildings.get((x, y - 1), ""): return 999999
        if "pm_" in pmap.buildings.get((x, y), "") and ("pm_" in pmap.buildings.get((x, y + 1), "") or "pm_" in pmap.buildings.get((x, y - 1), "")): return 999999
        if "pc_" in pmap.buildings.get((x, y), "") and ("pc_" in pmap.buildings.get((x, y + 1), "") or "pc_" in pmap.buildings.get((x, y - 1), "")): return 999999
        if "m_" in pmap.ground_layer.get((x, y), "") or "m_" in pmap.ground_layer.get((x - 1, y), "") or "m_" in pmap.ground_layer.get((x, y - 1), "") or "m_" in pmap.ground_layer.get((x - 1, y - 1), ""): return HILL_WEIGHT
        if "pd_" in pmap.ground_layer.get((x, y), "") or "pd_" in pmap.ground_layer.get((x - 1, y), "") or "pd_" in pmap.ground_layer.get((x, y - 1), "") or "pd_" in pmap.ground_layer.get((x - 1, y - 1), ""): return WATER_WEIGHT
        if is_actual_path(pmap, x, y) or "b_" in pmap.ground_layer.get((x, y), "") or "mrk" in pmap.ground_layer.get((x, y), ""): return PATH_WEIGHT
        if pmap.ground_layer.get((x, y), "") == "" or "p_4" in pmap.ground_layer.get((x, y), ""): return GRASS_WEIGHT
        return 999999

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


    weight_array = {}
    for y in range(pmap.height):
        weight_array_row = []
        for x in range(pmap.width):
            weight_array_row.append(determine_weight(x, y))
        weight_array[y] = weight_array_row

    for front_door in range(len(pmap.front_doors) - 1):
        current_tile = pmap.front_doors[front_door]
        if not current_tile: print("godverdomme kutzooi")
        target_tile = pmap.front_doors[front_door + 1]
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
        make_path_double(pmap, path, house_path_type)
        create_bridges(pmap)

    # fixit(ground_Tiles)


def make_path_double(pmap, path, house_path_type):
    path_extention = []
    for (x, y) in path:
        if "p_" not in pmap.ground_layer.get((x, y - 1), ""): path_extention.append((x, y - 1))
        if "p_" not in pmap.ground_layer.get((x - 1, y), ""): path_extention.append((x - 1, y))
        if "p_" not in pmap.ground_layer.get((x - 1, y - 1), ""): path_extention.append((x - 1, y - 1))

    for (x, y) in path_extention:
        if pmap.tile_heights.get((x, y), 0) < 1:
            pmap.ground_layer[(x, y)] = "b_"
        elif "p_" not in pmap.ground_layer.get((x, y), ""): pmap.ground_layer[(x, y)] = house_path_type


def create_bridges(pmap):
    for (x, y) in pmap.ground_layer.keys():
        if pmap.ground_layer.get((x, y), "") == "b_":
            if "pd_" in pmap.ground_layer.get((x, y - 1), ""):
                pmap.ground_layer[(x, y)] = "b_1"
                pmap.ground_layer[(x, y + 1)] = "b_2"
            if "pd_" in pmap.ground_layer.get((x, y + 1), ""):
                pmap.ground_layer[(x, y)] = "b_2"
                pmap.ground_layer[(x, y - 1)] = "b_1"
            if "pd_" in pmap.ground_layer.get((x - 1, y), ""):
                pmap.ground_layer[(x, y)] = "b_3"
                pmap.ground_layer[(x + 1, y)] = "b_4"
            if "pd_" in pmap.ground_layer.get((x + 1, y), ""):
                pmap.ground_layer[(x, y)] = "b_4"
                pmap.ground_layer[(x - 1, y)] = "b_3"

        if "b_" in pmap.ground_layer.get((x, y - 1), "") and "pd_" in pmap.ground_layer.get((x, y), ""):
            pmap.decoration_layer[(x, y)] = "bu_0"

    for (x, y) in pmap.ground_layer.keys():
        if pmap.ground_layer.get((x, y), "") == "b_":
            if "b_" in pmap.ground_layer.get((x - 1, y), ""):
                pmap.ground_layer[(x, y)] = pmap.ground_layer[(x - 1, y)]
            if "b_" in pmap.ground_layer.get((x, y - 1), ""):
                pmap.ground_layer[(x, y)] = pmap.ground_layer[(x, y - 1)]
