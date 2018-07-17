import cv2
import os
import shutil
from PIL import Image

edjify = [
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

def edge_from_image(path, topath, apply_transparency):
    image = Image.open(path)
    edge_array = cv2.Canny(cv2.imread(path, 0), 100, 110)
    edge_image = Image.fromarray(edge_array, mode=image.mode)

    if(apply_transparency):
        transparency_color = image.getpixel((0, 0))
        for x in range(image.width):
            for y in range(image.height):
                if(image.getpixel((x, y)) == transparency_color and edge_image.getpixel((x, y)) != 255):
                    edge_image.putpixel((x, y), 209)

    edge_image.putpalette(image.getpalette())
    edge_image.save(topath)

# Make directories
try:
    os.mkdir('edj/QUPDOWN')
    os.mkdir('edj')
except FileExistsError:
    pass

# Make edge images
for image in edjify:
    edge_from_image('default/' + image[0], 'edj/' + image[0], image[1])

# Copy masks and .txt
for copy in just_copy:
    shutil.copy('default/' + copy, 'edj/' + copy)
