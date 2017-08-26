import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import os
import cv2
import numpy as np
import logging

# From  https://stackoverflow.com/questions/32504246/draw-ellipse-in-python-pil-with-line-thickness
def draw_circle(image, bounds, width=1, outline='white', antialias=4):
    """Improved ellipse drawing function, based on PIL.ImageDraw."""    
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)
    for offset, fill in (width/-2.0, 'white'), (width/2.0, 'black'):
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        draw.ellipse([left, top, right, bottom], fill=fill)
    mask = mask.resize(image.size, Image.LANCZOS)
    image.paste(outline, mask=mask)

def draw_letter(letter):
    font = ImageFont.truetype("unicode.ttf", 75, encoding="unic")
    image=Image.new("RGBA", (200,200),(255,255,255,0))
    draw = ImageDraw.Draw(image)
    draw.text((70,45),letter,(0,0,0),font=font)
    draw = ImageDraw.Draw(image)
    image.save('temp.png')
    return image

def crop_circle(image):
    temp_img = cv2.imread('temp.png', 0)
    os.remove('temp.png')
    ret,thresh = cv2.threshold(temp_img,0,100,cv2.THRESH_BINARY_INV)
    _,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    cnt = contours[0]
    
    ### With Moments
    # M = cv2.moments(cnt)
    # cx = int(M['m10']/M['m00'])
    # cy = int(M['m01']/M['m00'])
    
    ### With Center
    x,y,w,h = cv2.boundingRect(cnt)
    cx = int(x+w/2)
    cy = int(y+h/2)
    radius = 45
    width=5
    circle = [int(cx)-radius,int(cy)-radius,int(cx)+radius,int(cy)+radius]
    draw_circle(image,circle, outline =(0,0,0),width=width)
    bound = (int(cx)-radius-width,int(cy)-radius-width,int(cx)+radius+width,int(cy)+radius+width)
    return image.crop(bound)



def setColor(im,R=255,G=255,B=255):
    data = np.array(im)
    # Clear, make all black pixel
    for i,alpha in enumerate(data[:,:,3]) :
        for j,v in enumerate(alpha) :
            if v != 0 :
                data[:,:,0],  data[:,:,1], data[:,:,2] =  0, 0, 0
    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    mask = (red == 0) & (green == 0) & (blue == 0)
    data[:,:,:3][mask] = [R, G, B]
    return Image.fromarray(data)

def draw_word(letter,path=''):
    letter = str(letter)
    file_name = letter + '.png'
    image = draw_letter(letter)
    image = crop_circle(image)
    image = setColor(image,190,190,190)
    image.save(path + file_name)


for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890+-' :
    try :
        draw_word(c,path='./result/')
    except :
        logging.warning('Directory not found, try to build \"result\"')
        os.mkdir('result')
        draw_word(c,path='./result/')