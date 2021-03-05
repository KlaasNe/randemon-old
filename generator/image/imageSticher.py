import os, pygame, datetime

x_Images = 3
y_Images = 2
x_Size_Image = 68 * 16
y_Size_Image = 120 * 16

screen = pygame.display.set_mode((x_Images * x_Size_Image, y_Images * y_Size_Image))

for image in range(x_Images * y_Images):
    if image < 10:
        image_Number = "0" + str(image)
    else:
        image_Number = str(image)

    try:
        screen.blit(pygame.image.load(os.path.join("../saved images", image_Number + ".png")), (x_Size_Image * (image % x_Images), y_Size_Image * (image // x_Images)))
    except Exception as e:
        print(e)

pygame.display.update()

save = input("Save this image? (y/n): ")
t = datetime.datetime.now().strftime("%G-%m-%d %H-%M-%S")
if save == "y":
    pygame.image.save(screen, os.path.join("../saved images", t + ".png"))
