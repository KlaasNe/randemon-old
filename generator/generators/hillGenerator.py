# Calculates where to draw edges of hills
def create_hill_edges(pmap, layer, height_map, hill_type=0, update=False):
    # Determines which sprite to use at (x, y)
    def define_hill_edge_texture(cx, cy):
        # Looks for the tile heights around (x, y) and adds their relative height to an array. 1 means the tile is
        # situated higher than the central tile, 0 means equal height, -1 means lower
        def get_hills_around_tile():
            current_tile_height = height_map[(cx, cy)]
            hills_around_tile = []
            for around in range(0, 9):
                tile_coordinate = (cx + around % 3 - 1, cy + around // 3 - 1)
                curr_height = height_map.get(tile_coordinate, current_tile_height)
                if curr_height > current_tile_height:
                    hills_around_tile.append(1)
                elif curr_height < current_tile_height:
                    hills_around_tile.append(-1)
                elif curr_height == current_tile_height:
                    hills_around_tile.append(0)
            return hills_around_tile

        # using the array of relative heights, this calculates the sprite for the hill texture
        hills_around = get_hills_around_tile()
        h = 5 * hill_type
        if height_map.get((cx, cy), 0) < 2:
            return -1
        if hills_around[3] == 0 and hills_around[6] == -1 and hills_around[7] == 0:
            return "hi", 0 + h, 1
        if hills_around[5] == 0 and hills_around[7] == 0 and hills_around[8] == -1:
            return "hi", 0 + h, 2
        if hills_around[0] == -1 and hills_around[1] == 0 and hills_around[3] == 0:
            return "hi", 3 + h, 0
        if hills_around[1] == 0 and hills_around[2] == -1 and hills_around[5] == 0:
            return "hi", 3 + h, 0
        if hills_around[1] == 0 and hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == 0:
            return -1
        if hills_around[1] == 0 and hills_around[3] == -1 and hills_around[7] == 0:
            return "hi", 1 + h, 0
        if hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == -1:
            return "hi", 4 + h, 0
        if hills_around[1] == 0 and hills_around[5] == -1 and hills_around[7] == 0:
            return "hi", 2 + h, 0
        if hills_around[1] == -1 and hills_around[3] == 0 and hills_around[5] == 0:
            return "hi", 3 + h, 0
        if hills_around[1] == -1 and hills_around[3] == -1:
            return "hi", 1 + h, 1
        if hills_around[3] == -1 and hills_around[7] == -1:
            return "hi", 3 + h, 1
        if hills_around[5] == -1 and hills_around[7] == -1:
            return "hi", 4 + h, 1
        if hills_around[1] == -1 and hills_around[5] == -1:
            return "hi", 2 + h, 1
        return -1

    for y in range(0, layer.sy):
        for x in range(0, layer.sx):
            hill_edge_texture = define_hill_edge_texture(x, y)
            if hill_edge_texture != -1:
                if hill_edge_texture == ("hi", 3, 0) and height_map.get((x, y), -1) == pmap.highest_path + 1:
                    hill_edge_texture = ("hi", 0, 3)
                elif update and hill_edge_texture[1] in [1, 2, 3] \
                        and height_map.get((x, y), -1) > pmap.highest_path + 1:
                    hill_edge_texture = ("hi", hill_edge_texture[1], hill_edge_texture[2] + 2)

                if "ro" != layer.get_tile_type((x, y)) or layer.get_tile((x, y))[1] < 2:
                    if update:
                        layer.set_tile((x, y), hill_edge_texture)
                    elif (x, y) not in layer.get_ex_pos():
                        layer.set_tile((x, y), hill_edge_texture)
            elif layer.get_tile_type((x, y)) == "hi":
                layer.rm_tile((x, y))
