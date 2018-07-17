import cv2
import os
import shutil
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

def luminance(rgb):
    lum = int(0.2126*rgb[0] + 0.7152*rgb[1] + 0.0722*rgb[2])
    if(lum == 0):
        lum = 1
    return lum

def rgb_from_palette_index(index, palette):
    index *= 3
    return (palette[index], palette[index+1], palette[index+2])

def greyscale_palette():
    # m is a list of 256*3 RGB colours,
    # 255, 0, 0,  0, 0, 0,  2, 2, 2,  3, 3, 3 ... 255, 255, 255
    # first three will be transparency in elma (red)
    # then the next 255 will be greyscale (except 1, 1, 1)
    m = []
    m.extend([255, 0, 0])
    m.extend([0, 0, 0])
    for x in range(2, 256):
        m.extend([x, x, x])
    return m

def dajrk(defaultpath, dajrkpath, apply_transparency):
    default = Image.open(defaultpath)
    default_palette = default.getpalette()
    
    dajrk = Image.new(mode='P', size=(default.width, default.height))
    #dajrk.putpalette(greyscale_palette())
    dajrk.putpalette(default_palette)
    
    transparency_color = default.getpixel((0, 0))

    luminances = []
    for x in range(default.width):
        for y in range(default.height):
            defaultpx = default.getpixel((x, y))
            if(apply_transparency and defaultpx == transparency_color):
                pass
            else:
                lum = luminance(rgb_from_palette_index(defaultpx, default_palette))
                luminances.append(lum)
    luminances.sort()

    # Luminances bands
    q1 = luminances[len(luminances) // 4]
    q2 = luminances[len(luminances) // 4 * 2]
    q3 = luminances[len(luminances) // 4 * 3]
    
    for x in range(default.width):
        for y in range(default.height):
            defaultpx = default.getpixel((x, y))
            dajrkpx = 0
            if(apply_transparency and defaultpx == transparency_color):
                pass
            else:
                defaultpx_rgb = rgb_from_palette_index(defaultpx, default_palette)
                lum = luminance(defaultpx_rgb)

                if(q1 > lum):
                    dajrkpx = 25
                elif(q2 > lum):
                    dajrkpx = 17
                elif(q3 > lum):
                    dajrkpx = 52
                else:
                    dajrkpx = 36
            dajrk.putpixel((x, y), dajrkpx)

    dajrk.save(dajrkpath)

for img in images:
    dajrk('default/' + img[0], 'dajrk/' + img[0], img[1])
    
for cpy in just_copy:
    shutil.copy('default/' + cpy, 'dajrk/' + cpy)







