import cv2
import os
import shutil
from PIL import Image, ImageFilter

images = [
    ['barrel.bmp', True],
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
          ['QUPDOWN/QUP_9.bmp', True]
    ]

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
    print('denoising: {}'.format(path))
    img_t = cv2.imread(path, 0)
    deno = cv2.fastNlMeansDenoising(img_t, None, 30, 7, 21)
    img2 = Image.fromarray(deno, mode='P')
    img2.putpalette(GREYSCALE_PALETTE)
    img2.save(path + '_dn.bmp')

for img in images:
    dajrk('default/' + img[0], 'dajrk/' + img[0], img[1])
##    denoise('dajrk/' + img[0])
    
for cpy in just_copy:
    shutil.copy('default/' + cpy, 'dajrk/' + cpy)







