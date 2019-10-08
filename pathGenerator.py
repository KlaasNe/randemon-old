import math


def apply_path_sprites(layer, map_size_x, map_size_y):
    from mapGenerator2 import out_of_bounds

    def calculate_path_sprite(x, y):
        tiles_around = []
        for around in range(0, 9):
            path_around = layer.get((x + (around % 3) - 1, y + math.floor(around / 3) - 1), 0)
            # if path_around == 0: path_around = house_Tiles.get((x + (around % 3) - 1, y + math.floor(around / 3) - 1), 0)
            if "p_" in str(path_around) or "b_" in str(path_around) or "pl_" in str(path_around) or "sta_" in str(
                    path_around) or "m_4_p" in str(path_around) or "pd_" in str(path_around) or out_of_bounds(
                    x + (around % 3) - 1, y + math.floor(around / 3) - 1) or "mrk" in str(path_around):
                tiles_around.append(1)
            else:
                tiles_around.append(0)
        if tiles_around == [1, 1, 1, 1, 1, 1, 0, 1, 1]:
            return "_9"
        elif tiles_around == [1, 1, 1, 1, 1, 1, 1, 1, 0]:
            return "_10"
        elif tiles_around == [1, 1, 0, 1, 1, 1, 1, 1, 1]:
            return "_11"
        elif tiles_around == [0, 1, 1, 1, 1, 1, 1, 1, 1]:
            return "_12"
        elif tiles_around == [1, 1, 1, 1, 1, 1, 1, 1, 1] or (
                tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1):
            return "_0"
        elif tiles_around == [0, 1, 1, 0, 1, 1, 0, 1, 1] or tiles_around == [1, 1, 1, 0, 1, 1, 0, 1,
                                                                             1] or tiles_around == [0, 1, 1, 0, 1, 1, 1,
                                                                                                    1,
                                                                                                    1] or tiles_around == [
            1, 1, 1, 0, 1, 1, 1, 1, 1]:
            return "_1"
        elif tiles_around == [1, 1, 1, 1, 1, 1, 0, 0, 0] or tiles_around == [1, 1, 1, 1, 1, 1, 1, 0,
                                                                             0] or tiles_around == [1, 1, 1, 1, 1, 1, 0,
                                                                                                    0,
                                                                                                    1] or tiles_around == [
            1, 1, 1, 1, 1, 1, 1, 0, 1]:
            return "_2"
        elif tiles_around == [1, 1, 0, 1, 1, 0, 1, 1, 0] or tiles_around == [1, 1, 1, 1, 1, 0, 1, 1,
                                                                             0] or tiles_around == [1, 1, 0, 1, 1, 0, 1,
                                                                                                    1,
                                                                                                    1] or tiles_around == [
            1, 1, 1, 1, 1, 0, 1, 1, 1]:
            return "_3"
        elif tiles_around == [0, 0, 0, 1, 1, 1, 1, 1, 1] or tiles_around == [1, 0, 0, 1, 1, 1, 1, 1,
                                                                             1] or tiles_around == [0, 0, 1, 1, 1, 1, 1,
                                                                                                    1,
                                                                                                    1] or tiles_around == [
            1, 0, 1, 1, 1, 1, 1, 1, 1]:
            return "_4"
        elif tiles_around[5] == 1 and tiles_around[7] == 1 and tiles_around[8] == 1:
            return "_5"
        elif tiles_around[1] == 1 and tiles_around[2] == 1 and tiles_around[5] == 1:
            return "_6"
        elif tiles_around[0] == 1 and tiles_around[1] == 1 and tiles_around[3] == 1:
            return "_7"
        elif tiles_around[3] == 1 and tiles_around[6] == 1 and tiles_around[7] == 1:
            return "_8"
        return "_er"

    for x in range(0, map_size_x):
        for y in range(0, map_size_y):
            if (x, y) in layer and "p_" in layer[(x, y)]:
                path = calculate_path_sprite(x, y)
                if not path == "_er":
                    layer[(x, y)] = str(layer[(x, y)]) + str(path)
                else:
                    layer[(x, y)] = "g_0"

    # finish_path_edges(decoration_Tiles)