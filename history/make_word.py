import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# def draw_ellipse(image, bounds, width=1, outline='white', antialias=4):
#     """Improved ellipse drawing function, based on PIL.ImageDraw."""

#     # Use a single channel image (mode='L') as mask.
#     # The size of the mask can be increased relative to the imput image
#     # to get smoother looking results. 
#     mask = Image.new(
#         size=[int(dim * antialias) for dim in image.size],
#         mode='L', color='black')
#     draw = ImageDraw.Draw(mask)

#     # draw outer shape in white (color) and inner shape in black (transparent)
#     for offset, fill in (width/-2.0, 'white'), (width/2.0, 'black'):
#         left, top = [(value + offset) * antialias for value in bounds[:2]]
#         right, bottom = [(value - offset) * antialias for value in bounds[2:]]
#         draw.ellipse([left, top, right, bottom], fill=fill)

#     # downsample the mask using PIL.Image.LANCZOS 
#     # (a high-quality downsampling filter).
#     mask = mask.resize(image.size, Image.LANCZOS)
#     # paste outline color to input image through the mask
#     image.paste(outline, mask=mask)


# for c in string :
font = ImageFont.truetype("code.ttf", 90, encoding="unic")
img=Image.new("RGBA", (150,150),(255,255,255,0))
draw = ImageDraw.Draw(img)
draw.text((30,30),"B",(0,0,0),font=font)
draw = ImageDraw.Draw(img)
# x = 50
# y=50
# r=50
# bound = [5, 19, 105, 119]
# draw_ellipse(img,bound, outline ='black',width=5)
# draw.ellipse((x-r, y-r, x+r, y+r), fill=(255,0,0,0))


img.save("A.png")