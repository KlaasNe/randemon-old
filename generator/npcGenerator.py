import random
from pathGenerator import is_actual_path
from buildingGenerator import is_inside_cluster

NB_NPC = 55
off_Path_Npc = [14, 15, 26, 27, 28, 29, 30, 31, 32, 36, 37, 38, 39, 49]
water_Npc = [28, 29, 30]
shore_Npc = [31, 32, 37, 38]
bridge_Npc = [31, 32, 36, 37, 38]
outside_Npc = [14, 15, 26, 27, 39, 49]


def spawn_npc(pmap, population, path_only=False):
    coord = random_npc_coordinates(pmap, population)
    for co in coord:
        x, y = co
        if (x, y) not in pmap.buildings.keys() and "m_" not in pmap.ground_layer.get((x, y), ""):
            if path_only:
                if is_actual_path(pmap, x, y):
                    npc = get_path_npc()
                    set_npc(pmap, npc, x, y)
            else:
                npc = get_npc(pmap, x, y)
                if npc is not None: set_npc(pmap, npc, x, y)


def set_npc(pmap, npc, x, y):
    direction = 1 if npc == 50 else random.randint(1, 4)
    pmap.npc_layer[(x, y)] = "npc_" + str(npc) + "_" + str(direction)
    if direction == 2 and is_actual_path(pmap, x, y):
        if (x + 1, y) not in pmap.npc_layer.keys() and (x + 1, y) not in pmap.buildings.keys() and "m_" not in pmap.ground_layer.get((x + 1, y), "") and "st_" not in pmap.ground_layer.get((x + 1, y), "") and "fe_" not in pmap.ground_layer.get((x, y), ""):
            snpc = get_path_npc()
            while snpc == 50:
                snpc = get_path_npc()
            pmap.npc_layer[(x + 1, y)] = "npc_" + str(snpc) + "_4"


def get_npc(pmap, x, y):
    WATER_POP = 0.2
    npc_number = None
    if not pmap.raining:
        if random.random() < WATER_POP and "pd_" in pmap.ground_layer.get((x, y), "") and is_inside_cluster(pmap, x, y, 20, 1):
            npc_number = get_water_npc()
        elif "b_" in pmap.ground_layer.get((x, y), ""):
            npc_number = get_bridge_npc()
        elif random.random() < WATER_POP and "p_4" in pmap.ground_layer.get((x, y), "") and is_inside_cluster(pmap, x, y, 20, 1):
            npc_number = get_shore_npc()
    if (x, y) not in pmap.ground_layer.keys():
        npc_number = get_outside_npc()
    elif is_actual_path(pmap, x, y):
        npc_number = get_path_npc()
    return npc_number


def get_path_npc():
    npc_nr = random.randint(1, NB_NPC)
    while npc_nr in off_Path_Npc:
        npc_nr = random.randint(1, NB_NPC)
    return npc_nr


def get_water_npc():
    return water_Npc[random.randint(1, len(water_Npc) - 1)]


def get_bridge_npc():
    return bridge_Npc[random.randint(1, len(bridge_Npc) - 1)]


def get_shore_npc():
    return shore_Npc[random.randint(1, len(shore_Npc) - 1)]


def get_outside_npc():
    return outside_Npc[random.randint(1, len(outside_Npc) - 1)]


def random_npc_coordinates(pmap, population):
    coord = set()
    for npc in range(round(pmap.width * pmap.height * (population / 100))):
        (x, y) = random_on_map(pmap)
        coord.add((x, y))
    return coord


def random_on_map(pmap):
    return random.randint(0, pmap.width - 1), random.randint(0, pmap.height - 1)
