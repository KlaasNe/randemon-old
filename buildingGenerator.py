import random


def spawn_house(pmap, house_type, house_front_path_type):

    def unavailable_building_spot(x, y, horizontal_spacing, vertical_spacing):
        reference_height = pmap.tile_heights.get((x, y), 0)
        for check_y in range(y - vertical_spacing, y + house_size_y + vertical_spacing):
            for check_x in range(x - vertical_spacing, x + house_size_x + horizontal_spacing):
                if pmap.tile_heights.get((check_x, check_y), -1) != reference_height or "h_" in pmap.buildings.get((check_x, check_y), "") or "pd_" in pmap.ground_layer.get((check_x, check_y), ""):
                    return True
        return False

    def search_available_building_spot(cluster_radius, max_attempts):
        attempts = 1
        house_x_attempt = random.randint(1, pmap.width - house_size_x)
        house_y_attempt = random.randint(1, pmap.height - house_size_y)
        while attempts < max_attempts and unavailable_building_spot(house_x_attempt, house_y_attempt, 1, 3) or not is_inside_cluster(house_x_attempt, house_y_attempt, cluster_radius, 3):
            attempts += 1
            house_x_attempt = random.randint(1, pmap.width - house_size_x)
            house_y_attempt = random.randint(1, pmap.height - house_size_y)
            if "h_" in pmap.buildings.get((house_x_attempt, house_y_attempt), ""):
                lower_right_of_house = find_lower_right_of_house(house_x_attempt, house_y_attempt, house_size_y)
                house_x_attempt = lower_right_of_house[0]
                house_y_attempt = lower_right_of_house[1]
        return (house_x_attempt, house_y_attempt) if not attempts >= max_attempts and not unavailable_building_spot(house_x_attempt, house_y_attempt, 0, 3) and is_inside_cluster(house_x_attempt, house_y_attempt, cluster_radius, 3) else False

    def is_inside_cluster(x, y, radius, connections):
        from math import sqrt

        if len(pmap.front_doors) == 0: return True

        found_connections = 0
        for (front_door_x, front_door_y) in pmap.front_doors:
            if sqrt((x - front_door_x) ** 2 + (y - front_door_y) ** 2) < radius:
                found_connections += 1
            if connections > len(pmap.front_doors):
                if found_connections == 1: return True
            else:
                if found_connections == connections: return True
        return False

    def find_lower_right_of_house(x, y, size_y):
        while "h_" in pmap.buildings.get((x - 1, y), "") or "h_" in pmap.buildings.get((x, y - 1), ""):
            if "h_" in pmap.buildings.get((x - 1, y), ""): y += 1
            if "h_" in pmap.buildings.get((x, y - 1), ""): x += 1
        return (x, y - size_y)

    house_type_data = [[0, 4, 5, 5, 4, 4, 5, 5, 4, 6], [0, 4, 3, 4, 5, 7, 4, 4, 5, 4]]  # x and y size of each house
    house_size_x = house_type_data[0][house_type]
    house_size_y = house_type_data[1][house_type]

    build_spot = search_available_building_spot(40, 999)
    if build_spot:
        house_x = build_spot[0]
        house_y = build_spot[1]
        for house_build_y in range(house_size_y):
            for house_build_x in range(house_size_x):
                pmap.buildings[(house_x + house_build_x, house_y + house_build_y)] = "h_" + str(house_type) + "_" + str(house_build_x + (house_build_y * house_size_x) + 1)
        pmap.front_doors.append((round(house_x + house_size_x / 2), house_y + house_size_y + 1))
        for front_y in range(4):
            for front_x in range(house_size_x):
                pmap.ground_layer[(house_x + front_x, house_y + house_size_y + front_y - 2)] = house_front_path_type
        # houses_Front_Doors.append((int(house_x + house_size_x / 2), int(house_y + house_size_y)))
        if random.randint(0, 1) == 1 and not pmap.has_tile_at_position(pmap.ground_layer, house_x - 1, house_y + house_size_y - 2):
            pmap.buildings[(house_x - 1, house_y + house_size_y - 1)] = "mbx_0"
            pmap.buildings[(house_x - 1, house_y + house_size_y - 2)] = "mbx_1"

