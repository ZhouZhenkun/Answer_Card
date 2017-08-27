
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import check
class Model():

    def __init__(self,width=4500, height=4000, font_color=(190,190,190,255)) :
        self.count = 0
        self.padding = 50
        self.font_size = 120
        self.width = width
        self.height = height
        self.font_color = font_color
        self.font = ImageFont.truetype("unicode.ttf", self.font_size, encoding="unic")
        self.canvas = Image.new( "RGBA", (self.width,self.height) )
        self.draw = ImageDraw.Draw( self.canvas )
        self.questInit()
        self.questStart = None


    def drawText(self,text,location=(0,0)):
        self.draw.text( (location), text, font=self.font, fill=self.font_color )

    def questInit(self, x=0, y=0) :
        self.quest_left = x
        self.quest_up = y
        self.quest_right = 0 
        self.quest_down = 0

    def questBorderX(self,x=0):
        if self.quest_right < x :
            self.quest_right = x
        
    def questBorderY(self,y=0):
        if self.quest_down < y :
            self.quest_down = y
            print(self.quest_down)

    def questNum(self):
        self.count += 1
        yield '{:0>2}\n'.format( str(self.count) )


    def optionChain(self,sequence,pic_size=120):
        self.pic_size = pic_size
        files = ['result/{}.png'.format(c) for c in sequence ]
        images = list(map(Image.open, files))
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)
        assert max_height == pic_size and total_width == (len(sequence) * pic_size), 'Make Sure the size of result/*.png is {}x{}'.format(self.pic_size,self.pic_size)
        option = Image.new('RGBA', (total_width, max_height),(255,255,255,0))
        x = 0
        block = []
        for im in images:
            option.paste(im, (x,0))
            block.append((x,0))
            x += im.size[0]
        self.questBorderX(x)
        print('Now X Border is :',self.quest_right)
        return option,np.array(block)


    def optionRect(self,num,sequence,location):
        if num == 0 : 
            return
        options, blockX = self.optionChain(sequence)
        temp = Image.new('RGBA', ((len(sequence) * self.pic_size), num*self.pic_size),(255,255,255,0))
        block = []
        y_offset = 0
        for quest in range(num):
            temp.paste(options, (0,y_offset))
            block.append(blockX + (0,y_offset))
            y_offset += self.pic_size

        self.questBorderX(self.quest_right + location[0])
        self.questBorderY(y_offset + location[1])
        block = np.array(block) + location
        print(block)
        self.paste(temp,location)
        return temp,block


    def border(self,offset=10, width=10):
        cor = (0,0,self.width,self.height)
        cor = (offset,offset, self.width-offset,self.height-offset)
        
        for i in range(width):
            self.draw.rectangle(cor ,outline=(0,0,0))   
            cor = (cor[0]+1,cor[1]+1, cor[2]-1,cor[3]-1) 
        self.canvas.save( "test.png" )
        
    # 學號格
    def studentID(self,digits):
        self.drawText('學',location=(self.padding,200))
        self.drawText('號',location=(self.padding,400))
        image, block = self.optionRect(digits,'1234567890',(200,self.padding))
        self.questBorderY(image.size[1]+self.pic_size+int(self.padding/2))
        
    def testID(self):
        offset = int(self.width/2)
        self.drawText('考',location=(offset + self.padding,150))
        self.drawText('卷',location=(offset + self.padding,270))
        self.drawText('編',location=(offset + self.padding,390))
        self.drawText('號',location=(offset + self.padding,510))
        image, block = self.optionRect(1,'ABCDEFGHIJ',(offset + 200,self.padding))
        image, block = self.optionRect(5,'1234567890',(offset + 200,image.size[1]+self.padding))
        self.questBorderY(image.size[1]+self.pic_size+int(self.padding/2))

    def quest(self,num,sequence='ABCD'):
        if self.questStart == None :
            self.questStart = self.quest_down
        self.questInit(self.quest_left,self.questStart)
        max_height = int((self.height-self.questStart-20)/self.pic_size)
        remain = max_height-self.count%max_height
        if num > remain and remain != max_height :
            print(remain)
            rect = self.optionRect(remain,sequence,(self.quest_left + self.font_size*2, int(self.padding/2) +  self.questStart +(self.count%max_height)*(self.font_size)))
            for _ in range(remain):
                location = (self.quest_left + self.padding, self.questStart+(self.count%max_height)*(self.font_size))
                self.drawText(''.join(self.questNum()), location=location )
            self.questInit(self.quest_right,self.questStart)
            num -= remain
        row = range(num)[::max_height]
        rect = None
        for i,r in enumerate(row) :
            if len(row)!=(i+1) and num > max_height:
                rect = self.optionRect(max_height,sequence,(self.quest_left + self.font_size*2, int(self.padding/2) +  self.questStart +(self.count%max_height)*(self.font_size)))
                for _ in range(max_height):
                    location = (self.quest_left + self.padding, self.questStart+(self.count%max_height)*(self.font_size))
                    self.drawText(''.join(self.questNum()), location=location )
                self.questInit(self.quest_right,self.questStart)
            elif len(row) == (i+1):
                # self.questStart = self.quest_up
                self.optionRect(num%max_height,sequence,(self.quest_left + self.font_size*2, int(self.padding/2) +  self.questStart +(self.count%max_height)*(self.font_size)))
                for x in range(num%max_height):
                    location = (self.quest_left + self.padding, self.questStart+(self.count%max_height)*(self.font_size))
                    self.drawText(''.join(self.questNum()), location=location )
                # if self.questStart == None :
                #     self.questStart = self.quest_up
                assert self.quest_right < self.width
                if self.count%max_height == 0 :
                    self.questInit(self.quest_right,self.questStart)
                else :
                    self.questInit(self.quest_left,self.quest_down)
            else :
                assert False, 'WTF???'
        
        
        
    def paste(self, image, location):
        self.canvas.paste(image,location)
        # self.canvas.save( "test.png" )

    def setAnswer(self):
        pass


model = Model()
model.studentID(6)
model.testID()
# model.questInit()
# model.quest(40,'ABCDEFGHIJ')

# model.quest(46 ,'ABCD')

# model.quest(46 ,'ABCD')

model.quest(74 ,'ABCDEFGHIJ')
# model.quest(16,'1234')
model.border()
