import cv2
import os
import shutil
import colorsys
import numpy
from PIL import Image

import paths

def palette_img_from_img(path):
    p = Image.open(path).getpalette()
    test = Image.new(mode='P', size=(16, 16))
    test.putpalette(p)
    for n in range(256):
        test.putpixel((n % 16, n // 16), n)
    return test

def change_value(rgb, value):
    # Adds value to colour's existing value
    col = list(colorsys.rgb_to_hsv(rgb[0] / 256.0, rgb[1] / 256.0, rgb[2] / 256.0))
    col[2] += value / 256.0
    if(col[2] < 0):
        col[2] = 0
    if(col[2] > 1):
        col[2] = 1
    col = colorsys.hsv_to_rgb(col[0], col[1], col[2])
    return tuple(map(int, (col[0] * 256.0, col[1] * 256.0, col[2] * 256.0)))

def get_medians(dajrk):
    lumis = []
    for x in range(dajrk.width):
        for y in range(dajrk.height):
            lumis.append(dajrk.getpixel((x, y)))
    lumis.sort()
    return {
        'Q1': lumis[len(lumis)//4 * 1],
        'Q2': lumis[len(lumis)//4 * 2],
        'Q3': lumis[len(lumis)//4 * 3]
    }

def dejtaijl(cedjpath, dajrkpath, apply_transparency, dejtaijlpath, palette):
    print(dejtaijlpath)
    _cedj = Image.open(cedjpath)
    _cedjpal = _cedj.getpalette()
    cedj = _cedj.convert(mode='RGB')
    dajrk = Image.open(dajrkpath)

    medians = get_medians(dajrk)

    dejtaijl = Image.new(mode='RGB', size=(cedj.width, cedj.height))

    for x in range(dejtaijl.width):
        for y in range(dejtaijl.height):
            dajrkpx = dajrk.getpixel((x, y))
            cedjpx = cedj.getpixel((x, y))
            _cedjpx = _cedj.getpixel((x, y))

            px = None
            if(apply_transparency and _cedjpx == 209):
                px = (255, 166, 32)
            elif(_cedjpx == 0):
                px = (0, 0, 0)
            elif(dajrkpx < medians['Q1']):
                px = change_value(cedjpx, -32)
            elif(dajrkpx < medians['Q3']):
                px = cedjpx
            else:
                px = change_value(cedjpx, 32)

            dejtaijl.putpixel((x, y), px)

#### Originally planned on this conversion to 'P' image using quantize,
#### however the results were not good. Instead, I am saving the bmps as
#### RGB and allowing sunl's tool to map to the palette, which does a much
#### better job.
##    dejtaijl2 = dejtaijl.quantize(palette=palette)
##
##    if(apply_transparency):
##        for x in range(dejtaijl2.width):
##            for y in range(dejtaijl2.height):
##                if(_cedj.getpixel((x, y)) == 209):
##                    dejtaijl2.putpixel((x, y), 209)
##    
##    dejtaijl2.save(dejtaijlpath)
    dejtaijl.save(dejtaijlpath)

palette = palette_img_from_img(paths.cedj_dir + 'sedge.bmp')
for img in paths.images:
    dejtaijl(paths.cedj_dir + img[0], paths.dajrk_dir + img[0], img[1], paths.dejtaijl_dir + img[0], palette)

for cpy in paths.just_copy:
    shutil.copy(paths.default_dir + cpy, paths.dejtaijl_dir + cpy)

