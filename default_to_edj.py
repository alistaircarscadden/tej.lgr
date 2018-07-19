import cv2
import os
import shutil
from PIL import Image

import paths
edjify = paths.images

force_border_edges = {
    'edj/barrel.bmp': ['left', 'right'],
    'edj/bridge.bmp': ['bottom'],
    'edj/flag.bmp': ['top'],
    'edj/secret.bmp': ['top']
    }

# Canny recommended values are lowThreshold = x, highThreshold = 3x
QUPDOWN_thresh = 200
canny_threshold = {
    'default': 100,

    # Standard
    'edj/bridge.bmp': 20,
    'edj/barrel.bmp': 50,
    'edj/log1.bmp': 30,
    'edj/ground.bmp': 49,
    'edj/Q1SUSP2.bmp': 30,
    'edj/Q1LEG.bmp': 50,
    'edj/sedge.bmp': 50,
    'edj/support1.bmp': 80,
    'edj/cliff.bmp': 36,
    'edj/secret.bmp': 350,
    'edj/brick.bmp': 116,

    # Objects
    #'edj/QEXIT.bmp': 50,
    ##'edj/QKILLER.bmp': 100,
    #'edj/qfood1.bmp': 12,
    #'edj/qfood2.bmp': 16,
    
    # Grass
    'edj/QUPDOWN/QDOWN_1.bmp': QUPDOWN_thresh,
    'edj/QUPDOWN/QDOWN_5.bmp': QUPDOWN_thresh,
    'edj/QUPDOWN/QDOWN_9.bmp': QUPDOWN_thresh,
    'edj/QUPDOWN/QDOWN_14.bmp': QUPDOWN_thresh,
    'edj/QUPDOWN/QDOWN_18.bmp': QUPDOWN_thresh,
    'edj/QUPDOWN/QUP_0.bmp': QUPDOWN_thresh,
    'edj/QUPDOWN/QUP_1.bmp': QUPDOWN_thresh,
    'edj/QUPDOWN/QUP_5.bmp': QUPDOWN_thresh,
    'edj/QUPDOWN/QUP_9.bmp': QUPDOWN_thresh,
    'edj/QUPDOWN/QUP_14.bmp': QUPDOWN_thresh,
    'edj/QUPDOWN/QUP_18.bmp': QUPDOWN_thresh,
    }

def edge_from_image(path, topath, apply_transparency):
    image = Image.open(path)

    threshold = canny_threshold[topath] if topath in canny_threshold else canny_threshold['default']
    
    edge_array = cv2.Canny(cv2.imread(path, 0), threshold, 3 * threshold)
    edge_image = Image.fromarray(edge_array, mode=image.mode)

    if(apply_transparency):
        transparency_color = image.getpixel((0, 0))
        for x in range(image.width):
            for y in range(image.height):
                # Top left pixel must be orange
                # Any pixel that is transparent in the original
                # and black in the edge version must be transparent
                # white pixels (edges) stay.
                if((x, y) == (0, 0) or
                   image.getpixel((x, y)) == transparency_color and 
                   edge_image.getpixel((x, y)) != 255):
                    edge_image.putpixel((x, y), 209)

        for x in range(image.width):
            for y in range(image.height):
                # If a pixel is black and has transparency beside
                # it, the edge detection failed to detect this edge
                # and we will force it to be white
                # (this happens, for example, in tree3 where the bg
                # is blue, and the top of the tree is light green)
                if(edge_image.getpixel((x, y)) == 0):
                    any_transparent = False
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    for x_off, y_off in directions:
                        _x_, _y_ = x + x_off, y + y_off
                        try:
                            if(edge_image.getpixel((_x_, _y_)) == 209):
                                any_transparent = True
                        except IndexError:
                            pass
                    if(any_transparent):
                        edge_image.putpixel((x, y), 255)

    force_borders = force_border_edges[topath] if topath in force_border_edges else []
    for border in force_borders:
        if(border == 'left' or border == 'right'):
            x = 0 if border == 'left' else edge_image.width - 1
            for y in range(edge_image.height):
                if(edge_image.getpixel((x, y)) == 0):
                    edge_image.putpixel((x, y), 255)
        if(border == 'top' or border == 'bottom'):
            y = 0 if border == 'top' else edge_image.height - 1
            for x in range(edge_image.width):
                if(edge_image.getpixel((x, y)) == 0):
                    edge_image.putpixel((x, y), 255)
    
    edge_image.putpalette(image.getpalette())
    edge_image.save(topath)

# Make edge images
for image in paths.edjify:
    edge_from_image(paths.default_dir + image[0], paths.edj_dir + image[0], image[1])

# Copy masks and .txt
for copy in paths.just_copy:
    shutil.copy(paths.default_dir + copy, paths.edj_dir + copy)

# Special rule: QGRASS.bmp should be white

# UNCOMMENT if building edj to .lgr,
# leave commented if building up to cedj...dejtaijl... etc

##qgrass = Image.open('edj/QGRASS.bmp')
##qgrass_w = Image.new(mode='P', size=(qgrass.width, qgrass.height), color=255)
##qgrass_w.putpalette(qgrass.getpalette())
##qgrass.close()
##qgrass_w.save('edj/QGRASS.bmp')
