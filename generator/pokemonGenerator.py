def spawn_pokemon(pmap):
    SHINY_PROBABILITY = 0.001
    from random import random, randint

    def can_spawn_pokemon(odds):
        return odds > random()

    def is_enough_water_space(x1, y1, x2, y2):
        for check_y in range(y1, y2 + 1):
            for check_x in range(x1, x2 + 1):
                if "pd_" not in pmap.ground_layer.get((check_x, check_y), ""):
                    return False
        return True

    def spawn_lapras(odds):
        lapras = False
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if can_spawn_pokemon(odds) and is_enough_water_space(x - 1, y - 1, x + 1, y + 2):
                    if random() < SHINY_PROBABILITY:
                        # direction should be either 5 or 7
                        direction = 5 + 2 * randint(0, 1)
                    else:
                        # direction should be either 1 or 3
                        direction = 1 + 2 * randint(0, 1)
                    pmap.ground_layer[(x, y + 1)] = "pd_l_" + str(direction + 1)
                    pmap.ground_layer[(x, y)] = "pd_l_" + str(direction)
                lapras = True
        return lapras

    def spawn_gyarados(odds):
        gyarados = False
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                shiny = 0
                if can_spawn_pokemon(odds) and is_enough_water_space(x - 1, y - 1, x + 2, y + 2):
                    if random() < SHINY_PROBABILITY: shiny = 4
                    pmap.ground_layer[(x + 1, y)] = "pd_g_" + str(2 + shiny)
                    pmap.ground_layer[(x, y + 1)] = "pd_g_" + str(3 + shiny)
                    pmap.ground_layer[(x + 1, y + 1)] = "pd_g_" + str(4 + shiny)
                    pmap.ground_layer[(x, y)] = "pd_g_" + str(1 + shiny)
                    gyarados = True
        return gyarados

    def spawn_diglett(odds):
        diglett = False
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if (x, y) not in pmap.ground_layer.keys() and (x, y) not in pmap.buildings.keys() and can_spawn_pokemon(odds):
                    if random() < SHINY_PROBABILITY:
                        pmap.ground_layer[(x, y)] = "diglet_2"
                    else:
                        pmap.ground_layer[(x, y)] = "diglet_1"
                    diglett = True
        return diglett

    def spawn_snorlax(odds):

        def check_bridge_space(x1, y1, x2, y2):
            for check_y in range(y1, y2 + 1):
                for check_x in range(x1, x2 + 1):
                    if "b_" not in pmap.ground_layer.get((check_x, check_y), ""):
                        return False
                    if "sn_" in pmap.decoration_layer.get((check_x, check_y), ""):
                        return False
            return True

        snorlax = False
        shiny = 0
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if "b_" in pmap.ground_layer.get((x, y), "") and can_spawn_pokemon(odds) and check_bridge_space(x, y, x + 1, y + 1):
                    if random() < SHINY_PROBABILITY: shiny = 4
                    for snorlax_tile in range(4):
                        pmap.decoration_layer[(x + snorlax_tile % 2, y + snorlax_tile // 2)] = "sn_" + str(snorlax_tile + 1 + shiny)
                    snorlax = True
        return snorlax

    def spawn_exceguttor(odds):
        exceguttor = False
        shiny = 0
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if can_spawn_pokemon(odds) and "p_4" in pmap.ground_layer.get((x, y), ""):
                    if random() < SHINY_PROBABILITY: shiny = 2
                    pmap.decoration_layer[(x, y)] = "exc_" + str(1 + shiny)
                    pmap.decoration_layer[(x, y - 1)] = "exc_" + str(2 + shiny)
                exceguttor = True
        return exceguttor

    def spawn_togetic(odds):
        togetic = False
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if can_spawn_pokemon(odds):
                    pmap.decoration_layer[(x, y)] = "togetic"
                    togetic = True
        return togetic

    lapras = spawn_lapras(0.001)
    gyarados = spawn_gyarados(0.001)
    diglett = spawn_diglett(0.001)
    snorlax = spawn_snorlax(0.035)
    exceguttor = spawn_exceguttor(0.0025)
    togetic = spawn_togetic(0.0001)

    return lapras and diglett and snorlax and exceguttor and gyarados and togetic
