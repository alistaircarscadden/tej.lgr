import cv2
import numpy as np
import os
import shutil
from PIL import Image, ImageFilter

import paths

def luminance(rgb):
    lum = int(0.2126*rgb[0] + 0.7152*rgb[1] + 0.0722*rgb[2])
    if(lum == 0):
        lum = 1
    return lum

def rgb_from_palette_index(index, palette):
    index *= 3
    return (palette[index], palette[index+1], palette[index+2])

def greyscale_palette():
    m = []
    for x in range(0, 256):
        m.extend([x, x, x])
    return m

def contiguous_palette(palette):
    cont = []
    for x in range(0, 256*3, 3):
        cont.append(palette[x])
    for x in range(1, 256*3, 3):
        cont.append(palette[x])
    for x in range(2, 256*3, 3):
        cont.append(palette[x])
    print(len(palette))
    print(len(cont))
    return cont

GREYSCALE_PALETTE = greyscale_palette()

def dajrk(defaultpath, dajrkpath, apply_transparency):
    default = Image.open(defaultpath)
    greyscale = default.convert(mode='L')
    greyscale.putpalette(default.getpalette())

    if(apply_transparency):
        transparent = default.getpixel((0, 0))
        for x in range(default.width):
            for y in range(default.height):
                if(greyscale.getpixel((x, y)) == 209):
                    greyscale.putpixel((x, y), 210)
                if(default.getpixel((x, y)) == transparent):
                    greyscale.putpixel((x, y), 209)
            
    greyscale.save(dajrkpath)

def denoise(path):
    kernel = np.ones((5,5),np.uint8)
    img_t = cv2.imread(path, 0)
    #deno = cv2.fastNlMeansDenoising(img_t, None, 30, 13, 21)
    deno = cv2.morphologyEx(img_t, cv2.MORPH_OPEN, kernel)
    img2 = Image.fromarray(deno, mode='P')
    img2.putpalette(GREYSCALE_PALETTE)
    return img2

for img in paths.images:
    dajrk(paths.default_dir + img[0], paths.dajrk_dir + img[0], img[1])
    denoise(paths.dajrk_dir + img[0]).save(paths.dajrk_dir + img[0])
    
for cpy in paths.just_copy:
    shutil.copy(paths.default_dir + cpy, paths.dajrk_dir + cpy)







