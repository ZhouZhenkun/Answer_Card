from PIL import Image,ImageDraw

sequence = 'ABCDEFGHI'


def drawing(image,text,location=(0,0)):
    draw = ImageDraw.Draw( image )
    font_size = 100
    font = ImageFont.truetype("unicode.ttf", font_size, encoding="unic")
    draw.text( (location), text, font=font, fill=(190,190,190)) 

# num is number of questions
def quest_block(num,sequence):
    files = ['./result/{}.png'.format(c) for c in sequence ]
    images = list(map(Image.open, files))
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)
    total_height = num * max_height

    option = Image.new('RGBA', (total_width, total_height),(255,255,255,0))

    for quest in range(num):
        y_offset = max_height*quest
        x_offset = 0
        for im in images:
            option.paste(im, (x_offset,y_offset))
            x_offset += im.size[0]

    option.save('block.png',"PNG")
    print('Block Size:',option.size)
    return option

quest_block(3,sequence)