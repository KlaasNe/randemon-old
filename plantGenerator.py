from noise import snoise2
import random


def create_trees(pmap, spawn_rate, x_offset, y_offset):
    octaves = 2
    freq = 40
    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            if (x, y) not in pmap.ground_layer.keys() and (x, y - 1) not in pmap.ground_layer.keys() and (x, y - 2) not in pmap.ground_layer.keys() and (x, y) not in pmap.buildings.keys() and (x, y) not in pmap.decoration_layer.keys():
                if snoise2((x + x_offset) / freq, (y + y_offset) / freq, octaves) + 0.5 < spawn_rate / 100 and random.random() > 0.5:
                    pmap.ground_layer[(x, y)] = "st_0"
                    pmap.ground_layer[(x, y - 1)] = "st_1"
                    pmap.ground_layer[(x, y - 2)] = "st_2"
