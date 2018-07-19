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
    greyscale.putpalette(GREYSCALE_PALETTE)
    greyscale.save(dajrkpath)

def smooth(image, iterations=1):
    def iteration(it_image):
        smoothed = it_image.copy()

        def neighbors(r):
            s = r // 2
            for i in range(r*r):
                yield i % r - s, i // r - s

        for x in range(image.width):
            for y in range(image.height):
                histogram = [0] * 256
                for x_off, y_off in neighbors(3):
                    _x_, _y_ = x + x_off, y + y_off
                    try: histogram[image.getpixel((_x_, _y_))] += 1
                    except IndexError: pass
                smoothed.putpixel((x, y),
                                  max(enumerate(histogram), key=lambda a: a[1])[0])

        return smoothed

    for i in range(iterations):
        image = iteration(image)

    return image

def denoise(path):
    kernel3 = np.ones((3,3),np.uint8)
    kernel5 = np.ones((5,5),np.uint8)
    img_t = cv2.imread(path, 0)
    #cv2.fastNlMeansDenoising(img_t, None, 30, 13, 21)
    deno = cv2.morphologyEx(img_t, cv2.MORPH_OPEN, kernel3)
    deno2 = cv2.morphologyEx(deno, cv2.MORPH_CLOSE, kernel5)
    img2 = Image.fromarray(deno2, mode='L')
    assert(img2 != None)
    return img2

for image in paths.images:
    print('{}{}'.format(paths.dajrk_dir, image[0]))
    dajrk(paths.default_dir + image[0], paths.dajrk_dir + image[0], image[1])
    smooth(denoise(paths.dajrk_dir + image[0]), iterations=2).save(paths.dajrk_dir + image[0])
    
for cpy in paths.just_copy:
    shutil.copy(paths.default_dir + cpy, paths.dajrk_dir + cpy)







