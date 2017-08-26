
from PIL import Image, ImageDraw, ImageFont
import numpy as np
class Model():

    def __init__(self,width=3000, height=3000, total_quest=10, font_color=(190,190,190,255)) :
        self.count = 0
        self.padding = 50
        self.font_size = 100
        self.width = width
        self.height = height
        self.questBlock = []
        self.total_quest = total_quest
        self.font_color = font_color
        self.font = ImageFont.truetype("unicode.ttf", self.font_size, encoding="unic")
        self.canvas = Image.new( "RGBA", (self.width,self.height) )
        # self.canvas = Image.new( "RGBA", (self.width,self.height),'white' )


    def questNum(self):
        self.count += 1
        yield '{:0>2}\n'.format( str(self.count) )

    def questRect(self,num,sequence,location,maxH = 100):
        temp = []
        
        files = ['result/{}.png'.format(c) for c in sequence ]
        images = list(map(Image.open, files))
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)
        assert max_height == maxH , 'Make Sure the size of result/*.png'
        total_height = num * max_height

        option = Image.new('RGBA', (total_width, total_height),(255,255,255,0))
        
        y_offset = 0
        for quest in range(num):
            block = []
            x_offset = 0
            for im in images:
                option.paste(im, (x_offset,y_offset))
                block.append((x_offset,y_offset))
                x_offset += im.size[0]
            temp.append(block)
            y_offset += max_height
            
        
        print(np.array(temp) + location)
        model.paste(option,location)


    def drawText(self,text,location=(0,0)):
        draw = ImageDraw.Draw( self.canvas )
        draw.text( (location), text, font=self.font, fill=self.font_color )
        self.canvas.save( "test.png" )


    def border(self,offset=10, width=3):
        draw = ImageDraw.Draw( self.canvas )
        cor = (0,0,self.width,self.height)
        cor = (offset,offset, self.width-offset,self.height-offset)
        
        for i in range(width):
            draw.rectangle(cor ,outline=(0,0,0))   
            cor = (cor[0]+1,cor[1]+1, cor[2]-1,cor[3]-1) 
        self.canvas.save( "test.png" )
        
    # 學號格
    def studentID(self,digits):
        self.drawText('學',location=(self.padding,200))
        self.drawText('號',location=(self.padding,400))
        self.questRect(digits,'1234567890',(200,self.padding))
        
    def testID(self):
        offset = int(self.width/2)
        self.drawText('考',location=(offset + self.padding,150))
        self.drawText('卷',location=(offset + self.padding,250))
        self.drawText('編',location=(offset + self.padding,350))
        self.drawText('號',location=(offset + self.padding,450))
        self.questRect(1,'ABCDEFGHIJ',(offset + 200,self.padding))
        self.questRect(5,'1234567890',(offset + 200,100+self.padding))

    def quest(self,type='EN'):
        location = (self.padding, 750+ (self.count)*(self.font_size+10))
        self.drawText(''.join(self.questNum()), location=location )
        self.questRect(1,'ABCD',(200, int(self.padding/2) + location[1]))
        
        
    def paste(self, image, location):
        self.canvas.paste(image,location)
        self.canvas.save( "test.png" )

    def setAnswer(self):
        pass



# Test
# model = Model()
# model.question(10,10,type='EN')
# model.question(5,10,type='TEST')
# # model.question(20,20)
# model.question(10,10,type='NUM')
# model.question(10,10,type='ENL')
# # model.question(6,7,type='NUM')
# # model.question(2,17,type='EN')
# model.border()




model = Model()
model.studentID(6)
model.testID()
for i in range(20) :
    model.quest()
model.border()


# 學號


# model.question(6,10,type='NUM')
# # 考卷編號  （）
# model.question(1,5,type='EN')
# model.question(5,10,type='NUM')

# model.question(20,4,type='EN')
# model.question(10,10,type='EN')
# model.question(16,4,type='EN')
# model.border()