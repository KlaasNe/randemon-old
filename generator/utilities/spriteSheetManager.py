from os import path

from PIL import Image, ImageOps


class SpriteSheetReader:

    def __init__(self, image, margin=0):
        self.sprite_sheet = image
        self.margin = margin

    def get_tile(self, tile_x, tile_y, mirror, tile_s_x=16, tile_s_y=16):
        pos_x = (tile_s_x * tile_x) + (self.margin * (tile_x + 1))
        pos_y = (tile_s_y * tile_y) + (self.margin * (tile_y + 1))
        box = (pos_x, pos_y, pos_x + tile_s_x, pos_y + tile_s_y)
        return ImageOps.mirror(self.sprite_sheet.crop(box)) if mirror else self.sprite_sheet.crop(box)


class SpriteSheetWriter:

    def __init__(self, sprite_sheet, tile_s_x=16, tile_s_y=16):
        self.sprite_sheet = SpriteSheetReader(sprite_sheet)
        self.tile_s_x = tile_s_x
        self.tile_s_y = tile_s_y

    def get_tile(self, sheet_x, sheet_y, mirror=False):
        return self.sprite_sheet.get_tile(sheet_x, sheet_y, mirror, self.tile_s_x, self.tile_s_y)

    def draw_tile(self, image, draw_sheet, draw_x, draw_y):
        dest_box = (draw_x, draw_y, draw_x + self.tile_s_x, draw_y + self.tile_s_y)
        try:
            draw_sheet.paste(image, dest_box, mask=image)
        except ValueError:
            draw_sheet.paste(image, dest_box)
        except Exception as e:
            print(e)


class DrawSheet:

    def __init__(self, sheet_size_x, sheet_size_y):
        self.sheet_size_x = sheet_size_x
        self.sheet_size_y = sheet_size_y
        self.draw_sheet = Image.new("RGBA", (self.sheet_size_x, self.sheet_size_y), (0, 0, 0, 0))

    def drawable(self):
        return self.draw_sheet

    def show(self):
        self.draw_sheet.show()

    def close(self):
        self.draw_sheet.close()

    def save(self, name):
        self.draw_sheet.save(path.join("saved images", name + ".png"), "png")

    def save_split(self, name, x_split, y_split):
        size_x, size_y = self.sheet_size_x // x_split, self.sheet_size_y // y_split
        for y in range(y_split):
            for x in range(x_split):
                box = (x * size_x, y * size_y, (x + 1) * size_x, (y + 1) * size_y)
                self.draw_sheet.crop(box).save(path.join("saved images", name + str((x, y)) + ".png"), "png")
