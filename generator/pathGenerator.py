from sys import maxsize

PATH_WEIGHT = 1
GRASS_WEIGHT = 8
HILL_WEIGHT = 32
WATER_WEIGHT = 32


def get_path_type(pmap, x, y):
    try:
        if pmap.get_tile_type("ground_layer", x, y) == "pa":
            return pmap.get_tile("ground_layer", x, y)[2] // 3
        else:
            return None
    except IndexError:
        pass


def apply_path_sprites(pmap):
    def calculate_path_sprite(x, y, path_type):
        tiles_around = []
        for around in range(0, 9):
            path_around = pmap.get_tile_type("ground_layer", x + around % 3 - 1, y + around // 3 - 1)
            if "pa" == path_around or "ro" == path_around:
                tiles_around.append(1)
                if (x, y) not in pmap.buildings.keys() and is_actual_path(pmap, x, y) and get_path_type(pmap, x + around % 3 - 1, y + around // 3 - 1) == 3:
                    pmap.decoration_layer[(x, y)] = ("de", 6, 3)
            else:
                tiles_around.append(0)

        if tiles_around == [1, 1, 1, 1, 1, 1, 0, 1, 1]:
            return "pa", 2, 2 + 3 * path_type
        elif tiles_around == [1, 1, 1, 1, 1, 1, 1, 1, 0]:
            return "pa", 1, 2 + 3 * path_type
        elif tiles_around == [1, 1, 0, 1, 1, 1, 1, 1, 1]:
            return "pa", 3, 2 + 3 * path_type
        elif tiles_around == [0, 1, 1, 1, 1, 1, 1, 1, 1]:
            return "pa", 4, 2 + 3 * path_type
        elif tiles_around == [1, 1, 1, 1, 1, 1, 1, 1, 1] or (tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1):
            return "pa", 0, 0 + 3 * path_type
        elif tiles_around == [0, 1, 1, 0, 1, 1, 0, 1, 1] or tiles_around == [1, 1, 1, 0, 1, 1, 0, 1, 1] or tiles_around == [0, 1, 1, 0, 1, 1, 1, 1, 1] or tiles_around == [1, 1, 1, 0, 1, 1, 1, 1, 1]:
            return "pa", 1, 0 + 3 * path_type
        elif tiles_around == [1, 1, 1, 1, 1, 1, 0, 0, 0] or tiles_around == [1, 1, 1, 1, 1, 1, 1, 0, 0] or tiles_around == [1, 1, 1, 1, 1, 1, 0, 0, 1] or tiles_around == [1, 1, 1, 1, 1, 1, 1, 0, 1]:
            return "pa", 4, 0 + 3 * path_type
        elif tiles_around == [1, 1, 0, 1, 1, 0, 1, 1, 0] or tiles_around == [1, 1, 1, 1, 1, 0, 1, 1, 0] or tiles_around == [1, 1, 0, 1, 1, 0, 1, 1, 1] or tiles_around == [1, 1, 1, 1, 1, 0, 1, 1, 1]:
            return "pa", 2, 0 + 3 * path_type
        elif tiles_around == [0, 0, 0, 1, 1, 1, 1, 1, 1] or tiles_around == [1, 0, 0, 1, 1, 1, 1, 1, 1] or tiles_around == [0, 0, 1, 1, 1, 1, 1, 1, 1] or tiles_around == [1, 0, 1, 1, 1, 1, 1, 1, 1]:
            return "pa", 3, 0 + 3 * path_type
        elif tiles_around[5] == 1 and tiles_around[7] == 1 and tiles_around[8] == 1:
            return "pa", 3, 1 + 3 * path_type
        elif tiles_around[1] == 1 and tiles_around[2] == 1 and tiles_around[5] == 1:
            return "pa", 1, 1 + 3 * path_type
        elif tiles_around[0] == 1 and tiles_around[1] == 1 and tiles_around[3] == 1:
            return "pa", 2, 1 + 3 * path_type
        elif tiles_around[3] == 1 and tiles_around[6] == 1 and tiles_around[7] == 1:
            return "pa", 4, 1 + 3 * path_type
        return "na", 0, 0

    for x in range(0, pmap.width):
        for y in range(0, pmap.height):
            try:
                path_type = pmap.get_tile("ground_layer", x, y)[2] // 3
                if "pa" == pmap.get_tile_type("ground_layer", x, y):
                    pmap.ground_layer[(x, y)] = calculate_path_sprite(x, y, path_type)
            except TypeError:
                pass
            except IndexError:
                pass


def is_actual_path(pmap, x, y):
    try:
        return ("pa" == pmap.get_tile_type("ground_layer", x, y) or "ro" == pmap.get_tile_type("ground_layer", x, y)) and get_path_type(pmap, x, y) != 3
    except Exception as e:
        print(e)


def generate_dijkstra_path(pmap, house_path_type):

    def initialize_dijkstra():
        for y in range(pmap.height):
            current_weight.append(pmap.width * [maxsize])
            weight.append(weight_array[y])
            visited.append(pmap.width * [False])
            previous_tile.append(pmap.width * [(0, 0)])

    def handle_current_tile():
        curr_x = current_tile[0]
        curr_y = current_tile[1]
        visited[curr_y][curr_x] = True
        for around_x, around_y in [(curr_x, curr_y - 1), (curr_x, curr_y + 1), (curr_x - 1, curr_y), (curr_x + 1, curr_y)]:
            if not pmap.out_of_bounds(around_x, around_y):
                new_weight = current_weight[curr_y][curr_x] + weight[around_y][around_x]
                if not visited[around_y][around_x] and current_weight[around_y][around_x] > new_weight:
                    current_weight[around_y][around_x] = new_weight
                    previous_tile[around_y][around_x] = current_tile
                    handle_tiles[(around_x, around_y)] = new_weight
        handle_tiles.pop(current_tile)

    def find_min_tile():
        min_weight = maxsize
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
        if pmap.tile_heights.get(current_tile, -1) > pmap.highest_path:
            pmap.highest_path = pmap.tile_heights[current_tile]
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
        while not current_tile == target_tile and current_weight[current_tile[1]][current_tile[0]] < 1999999:
            current_tile = find_min_tile()
            handle_current_tile()

        if current_weight[current_tile[1]][current_tile[0]] < 1999999:
            path = set()
            while not previous_tile[current_tile[1]][current_tile[0]] == (0, 0):
                path.add(current_tile)
                if "p_" not in pmap.ground_layer.get((current_tile[0], current_tile[1]), ""):
                    weight_array[current_tile[1]][current_tile[0]] = PATH_WEIGHT
                current_tile = previous_tile[current_tile[1]][current_tile[0]]
            path.add(current_tile)

            make_path_double(pmap, path, house_path_type)

    create_stairs(pmap)
    create_bridges(pmap)


def determine_weight(pmap, x, y, avoid_hill_corners=True):

    def is_corner(x, y):
        if pmap.get_tile_type("ground_layer", x, y) == "hi" and pmap.get_tile("ground_layer", x, y)[2] in [1, 3]:
            return True
        elif pmap.get_tile("ground_layer", x, y) == ("hi", 3, 0) and pmap.get_tile_type("ground_layer", x, y - 1) == "hi":
            return True
        else:
            return False

    if "ho" == pmap.get_tile_type("buildings", x, y) or "ho" == pmap.get_tile_type("buildings", x - 1, y) or "ho" == pmap.get_tile_type("buildings", x, y - 1) or "ho" == pmap.get_tile_type("buildings", x - 1, y - 1):return 999999
    if "fe" == pmap.get_tile_type("secondary_ground", x, y) or "fe" == pmap.get_tile_type("secondary_ground", x - 1, y) or "fe" == pmap.get_tile_type("secondary_ground", x, y - 1): return 999999
    if pmap.get_tile_type("ground_layer", x, y) == "ro": return PATH_WEIGHT
    if pmap.get_tile_type("ground_layer", x, y - 1) == "ro": return 999999
    if pmap.get_tile_type("ground_layer", x - 1, y) == "ro": return 999999
    if avoid_hill_corners:
        if avoid_hill_corners and (is_corner(x, y) or is_corner(x - 1, y) or is_corner(x, y - 1) or is_corner(x - 1, y - 1)):
            return 999999
    if pmap.get_tile_type("ground_layer", x, y) == "hi": return HILL_WEIGHT
    if pmap.get_tile_type("ground_layer", x - 1, y) == "hi" or pmap.get_tile_type("ground_layer", x, y - 1) == "hi" or pmap.get_tile_type("ground_layer", x - 1, y - 1) == "hi": return HILL_WEIGHT
    if pmap.get_tile_type("ground_layer", x, y) == "wa" or pmap.get_tile_type("ground_layer", x - 1, y) == "wa" or pmap.get_tile_type("ground_layer", x, y - 1) == "wa" or pmap.get_tile_type("ground_layer", x - 1, y - 1) == "wa": return WATER_WEIGHT
    if is_actual_path(pmap, x, y) and is_actual_path(pmap, x - 1, y) and is_actual_path(pmap, x, y - 1) and is_actual_path(pmap, x - 1, y - 1): return PATH_WEIGHT
    if pmap.get_tile_type("ground_layer", x, y) == "" or pmap.get_tile_type("ground_layer", x - 1, y) == "" or pmap.get_tile_type("ground_layer", x, y - 1) == "" or get_path_type(pmap, x, y) == 3: return GRASS_WEIGHT
    return 999999


def make_path_double(pmap, path, path_type):
    path_extention = set()
    for (x, y) in path:
        path_extention.add((x, y))
        path_extention.add((x, y - 1))
        path_extention.add((x - 1, y))
        path_extention.add((x - 1, y - 1))

    for (x, y) in path_extention:
        if pmap.tile_heights.get((x, y), 0) < 1:
            pmap.ground_layer[(x, y)] = ("ro", 0, 0)
        elif "pa" != pmap.get_tile_type("ground_layer", x, y):
            pmap.ground_layer[(x, y)] = path_type


def create_bridges(pmap):
    for y in range(pmap.height):
        for x in range(pmap.width):
            if pmap.get_tile("ground_layer", x, y) == ("ro", 0, 0):
                if pmap.get_tile_type("ground_layer", x, y - 1) == "wa":
                    pmap.ground_layer[(x, y)] = ("ro", 0, 0)
                    pmap.ground_layer[(x, y + 1)] = ("ro", 0, 1)
                elif pmap.get_tile_type("ground_layer", x, y + 1) == "wa":
                    pmap.ground_layer[(x, y - 1)] = ("ro", 0, 0)
                    pmap.ground_layer[(x, y)] = ("ro", 0, 1)
                elif pmap.get_tile_type("ground_layer", x - 1, y) == "wa":
                    pmap.ground_layer[(x, y)] = ("ro", 1, 0)
                    pmap.ground_layer[(x + 1, y)] = ("ro", 1, 1)
                elif pmap.get_tile_type("ground_layer", x + 1, y) == "wa":
                    pmap.ground_layer[(x, y)] = ("ro", 1, 1)
                    pmap.ground_layer[(x - 1, y)] = ("ro", 1, 0)
                else:
                    pmap.ground_layer[(x, y)] = ("pa", 0, 10)

            if "ro" == pmap.get_tile_type("ground_layer", x, y - 1) and "wa" == pmap.get_tile_type("ground_layer", x, y):
                pmap.decoration_layer[(x, y)] = ("de", 6, 0)


def create_stairs(pmap):

    def path_above(x, y):
        return is_actual_path(pmap, x, y - 1)

    def path_under(x, y):
        return is_actual_path(pmap, x, y + 1)

    def path_left(x, y):
        return is_actual_path(pmap, x - 1, y)

    def path_right(x, y):
        return is_actual_path(pmap, x + 1, y)

    for path_y in range(pmap.height):
        for path_x in range(pmap.width):
            if "pa" in pmap.get_tile_type("ground_layer", path_x, path_y) and pmap.tile_heights[(path_x, path_y)] > 1:
                if path_above(path_x, path_y) and path_under(path_x, path_y) and (path_left(path_x, path_y) or path_right(path_x, path_y)):
                    if pmap.tile_heights.get((path_x, path_y), 0) > pmap.tile_heights.get((path_x, path_y - 1), 0):
                        pmap.ground_layer[(path_x, path_y)] = ("ro", 3, 0)
                        pmap.ground_layer[(path_x + 1, path_y)] = ("ro", 3, 1)

                    elif pmap.tile_heights.get((path_x, path_y), 0) > pmap.tile_heights.get((path_x, path_y + 1), 0):
                        pmap.ground_layer[(path_x, path_y)] = ("ro", 2, 0)
                        pmap.ground_layer[(path_x + 1, path_y)] = ("ro", 2, 1)

                elif path_left(path_x, path_y) and path_right(path_x, path_y) and path_under(path_x, path_y):
                    if pmap.tile_heights.get((path_x, path_y), 0) > pmap.tile_heights.get((path_x - 1, path_y), 0):
                        pmap.ground_layer[(path_x, path_y)] = ("ro", 4, 0)
                        pmap.ground_layer[(path_x, path_y + 1)] = ("ro", 4, 1)

                    elif pmap.tile_heights.get((path_x, path_y), 0) > pmap.tile_heights.get((path_x + 1, path_y), 0):
                        pmap.ground_layer[(path_x, path_y)] = ("ro", 5, 0)
                        pmap.ground_layer[(path_x, path_y + 1)] = ("ro", 5, 1)


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
            if pmap.get_tile_type("secondary_ground", x, y) != "fe":
                if is_actual_path(pmap, x - 1, y) and (x - 1, y) not in pmap.buildings.keys() and (x - 1, y) not in pmap.secondary_ground.keys():
                    if random() < 0.08 and check_availability_zone(x, y - 2, x + 2, y + 1):
                        pmap.secondary_ground[(x, y)] = ("de", 4, 2)
                        pmap.decoration_layer[(x, y - 1)] = ("de", 4, 1)
                        pmap.decoration_layer[(x, y - 2)] = ("de", 4, 0)
                        pmap.secondary_ground[(x + 1, y)] = ("de", 5, 2)
                if is_actual_path(pmap, x + 1, y) and (x + 1, y) not in pmap.buildings.keys() and (x + 1, y) not in pmap.secondary_ground.keys():
                    if random() < 0.08 and check_availability_zone(x, y - 2, x, y + 1):
                        pmap.secondary_ground[(x, y)] = ("de", 3, 2)
                        pmap.decoration_layer[(x, y - 1)] = ("de", 3, 1)
                        pmap.decoration_layer[(x, y - 2)] = ("de", 3, 0)
