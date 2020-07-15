import random
from pathGenerator import is_actual_path


# Spawns a house on the map with house_front_path_type as its front porch
# Houses are spawned by chosing a random x and y coordinate, checking whether enough space is available for the given
# house if not, choose a new position. There's an upper limit to try find a building spot.
def spawn_house(pmap, house_type, house_front_path_type):

    # checks if a chosen position has enough free space for the house + spacing, starting from the top left corner
    def unavailable_building_spot(x, y, h_spacing, v_spacing):
        reference_height = pmap.tile_heights.get((x, y), 0)
        for check_y in range(y - 2, y + house_size_y + v_spacing):
            for check_x in range(x - h_spacing, x + house_size_x + h_spacing + 1):
                if pmap.tile_heights.get((check_x, check_y), -1) != reference_height or "pd_" in pmap.ground_layer.get((check_x, check_y), "") or "fe_" in pmap.ground_layer.get((check_x, check_y), "") or (check_x, check_y) in pmap.buildings.keys():
                    if "h_" in pmap.buildings.get((check_x, check_y), "") or "pc_" in pmap.buildings.get((check_x, check_y), "") or "pm" in pmap.buildings.get((check_x, check_y), ""):
                        return check_x, check_y
                    else:
                        return True

        return False

    # Chooses a random x and y coordinate to try build a house
    # If a house already exists on the chosen coordinate, searches for the lower right corner of given house and when
    # enough space available, builds the house adjacent on the right to the house previously found
    def search_available_building_spot(cluster_radius, max_attempts):
        attempts = 1
        house_x_attempt = random.randint(1, pmap.width - house_size_x)
        house_y_attempt = random.randint(1, pmap.height - house_size_y)
        unavailable_spot = unavailable_building_spot(house_x_attempt, house_y_attempt, 2, 3)
        while attempts < max_attempts and unavailable_spot or not is_inside_cluster(pmap, house_x_attempt, house_y_attempt, cluster_radius, 3):
            attempts += 1
            house_x_attempt = random.randint(1, pmap.width - house_size_x)
            house_y_attempt = random.randint(1, pmap.height - house_size_y)
            unavailable_spot = unavailable_building_spot(house_x_attempt, house_y_attempt, 2, 3)
            if not isinstance(unavailable_spot, bool):
                lower_right_of_house = find_lower_right_of_house(unavailable_spot[0], unavailable_spot[1], house_size_y)
                house_x_attempt, house_y_attempt = lower_right_of_house
                unavailable_spot = unavailable_building_spot(house_x_attempt, house_y_attempt, 0, 2)
        return (house_x_attempt, house_y_attempt) if attempts <= max_attempts and not unavailable_spot and is_inside_cluster(pmap, house_x_attempt, house_y_attempt, cluster_radius, 3) else False

    # search for the lower right corner of a house
    def find_lower_right_of_house(x, y, size_y):
        while "h_" in pmap.buildings.get((x - 1, y), "") or "pc_" in pmap.buildings.get((x - 1, y), "") or "pm_" in pmap.buildings.get((x - 1, y), "") or "h_" in pmap.buildings.get((x, y - 1), "") or "pc_" in pmap.buildings.get((x, y - 1), "") or "pm_" in pmap.buildings.get((x, y - 1), ""):
            if "h_" in pmap.buildings.get((x - 1, y), "") or "pc_" in pmap.buildings.get((x - 1, y), "") or "pm_" in pmap.buildings.get((x - 1, y), ""): y += 1
            if "h_" in pmap.buildings.get((x, y - 1), "") or "pc_" in pmap.buildings.get((x, y - 1), "") or "pm_" in pmap.buildings.get((x, y - 1), ""): x += 1
        return x, y - size_y

    if house_type == "pm" or house_type == "pc":
        if house_type == "pm":
            house_size_x, house_size_y = 4, 4
        else:
            house_size_x, house_size_y = 5, 5
    else:
        house_type_data = [[0, 4, 5, 5, 4, 4, 5, 5, 4, 6], [0, 4, 3, 4, 5, 7, 4, 4, 5, 4]]  # x and y size of each house
        house_size_x = house_type_data[0][house_type]
        house_size_y = house_type_data[1][house_type]

    build_spot = search_available_building_spot(40, 99)
    if build_spot:
        house_x = build_spot[0]
        house_y = build_spot[1]
        for house_build_y in range(house_size_y):
            for house_build_x in range(house_size_x):
                if house_type == "pm" or house_type == "pc":
                    pmap.buildings[(house_x + house_build_x, house_y + house_build_y)] = str(house_type) + "_" + str(house_build_x + (house_build_y * house_size_x) + 1)
                else:
                    pmap.buildings[(house_x + house_build_x, house_y + house_build_y)] = "h_" + str(house_type) + "_" + str(house_build_x + (house_build_y * house_size_x) + 1)
        pmap.front_doors.append((round(house_x + house_size_x / 2), house_y + house_size_y + 1))
        for front_y in range(4):
            for front_x in range(house_size_x):
                if (house_x + front_x, house_y + house_size_y + front_y - 2) not in pmap.ground_layer.keys():
                    pmap.ground_layer[(house_x + front_x, house_y + house_size_y + front_y - 2)] = house_front_path_type
        if house_type != "pm" and house_type != "pc":
            if random.randint(0, 1) == 1 and not pmap.has_tile_at_position(pmap.ground_layer, house_x - 1, house_y + house_size_y - 2):
                pmap.buildings[(house_x - 1, house_y + house_size_y - 1)] = "mbx_0"
                pmap.buildings[(house_x - 1, house_y + house_size_y - 2)] = "mbx_1"

            if random.randint(1, 4) == 1:
                create_fence(pmap, house_x + house_size_x - 1, house_y + 1, 5, True)


# Checks whether a coordinate is at least in radius [distance] of [connections] houses
def is_inside_cluster(pmap, x, y, radius, connections):
    from math import sqrt

    if len(pmap.front_doors) == 0:
        return True

    found_connections = 0
    for (front_door_x, front_door_y) in pmap.front_doors:
        if sqrt((x - front_door_x) ** 2 + (y - front_door_y) ** 2) < radius:
            found_connections += 1
        if connections > len(pmap.front_doors):
            if found_connections == 1: return True
        else:
            if found_connections == connections: return True
    return False


# gives people a backyard surrounded by a fence
def create_fence(pmap, x, y, max_y, tree=False):
    def can_have_fence():
        curr_size = min(size_x // 2 + 1, max_y)
        new_max_y = curr_size
        for test_y in range(y - curr_size - 1, y):
            for test_x in range(x - size_x, x):
                if new_max_y == curr_size and "m_4" in pmap.ground_layer.get((test_x, test_y), ""):
                    new_max_y = curr_size - 1
                if "fe_" in pmap.ground_layer.get((test_x, test_y), "") or is_actual_path(pmap, test_x, test_y) or "pd_" in pmap.ground_layer.get((test_x, test_y), ""):
                    return False
        return new_max_y

    def check_house_width():
        test_x = x
        while "h_" in pmap.buildings.get((test_x, y), ""):
            test_x -= 1
        return x - test_x - 1

    def try_build_fence(fx, fy, height, fence):
        if pmap.tile_heights.get((fx, fy), -1) == height:
            pmap.ground_layer[(fx, fy)] = fence

    size_x = check_house_width()
    upd_max_y = can_have_fence()
    if upd_max_y:
        fence_height = pmap.tile_heights.get((x, y), -1)
        size_y = min(size_x // 2 + 1, max_y) if upd_max_y == max_y else upd_max_y
        try_build_fence(x, y - size_y, fence_height, "fe_1_5")
        try_build_fence(x - size_x, y - size_y, fence_height, "fe_1_8")
        for fence_y in range(y, y - size_y, -1):
            try_build_fence(x - size_x, fence_y, fence_height, "fe_1_4")
            try_build_fence(x, fence_y, fence_height, "fe_1_2")
        for fence_x in range(x - size_x + 1, x):
            if tree and random.randint(1, 100) == 1:
                pmap.ground_layer[(fence_x, y - size_y)] = "sne_1"
            else:
                try_build_fence(fence_x, y - size_y, fence_height, "fe_1_1")


# Adds random points to the sides of the map to have path running to the edge of the screen
def add_random_ends(pmap, path_type):
    end_sides = []
    nb_ends = random.randint(2, 4)
    for end in range(nb_ends):
        end_side = random.randint(0, 3)
        while end_side in end_sides:
            end_side = random.randint(0, 3)
        x = 1
        y = 1
        if end_side == 0:
            x = random.randint(0 + pmap.width // 4, 0 + 3 * (pmap.width // 4))
            end_sides.append(0)
        elif end_side == 1:
            x = pmap.width - 1
            y = random.randint(0 + pmap.height // 4, 0 + 3 * (pmap.height // 4))
            end_sides.append(1)
        elif end_side == 2:
            x = random.randint(0 + pmap.width // 4, 0 + 3 * (pmap.width // 4))
            y = pmap.height - 1
            end_sides.append(2)
        elif end_side == 3:
            y = random.randint(0 + pmap.height // 4, 0 + 3 * (pmap.height // 4))
            end_sides.append(3)

            max_height = 0
            for y_around in range(y - 2, y + 3):
                for x_around in range(x - 3, x + 3):
                    if "fe_" in pmap.ground_layer.get((x_around, y_around), ""):
                        max_height = -1
                        break
                    else:
                        max_height = max(max_height, pmap.tile_heights.get((x_around, y_around), 0))

            if max_height > 1:
                pmap.end_points.append((x, y))
                pmap.ground_layer[(x, y)] = path_type
                for y_around in range(y - 2, y + 3):
                    for x_around in range(x - 3, x + 3):
                        if not pmap.out_of_bounds(x_around, y_around) and "pd_" not in pmap.ground_layer.get((x_around, y_around), ""): pmap.tile_heights[(x_around, y_around)] = max_height