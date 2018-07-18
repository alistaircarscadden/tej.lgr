import cv2
import os
import shutil
import colorsys
import numpy
from PIL import Image

images = [['barrel.bmp', True],
          ['brick.bmp', False],
          ['bridge.bmp', True],
          ['bush1.bmp', True],
          ['bush2.bmp', True],
          ['bush3.bmp', True],
          ['cliff.bmp', True],
          ['edge.bmp', True],
          ['flag.bmp', True],
          ['ground.bmp', False],
          ['hang.bmp', True],
          ['log1.bmp', True],
          ['log2.bmp', True],
          ['mushroom.bmp', True],
          ['plantain.bmp', True],
          ['Q1BIKE.bmp', True],
          ['Q1BODY.bmp', True],
          ['Q1FORARM.bmp', True],
          ['Q1HEAD.bmp', True],
          ['Q1LEG.bmp', True],
          ['Q1SUSP1.bmp', True],
          ['Q1SUSP2.bmp', True],
          ['Q1THIGH.bmp', True],
          ['Q1UP_ARM.bmp', True],
          ['Q1WHEEL.bmp', True],
          ['Q2BIKE.bmp', True],
          ['Q2BODY.bmp', True],
          ['Q2FORARM.bmp', True],
          ['Q2HEAD.bmp', True],
          ['Q2LEG.bmp', True],
          ['Q2SUSP1.bmp', True],
          ['Q2SUSP2.bmp', True],
          ['Q2THIGH.bmp', True],
          ['Q2UP_ARM.bmp', True],
          ['Q2WHEEL.bmp', True],
          ['QCOLORS.bmp', False],
          ['QEXIT.bmp', True],
          ['QFLAG.bmp', True],
          ['qfood1.bmp', True],
          ['qfood2.bmp', True],
          ['QFRAME.bmp', False],
          ['QGRASS.bmp', False],
          ['QKILLER.bmp', True],
          ['secret.bmp', True],
          ['sedge.bmp', True],
          ['sky.bmp', False],
          ['st3top.bmp', True],
          ['stone1.bmp', False],
          ['stone2.bmp', False],
          ['stone3.bmp', False],
          ['supphred.bmp', True],
          ['support1.bmp', True],
          ['support2.bmp', True],
          ['support3.bmp', True],
          ['suppvred.bmp', True],
          ['susp.bmp', True],
          ['suspdown.bmp', True],
          ['suspup.bmp', True],
          ['tree1.bmp', True],
          ['tree2.bmp', True],
          ['tree3.bmp', True],
          ['tree4.bmp', True],
          ['tree5.bmp', True],
          ['QUPDOWN/QDOWN_1.bmp', True],
          ['QUPDOWN/QDOWN_14.bmp', True],
          ['QUPDOWN/QDOWN_18.bmp', True],
          ['QUPDOWN/QDOWN_5.bmp', True],
          ['QUPDOWN/QDOWN_9.bmp', True],
          ['QUPDOWN/QUP_0.bmp', True],
          ['QUPDOWN/QUP_1.bmp', True],
          ['QUPDOWN/QUP_14.bmp', True],
          ['QUPDOWN/QUP_18.bmp', True],
          ['QUPDOWN/QUP_5.bmp', True],
          ['QUPDOWN/QUP_9.bmp', True]]

just_copy = [
    'maskbig.bmp',
    'maskhor.bmp',
    'masklitt.bmp',
    'masktop.bmp',
    'lgr.txt',
]

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
            px = dajrk.getpixel((x, y))
            if(px != 209):
                lumis.append(px)
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
            if(_cedjpx == 0):
                px = (0, 0, 0)
            elif(dajrkpx < medians['Q1']):
                px = change_value(cedjpx, -32)
            else:#(dajrkpx < medians['Q3']):
                px = cedjpx
            #else:
            #    px = change_value(cedjpx, 32)

            dejtaijl.putpixel((x, y), px)

    dejtaijl2 = dejtaijl.quantize(palette=palette)

    if(apply_transparency):
        for x in range(dejtaijl2.width):
            for y in range(dejtaijl2.height):
                if(_cedj.getpixel((x, y)) == 209):
                    dejtaijl2.putpixel((x, y), 209)
    
    dejtaijl2.save(dejtaijlpath)

def save(dejtaijlpath, dejtaijl2path):
    palette = Image.open('default/sedge.bmp').getpalette()
    dejtaijlpng = Image.open(dejtaijlpath)
    dej = dejtaijlpng.quantize(palette=palette)
    dej.save(dejtaijl2path)

palette = palette_img_from_img('cedj/sedge.bmp')
for img in images:
    dejtaijl('cedj/' + img[0], 'dajrk/' + img[0], img[1], 'dejtaijl/' + img[0], palette)

for cpy in just_copy:
    shutil.copy('default/' + cpy, 'dejtaijl/' + cpy)

