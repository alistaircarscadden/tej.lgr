import cv2
import os
import shutil
from PIL import Image

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

def blow(src, dst, transparency):
    image = Image.open(src)
    blow = Image.new('P', (image.width, image.height))
    # 0 black 255 white 209 yellow
    for x in range(image.width):
        for y in range(image.height):
            if(transparency and image.getpixel((x, y)) == 209):
                blow.putpixel((x, y), 209)
            else:
                turn_white = image.getpixel((x, y)) == 255
                if(not turn_white):
                    num_whites_below = 0
                    for x_off, y_off in [(-1, 1), (0, 1), (1, 1)]:
                        _x_, _y_ = x + x_off, y + y_off
                        try:
                            if(image.getpixel((_x_, _y_)) == 255 or image.getpixel((_x_, _y_)) == 209):
                                num_whites_below += 1
                        except IndexError:
                            pass
                    turn_white = num_whites_below >= 1
                if(turn_white):
                    blow.putpixel((x, y), 255)
                else:
                    blow.putpixel((x, y), 0)


    blow.putpalette(image.getpalette())
    image.close()
    blow.save(dst)

# Make directories
try:
    os.mkdir('blow/QUPDOWN')
    os.mkdir('blow')
except FileExistsError:
    pass

# Copy all edit edj files to blow
for image in images:
    shutil.copy('edj/' + image[0], 'blow/' + image[0])

# Make blow images
for image in images:
    blow('blow/' + image[0], 'blow/' + image[0], image[1])

# Copy masks and .txt
for copy in just_copy:
    shutil.copy('edj/' + copy, 'blow/' + copy)
