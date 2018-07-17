import cv2
import os
import shutil
import colorsys
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

def change_value(rgb, value):
    # Adds value to colour's existing value
    col = colorsys.rgb_to_hsv(rgb[0] / 256.0, rgb[1] / 256.0, rgb[2] / 256.0)
    col[2] += value / 256.0
    if(col[2] < 0):
        col[2] = 0
    if(col[2] > 1):
        col[2] = 1
    col = colorsys.hsv_to_rgb(col[0], col[1], col[2])
    return [col[0] * 256.0, col[1] * 256.0, col[2] * 256.0]

def dejtaijl(cedjpath, dajrkpath, apply_transparency, dejtaijlpath):
    _cedj = Image.open(cedjpath)
    cedj = _cedj.convert(mode='RGB', palette=_cedj.getpalette())
    dajrk = Image.open(dajrkpath) # Transparent 0, lum 63 127 191 255

    dejtaijl = Image.new(mode='RGB', size=(cedj.width, cedj.height))

    for x in range(dejtaijl.width):
        for y in range(dejtaijl.height):
            dajrkpx = dajrk.getpixel((x, y))
            cedjpx = cedj.getpixel((x, y))
            dejtaijlpx = None

            print(cedjpx)
                    
                
    





