import cv2
import os
import shutil
from PIL import Image

import paths

def blow(src, dst, transparency):
    image = Image.open(src)
    blow = Image.new('P', (image.width, image.height))
    # 0 black 255 white 209 yellow
    for x in range(image.width):
        for y in range(image.height):
            if(transparency and image.getpixel((x, y)) == 209):
                blow.putpixel((x, y), 209)
            else:
                turn_white = image.getpixel((x, y)) == 255
                if(not turn_white):
                    num_whites_below = 0
                    for x_off, y_off in [(-1, 1), (0, 1), (1, 1)]:
                        _x_, _y_ = x + x_off, y + y_off
                        try:
                            if(image.getpixel((_x_, _y_)) == 255 or image.getpixel((_x_, _y_)) == 209):
                                num_whites_below += 1
                        except IndexError:
                            pass
                    turn_white = num_whites_below >= 1
                if(turn_white):
                    blow.putpixel((x, y), 255)
                else:
                    blow.putpixel((x, y), 0)


    blow.putpalette(image.getpalette())
    image.close()
    blow.save(dst)

# Copy all edit edj files to blow
for image in paths.images:
    shutil.copy(paths.edj_dir + image[0], paths.blow_dir + image[0])

# Make blow images
for image in paths.images:
    print('{}{}'.format(paths.blow_dir, image[0]))
    blow(paths.blow_dir + image[0], paths.blow_dir + image[0], image[1])

# Copy masks and .txt
for copy in paths.just_copy:
    shutil.copy(paths.edj_dir + copy, paths.blow_dir + copy)
