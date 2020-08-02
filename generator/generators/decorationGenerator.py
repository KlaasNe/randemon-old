import math
import random

from generators.pathGenerator import is_actual_path


# Spawns a truck on top of path
def spawn_truck(pmap, odds):
    for x in range(pmap.width):
        for y in range(pmap.height):
            if random.random() < odds and check_for_ground(pmap, x, y, 1, 3) and is_actual_path(pmap, x, y + 2) and is_actual_path(pmap, x + 2, y + 2):
                if check_for_building(pmap, x, y, 3, 3) and flat_surface(pmap, x, y + 1, 3, 2) and check_for_decoration(pmap, x, y, 3, 3):
                    for truck_tile in range(9):
                        pmap.secondary_ground[(x + truck_tile % 3, y + math.floor(truck_tile / 3))] = ("de", 7 + truck_tile % 3, truck_tile // 3)
                    return


# Checks wether a surface covering x to x + x_size, y to y + y_size all has the same heigt
def flat_surface(pmap, x, y, x_size, y_size):
    reference_height = pmap.tile_heights.get((x, y), -1)
    for tile in range(1, x_size * y_size + 1):
        if pmap.tile_heights.get((x + (tile % x_size), y + (tile // x_size)), -2) != reference_height:
            return False
    return True


# Checks an area for tiles in the building_layer
def check_for_building(pmap, x, y, x_size, y_size):
    for check_y in range(y, y + y_size + 1):
        for check_x in range(x, x + x_size + 1):
            if pmap.out_of_bounds(check_x, check_y) or (check_x, check_y) in pmap.buildings.keys():
                return False
    return True


# Checks an area for tiles in the ground_layer
def check_for_ground(pmap, x, y, x_size, y_size):
    for check_y in range(y, y + y_size + 1):
        for check_x in range(x, x + x_size + 1):
            if pmap.out_of_bounds(check_x, check_y) or (check_x, check_y) in pmap.ground_layer.keys():
                return False
    return True


# Checks an area for tiles in the decoration_layer
def check_for_decoration(pmap, x, y, x_size, y_size):
    for check_y in range(y, y + y_size + 1):
        for check_x in range(x, x + x_size + 1):
            if pmap.out_of_bounds(check_x, check_y) or (check_x, check_y) in pmap.decoration_layer.keys():
                return False
    return True


# Spawns rocks in water if no water is present in the ground layer at 10 tiles distance
def spawn_rocks(pmap, rocky_percentage):
    for y in range(pmap.height):
        for x in range(pmap.width):
            if random.random() < rocky_percentage:
                if "wa" == pmap.get_tile_type("ground_layer", x, y) and (x, y) not in pmap.decoration_layer.keys() and (x, y) not in pmap.npc_layer.keys():
                    if "wa" != pmap.get_tile_type("ground_layer", x - 10, y) or "wa" != pmap.get_tile_type("ground_layer", x + 10, y) or "wa" != pmap.get_tile_type("ground_layer", x, y - 10) or "wa" != pmap.get_tile_type("ground_layer", x, y + 10):
                        rock_type = random.randint(0, 1)
                        pmap.decoration_layer[(x, y)] = ("de", 6, 1 + rock_type)


# Spawns a team rocket balloon
def spawn_balloon(pmap):
    balloon = False
    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            if not balloon and random.random() < 0.001 and not pmap.out_of_bounds(x - 2, y) and (x + 1, y + 2) not in pmap.ground_layer.keys() and (x + 1, y + 2) not in pmap.buildings.keys() and (x + 1, y + 2) not in pmap.secondary_ground.keys() and y + 2 < pmap.height:
                for balloon_tile in range(12):
                    if balloon_tile >= 9:
                        pmap.secondary_ground[(x + balloon_tile % 3, y + balloon_tile // 3)] = ("de", balloon_tile % 3, balloon_tile // 3)
                    else:
                        pmap.decoration_layer[(x + balloon_tile % 3, y + balloon_tile // 3)] = ("de", balloon_tile % 3, balloon_tile // 3)
                return
