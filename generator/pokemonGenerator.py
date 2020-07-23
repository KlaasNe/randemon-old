from random import random, randint


# Spawns pokemon on the map most in the pmap.ground_layer
# Returns true if all existing pokemon are present on the map
pokemon_data = {
    "diglett": {"pos": (0, 0), "size": (1, 1), "odds": 0.001},
    "lapras": {"pos": (1, 0), "size": (1, 2), "odds": 0.001},
    "gyarados": {"pos": (2, 0), "size": (2, 2), "odds": 0.0005},
    "snorlax": {"pos": (4, 0), "size": (2, 2), "odds": 0.035},
    "exeggutor": {"pos": (6, 0), "size": (1, 2), "odds": 0.0025},
    "togetic": {"pos": (7, 0), "size": (1, 2), "odds": 0.0001},
    "seel": {"pos": (8, 0), "size": (1, 1), "odds": 0.0025}
}


def spawn_pokemons(pmap):
    SHINY_PROBABILITY = 0.001

    # May the odds be ever in your favour.
    def good_odds(odds):
        return odds > random()

    def is_enough_water_space(x1, y1, x2, y2):
        for check_y in range(y1, y2 + 1):
            for check_x in range(x1, x2 + 1):
                if "wa" not in pmap.get_tile_type("ground_layer", check_x, check_y):
                    return False
        return True

    def spawn_lapras(odds):
        lapras = False
        for y in range(pmap.height):
            for x in range(pmap.width):
                if good_odds(odds) and is_enough_water_space(x - 1, y - 1, x + 1, y + 2):
                    shiny = 2 if random() < SHINY_PROBABILITY else 0
                    pmap.ground_layer[(x, y)] = ("po", 1, shiny)
                    pmap.ground_layer[(x, y + 1)] = ("po", 1, 1 + shiny)
                lapras = True
        return lapras

    def spawn_gyarados(odds):
        gyarados = False
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if good_odds(odds) and is_enough_water_space(x - 1, y - 1, x + 2, y + 2):
                    shiny = 2 if random() < SHINY_PROBABILITY else 0
                    for gyarados_tile in range(4):
                        pmap.decoration_layer[(x + gyarados_tile % 2, y + gyarados_tile // 2)] = (
                        "po", 2 + gyarados_tile % 2, gyarados_tile // 2 + shiny)
                    gyarados = True
        return gyarados

    def spawn_diglett(odds):
        diglett = False
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if pmap.tile_heights.get((x, y), -1) <= pmap.highest_path and (x, y) not in pmap.ground_layer.keys() and (x, y) not in pmap.buildings.keys() and good_odds(odds):
                    shiny = 2 if random() < SHINY_PROBABILITY else 0
                    pmap.ground_layer[(x, y)] = ("po", 0, 0 + shiny)
                    diglett = True
        return diglett

    def spawn_snorlax(odds):

        def check_bridge_space(x1, y1, x2, y2):
            for check_y in range(y1, y2 + 1):
                for check_x in range(x1, x2 + 1):
                    if "ro" not in pmap.ground_layer.get((check_x, check_y), ""):
                        return False
                    if "po" in pmap.decoration_layer.get((check_x, check_y), ""):
                        return False
            return True

        snorlax = False
        shiny = 0
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if "ro" in pmap.ground_layer.get((x, y), "") and good_odds(odds) and check_bridge_space(x, y, x + 1, y + 1):
                    shiny = 2 if random() < SHINY_PROBABILITY else 0
                    for snorlax_tile in range(4):
                        pmap.decoration_layer[(x + snorlax_tile % 2, y + snorlax_tile // 2)] = ("po", 4 + snorlax_tile % 2, snorlax_tile // 2 + shiny)
                    snorlax = True
        return snorlax

    def spawn_exceguttor(odds):
        exceguttor = False
        shiny = 0
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if good_odds(odds) and "p_4" in pmap.ground_layer.get((x, y), ""):
                    if random() < SHINY_PROBABILITY: shiny = 2
                    pmap.decoration_layer[(x, y)] = "exc_" + str(1 + shiny)
                    pmap.decoration_layer[(x, y - 1)] = "exc_" + str(2 + shiny)
                exceguttor = True
        return exceguttor

    def spawn_togetic(odds):
        togetic = False
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if good_odds(odds):
                    shiny = 2 if random() < SHINY_PROBABILITY else 0
                    pmap.decoration_layer[(x, y)] = ("po", 7, shiny)
                    pmap.decoration_layer[(x, y + 1)] = ("po", 7, 1 + shiny)
                    togetic = True
        return togetic

    lapras = spawn_lapras(0.001)
    gyarados = spawn_gyarados(0.0005)
    diglett = spawn_diglett(0.001)
    snorlax = spawn_snorlax(0.025)
    # exceguttor = spawn_exceguttor(0.0025)
    togetic = spawn_togetic(0.0001)

    return lapras and diglett and snorlax and exceguttor and gyarados and togetic
