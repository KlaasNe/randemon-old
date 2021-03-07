from noise import snoise2
import random


# Checks if enough space is available to plant a tree
# No trees above the highest path height
# Adds an overlay to decoration_layer if the top of the tree overlaps with another tree
def create_trees(pmap, layer, spawn_rate, x_offset, y_offset):
    def mergeable(x, y):
        if (x, y - 1) not in layer.get_ex_pos() and (x + 1, y - 1) not in layer.get_ex_pos():
            if layer.get_tile((x, y)) == ("na", 2, 2) == layer.get_tile((x + 1, y)):
                if pmap.ground2.get_tile((x, y - 1)) == ("na", 2, 1) == pmap.ground2.get_tile((x + 1, y - 1)):
                    return True
        return False

    octaves = 2
    freq = 40
    for y in range(pmap.height):
        for x in range(pmap.width):
            if pmap.tile_heights.get((x, y), -1) <= pmap.highest_path:
                if (x, y) not in layer.get_ex_pos() and (x, y) not in pmap.ground2.get_ex_pos() and (x, y - 1) not in pmap.ground2.get_ex_pos() and (x, y) not in pmap.buildings.get_ex_pos() and (x, y) not in pmap.decoration.get_ex_pos() and (x, y - 1) not in pmap.decoration.get_ex_pos():
                    if abs(snoise2((x + x_offset) / freq, (y + y_offset) / freq, octaves)) * 2 > 1 - (spawn_rate / 100) and random.random() > 0.5:
                        pmap.decoration.set_tile((x, y - 2), ("na", 2, 0))
                        pmap.ground2.set_tile((x, y - 1), ("na", 2, 1))
                        pmap.ground.set_tile((x, y), ("na", 2, 2))

    for y in range(pmap.height):
        for x in range(pmap.width):
            if mergeable(x, y):
                pmap.decoration.set_tile((x, y - 2), ("na", 1, 5))
                pmap.decoration.set_tile((x + 1, y - 2), ("na", 2, 5))
                pmap.ground2.set_tile((x, y - 1), ("na", 1, 6))
                pmap.ground2.set_tile((x + 1, y - 1), ("na", 2, 6))
                pmap.ground.set_tile((x, y), ("na", 1, 7))
                pmap.ground.set_tile((x + 1, y), ("na", 2, 7))


# The whole map is filled with random green tiles
# Tall gras and flowers are spawned with a perlin noise field
def grow_grass(pmap, tall_grass_coverage, x_offset, y_offset):
    def random_grass(gx, gy):
        octaves = 2
        freq = 20
        sne_probability = abs(snoise2((gx + x_offset) / freq, (gy + y_offset) / freq, octaves)) * 2
        if pmap.tile_heights.get((gx, gy), -1) <= pmap.highest_path:
            if sne_probability < 1 - (tall_grass_coverage / 100) or (x, y - 1) in pmap.buildings.get_ex_pos() or (x, y) in pmap.ground2.get_ex_pos():
                grass_type = random.randint(0, 7)
                return "na", 0, grass_type
            else:
                sne_type = random.randint(0, 1)
                # Turn 80 percent of the flowers into tall grass
                if sne_type == 1 and random.random() < 0.8: return "na", 1, 0
                # Turn 0.5 percent of the tall grass into tall grass with a hidden item
                if sne_type == 0 and random.random() < 0.005: return "na", 1, 4
                return "na", 1, sne_type
        else:
            return "hi", 0, 0

    for y in range(pmap.height):
        for x in range(pmap.width):
            if (x, y) not in pmap.ground.get_ex_pos():
                pmap.plants.set_tile((x, y), random_grass(x, y))


def grow_snake_bushes(layer, spawnrate, growth):
    def create_snake_bush(pos):
        x, y = pos
        end2 = get_pos_around(((x, y), pos))
        end1 = (pos, end2[0])
        if end2 is not None:
            bush_ends = [end1, end2]
            while random.random() < growth:
                new_end_data = grow_random_end(bush_ends)
                if new_end_data is not None:
                    bush_ends[new_end_data[0]] = new_end_data[1]
                else: break

    def get_pos_around(pos):
        x, y = pos[0]
        direction = random.randint(0, 3)
        new_pos_opt = ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1))
        new_pos = new_pos_opt[direction]
        for tries in range(1, 5):
            if new_pos not in layer.get_ex_pos() and new_pos != pos[1]:
                return new_pos, (x, y)
            else:
                new_pos = new_pos_opt[(direction + tries) % 4]
        return None

    def grow_random_end(ends):
        rel_sprites = {(1, 0): {(0, -1): ("na", 4, 3), (-1, 0): ("na", 5, 0), (0, 1): ("na", 4, 0)},
                       (0, -1): {(-1, 0): ("na", 4, 2), (0, 1): ("na", 5, 1)},
                       (-1, 0): {(0, 1): ("na", 4, 1)}}
        end_int = random.randint(0, 1)
        prev_end = ends[end_int]
        x, y = prev_end[0]
        old_x, old_y = prev_end[1]
        new_end = get_pos_around(prev_end)
        if new_end is not None:
            new_x, new_y = new_end[0]
            rel_pos1 = (new_x - x, new_y - y)
            rel_pos2 = (old_x - x, old_y - y)
            try:
                sprite = rel_sprites[rel_pos1][rel_pos2]
            except KeyError:
                try:
                    sprite = rel_sprites[rel_pos2][rel_pos1]
                except KeyError as e:
                    print(e)
                    print(rel_pos1)
                    print(rel_pos2)
            layer.set_tile((x, y), sprite)
            return end_int, new_end

    for y in range(layer.sy):
        for x in range(layer.sx):
            if random.random() < spawnrate / 100 and (x, y) not in layer.get_ex_pos():
                create_snake_bush((x, y))


# Creates an overlay for the entire map showing rain
# The amount of rain is given with rain_rate
def create_rain(pmap, layer, odds,  rain_rate):
    if random.random() < odds:
        for y in range(pmap.height):
            for x in range(pmap.width):
                if random.random() < rain_rate:
                    if random.random() < 0.5 and "fe" != pmap.ground2.get_tile_type((x, y)) and "hi" != pmap.ground.get_tile_type((x, y)) and (x, y) not in pmap.npc.get_ex_pos():
                        layer.set_tile((x, y), ("ra", random.randint(0, 2), 1))
                    else:
                        layer.set_tile((x, y), ("ra", random.randint(1, 2), 0))
                else:
                    layer.set_tile((x, y), ("ra", 0, 0))
