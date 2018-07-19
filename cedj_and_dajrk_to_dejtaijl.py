import cv2
import os
import shutil
import colorsys
import numpy
from PIL import Image

import paths

blue_transparency = list(map(lambda s: paths.cedj_dir + s, [
    'cliff.bmp',
    'flag.bmp',
    'log1.bmp',
    'log2.bmp',
    'Q2FORARM.bmp',
    'Q2THIGH.bmp',
    ]))

shade_amount = {
    'default': [4, 64],
    'dejtaijl/stone1.bmp': [1, 256],
    'dejtaijl/sky.bmp': [1, 0],
    'dejtaijl/sedge.bmp': [2, 256],
    'dejtaijl/bridge.bmp': [2, 256],
    'dejtaijl/tree1.bmp': [2, 256],
    'dejtaijl/tree2.bmp': [2, 256],
    'dejtaijl/tree3.bmp': [2, 256],
    'dejtaijl/tree4.bmp': [2, 256],
    'dejtaijl/tree5.bmp': [2, 256],
    }

def change_value(rgb, value):
    col = list(colorsys.rgb_to_hsv(rgb[0] / 256.0, rgb[1] / 256.0, rgb[2] / 256.0))
    col[2] += value / 256.0
    if(col[2] < 0): col[2] = 0
    if(col[2] > 1): col[2] = 1
    col = colorsys.hsv_to_rgb(col[0], col[1], col[2])
    return tuple(map(int, (col[0] * 256.0, col[1] * 256.0, col[2] * 256.0)))

def get_medians(dajrk, cedj, apply_transparency):
    lumis = []
    for x in range(dajrk.width):
        for y in range(dajrk.height):
            if(not apply_transparency or cedj.getpixel((x, y)) != 209):
                lumis.append(dajrk.getpixel((x, y)))
    lumis.sort()
    return {
        'Q1': lumis[len(lumis)//4 * 1],
        'Q2': lumis[len(lumis)//4 * 2],
        'Q3': lumis[len(lumis)//4 * 3]
        }

def dejtaijl(cedjpath, dajrkpath, apply_transparency, dejtaijlpath):
    _cedj = Image.open(cedjpath)
    cedj = _cedj.convert(mode='RGB')
    dajrk = Image.open(dajrkpath)
    medians = get_medians(dajrk, _cedj, apply_transparency)
    dejtaijl = Image.new(mode='RGB', size=(cedj.width, cedj.height))

    for x in range(dejtaijl.width):
        for y in range(dejtaijl.height):
            dajrkpx = dajrk.getpixel((x, y))
            cedjpx = cedj.getpixel((x, y))
            _cedjpx = _cedj.getpixel((x, y))
            px = None
            if(apply_transparency and _cedjpx == 209):
                px = (0, 0, 255) if cedjpath in blue_transparency else (255, 166, 32)
            elif(_cedjpx == 0):
                px = (0, 0, 0)
            else:
                divis = shade_amount[dejtaijlpath if dejtaijlpath in shade_amount else 'default'][0]
                clamp = shade_amount[dejtaijlpath if dejtaijlpath in shade_amount else 'default'][1]
                value_diff = max(-clamp, min(clamp, dajrkpx-medians['Q2']/divis))
                px = change_value(cedjpx,  value_diff)
            dejtaijl.putpixel((x, y), px)
            
    dejtaijl.save(dejtaijlpath)

for image in paths.images:
    print('{}{}'.format(paths.dejtaijl_dir, image[0]))
    dejtaijl(paths.cedj_dir + image[0], paths.dajrk_dir + image[0], image[1], paths.dejtaijl_dir + image[0])

for cpy in paths.just_copy:
    shutil.copy(paths.default_dir + cpy, paths.dejtaijl_dir + cpy)
