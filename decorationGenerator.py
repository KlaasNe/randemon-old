import math
import random


def spawn_truck(pmap, odds):
    for x in range(pmap.width):
        for y in range(pmap.height):
            if random.random() < odds and "p_" in pmap.ground_layer.get((x, y + 3), "") and "p_" in pmap.ground_layer.get((x + 2, y + 3), "") and "p_4" not in pmap.ground_layer.get((x, y + 3), "") and "p_4" not in pmap.ground_layer.get((x + 2, y + 3), ""):
                if check_for_building(pmap, x, y, 3, 3) and check_for_ground(pmap, x, y, 3, 1) and flat_surface(pmap, x, y + 1, 3, 2) and check_for_decoration(pmap, x, y, 3, 3):
                    for truck_tile in range(9):
                        pmap.decoration_layer[(x + truck_tile % 3, y + math.floor(truck_tile / 3))] = "t_" + str(truck_tile + 1)
                    pmap.ground_layer["Truck"] = True


def flat_surface(pmap, x, y, x_size, y_size):
    reference_height = pmap.tile_heights.get((x, y), -1)
    for tile in range(1, x_size * y_size + 1):
        if pmap.tile_heights.get((x + (tile % x_size), y + (tile // x_size)), -2) != reference_height:
            return False
    return True


def check_for_building(pmap, x, y, x_size, y_size):
    for check_y in range(y, y + y_size + 1):
        for check_x in range(x, x + x_size + 1):
            if pmap.out_of_bounds(check_x, check_y) or (check_x, check_y) in pmap.buildings.keys():
                return False
    return True


def check_for_ground(pmap, x, y, x_size, y_size):
    for check_y in range(y, y + y_size + 1):
        for check_x in range(x, x + x_size + 1):
            if pmap.out_of_bounds(check_x, check_y) or (check_x, check_y) in pmap.ground_layer.keys():
                return False
    return True

def check_for_decoration(pmap, x, y, x_size, y_size):
    for check_y in range(y, y + y_size + 1):
        for check_x in range(x, x + x_size + 1):
            if pmap.out_of_bounds(check_x, check_y) or (check_x, check_y) in pmap.ground_layer.keys():
                return False
    return True


def spawn_rocks(pmap, rocky_percentage):
    for y in range(pmap.height):
        for x in range(pmap.width):
            if random.random() < rocky_percentage:
                if "pd_" in pmap.ground_layer.get((x, y), "") and (x, y) not in pmap.decoration_layer.keys() and (x, y) not in pmap.npc_layer.keys():
                    if "pd_" not in pmap.ground_layer.get((x + 10, y), "") or "pd_" not in pmap.ground_layer.get((x - 10, y), "") or "pd_" not in pmap.ground_layer.get((x, y + 10), "") or "pd_" not in pmap.ground_layer.get((x, y - 10), ""):
                        pmap.decoration_layer[(x, y)] = "sr_0"
