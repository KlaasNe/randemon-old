import os

from .spriteSheetManager import *


def render2(layer, draw_sheet):
    def try_get_tile(curr_tile):
        try:
            img = sheet_writer.get_tile(curr_tile[1], curr_tile[2], curr_tile[3])
        except IndexError:
            img = sheet_writer.get_tile(curr_tile[1], curr_tile[2])
        return img

    previous_tile, previous_img = None, None
    for sw_name in sheet_writers.keys():
        sheet_writer = sheet_writers[sw_name]
        for tile_x, tile_y in layer.get_ex_pos():
            current_tile = layer.get_tile((tile_x, tile_y))
            if sw_name == current_tile[0]:
                if current_tile != previous_tile:
                    try:
                        tile_img = try_get_tile(current_tile)
                        sheet_writer.draw_tile(tile_img, draw_sheet, tile_x * 16, tile_y * 16)
                        previous_tile, previous_img = layer.get_tile((tile_x, tile_y)), tile_img
                    except KeyError:
                        pass
                else:
                    sheet_writer.draw_tile(previous_img, draw_sheet, tile_x * 16, tile_y * 16)


def render_npc(pmap, layer, draw_sheet):
    def try_get_tile(curr_tile):
        try:
            img = sheet_writer.get_tile(curr_tile[1], curr_tile[2], curr_tile[3])
        except IndexError:
            img = sheet_writer.get_tile(curr_tile[1], curr_tile[2])
        return img

    previous_tile, previous_img = None, None
    sheet_writer = SpriteSheetWriter(Image.open(os.path.join("resources", "npc.png")), 20, 23)
    for tile_x, tile_y in getattr(pmap, layer).keys():
        current_tile = pmap.get_tile(layer, tile_x, tile_y)
        if current_tile != previous_tile:
            try:
                tile_img = try_get_tile(current_tile)
                sheet_writer.draw_tile(tile_img, draw_sheet, tile_x * 16, tile_y * 16 - 7)
                previous_tile, previous_img = pmap.get_tile(layer, tile_x, tile_y), tile_img
            except KeyError:
                pass
        else:
            sheet_writer.draw_tile(previous_img, draw_sheet, tile_x * 16, tile_y * 16 - 7)


sheet_writers = {
    "pa": SpriteSheetWriter(Image.open(os.path.join("resources", "path.png"))),
    "wa": SpriteSheetWriter(Image.open(os.path.join("resources", "water.png"))),
    "na": SpriteSheetWriter(Image.open(os.path.join("resources", "nature.png"))),
    "hi": SpriteSheetWriter(Image.open(os.path.join("resources", "hills.png"))),
    "ro": SpriteSheetWriter(Image.open(os.path.join("resources", "road.png"))),
    "ho": SpriteSheetWriter(Image.open(os.path.join("resources", "houses.png"))),
    "fe": SpriteSheetWriter(Image.open(os.path.join("resources", "fences.png"))),
    "po": SpriteSheetWriter(Image.open(os.path.join("resources", "pokemon.png"))),
    "de": SpriteSheetWriter(Image.open(os.path.join("resources", "decoration.png"))),
    "ra": SpriteSheetWriter(Image.open(os.path.join("resources", "rain.png")))
}
