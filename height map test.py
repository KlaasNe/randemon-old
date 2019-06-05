import time, datetime, pygame, os, random, math
from noise import pnoise2, snoise2
from math import floor
from worldMap import image_grayscale_to_dict


def random_grass(decoration_rate, x, y, off_x, off_y):
    octaves = 1
    freq = 7

    sne_prob = snoise2((x + off_x) / freq, (y + off_y) / freq, octaves) + 1
    if sne_prob > (decoration_rate / 100):
        temp_grass = random.randint(0, 3)
        return "g_" + str(temp_grass)
    else:
        if random.random() < 0.001 and not ground_Tiles["Diglet"]:
            ground_Tiles["Diglet"] = True
            if random.random() < 0.02:
                return "diglet_2"
            else:
                return "diglet_1"
        else:
            temp_sne = random.randint(0, 4)
            while not (temp_sne == 0 or temp_sne == 2):
                temp_sne = random.randint(0, 4)
            if temp_sne == 2 and random.random() < 0.8: temp_sne = 0
            return "sne_" + str(temp_sne)


def fill_up_grass(layer, decoration_rate):
    off_x = random.random() * 1000000
    off_y = random.random() * 1000000
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if not (x, y) in layer.keys():
                layer[(x, y)] = random_grass(decoration_rate, x, y, off_x, off_y)


def generate_hills(layer):
    #mountainize(tile_Heights, 10)
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            hill_texture = str(calculate_hill_texture(tile_Heights, x, y))
            if not hill_texture == "-1":
                layer[(x, y)] = "m_" + hill_texture


def mountainize(layer, max_height):
    octaves = 1
    freq = 150
    off_x = random.random() * 1000000
    off_y = random.random() * 1000000
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            tile_height = abs(floor((snoise2((x + off_x) / freq, (y + off_y) / freq, octaves)) * max_height))
            layer[(x, y)] = tile_height


def generate_height_map(layer, height_list):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            layer[(x, y)] = "height_" + str(height_list[(x, y)])


def calculate_hill_texture(height_list, x, y):
    hills_around = test_hills_around(height_list, x, y)
    if hills_around[3] == 0 and hills_around[6] == -1 and hills_around[7] == 0: return 9
    if hills_around[5] == 0 and hills_around[7] == 0 and hills_around[8] == -1: return 10
    if hills_around[0] == -1 and hills_around[1] == 0 and hills_around[3] == 0: return 4
    if hills_around[1] == 0 and hills_around[2] == -1 and hills_around[5] == 0: return 4
    if hills_around[1] == 0 and hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == 0: return -1
    if hills_around[1] == 0 and hills_around[3] == -1 and hills_around[7] == 0: return 1
    if hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == -1: return 2
    if hills_around[1] == 0 and hills_around[5] == -1 and hills_around[7] == 0: return 3
    if hills_around[1] == -1 and hills_around[3] == 0 and hills_around[5] == 0: return 4
    if hills_around[1] == -1 and hills_around[3] == -1: return 5
    if hills_around[3] == -1 and hills_around[7] == -1: return 6
    if hills_around[5] == -1 and hills_around[7] == -1: return 7
    if hills_around[1] == -1 and hills_around[5] == -1: return 8
    return -1



def test_hills_around(height_list, x, y):
    current_tile_height = height_list[(x, y)]
    hills_around = []

    for around in range(0, 9):
        tile_coo = (x + around % 3 - 1, y + around // 3 - 1)
        if height_list.get(tile_coo, current_tile_height) == current_tile_height: hills_around.append(0)
        if height_list.get(tile_coo, current_tile_height) < current_tile_height: hills_around.append(-1)
        if height_list.get(tile_coo, current_tile_height) > current_tile_height: hills_around.append(1)

    return hills_around


def render(layer):
    for x in range(0, map_Size_X):
        for y in range(0, map_Size_Y):
            if (x, y) in layer.keys():
                tile = str(layer[(x, y)])
                try:
                    screen.blit(pygame.image.load(os.path.join("resources", tile + ".png")), (x * tile_Size, y * tile_Size))
                except Exception as e:
                    screen.blit(pygame.image.load(os.path.join("resources", "missing.png")), (x * tile_Size, y * tile_Size))
                    print(e)

    pygame.display.update()


ground_Tiles = {}
height_Tiles = {}
tile_Heights = image_grayscale_to_dict("world_height_map_downscaled2.jpg")
tile_Size = 16
map_Size_X = 540
map_Size_Y = 270
screen_Size_X = tile_Size * map_Size_X
screen_Size_Y = tile_Size * map_Size_Y

#mountainize(tile_Heights, 10)
generate_height_map(height_Tiles, tile_Heights)
#generate_height_map(ground_Tiles, tile_Heights)
#generate_hills(ground_Tiles)
#fill_up_grass(ground_Tiles, 0)

screen = pygame.display.set_mode((screen_Size_X, screen_Size_Y))
render(height_Tiles)
#time.sleep(4)
#render(ground_Tiles)

save = input("Save this image? (y/n): ")
t = datetime.datetime.now().strftime("%G-%m-%d %H-%M-%S")
if save == "y": pygame.image.save(screen, os.path.join("saved images", t+".png"))
