import cv2
import os
import shutil
from PIL import Image

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

for img in paths.images:
    print('{}{}'.format(paths.psych_dir, image[0]))
    dajrk(paths.default_dir + img[0], paths.dajrk_dir + img[0], img[1])
    
for cpy in paths.just_copy:
    shutil.copy(paths.default_dir + cpy, paths.dajrk_dir + cpy)







