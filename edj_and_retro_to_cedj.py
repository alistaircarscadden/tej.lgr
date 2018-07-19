import cv2
import os
import shutil
from PIL import Image

import paths

def cedj(retropath, edjpath, apply_transparency, cedjpath):
    retro = Image.open(retropath)
    edj = Image.open(edjpath)
    cedj = Image.new(mode='P', size=(retro.width, retro.height))

    for x in range(cedj.width):
        for y in range(cedj.height):
            edjpx = edj.getpixel((x, y))
            retropx = retro.getpixel((x, y))

            if(apply_transparency and edjpx == 209):
                cedjpx = edjpx
            elif(edjpx == 255):
                cedjpx = 0
            else:
                cedjpx = retropx

            cedj.putpixel((x, y), cedjpx)

    cedj.putpalette(retro.getpalette())
    cedj.save(cedjpath)

# Make edge images
for image in paths.images:
    print('{}{}'.format(paths.cedj_dir, image[0]))
    cedj(paths.tejtro_dir + image[0], paths.edj_dir + image[0], image[1], paths.cedj_dir + image[0])

# Copy masks and .txt
for copy in paths.just_copy:
    shutil.copy(paths.default_dir + copy, paths.cedj_dir + copy)
