
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from . import check
from .word import *

class Model():

    def __init__(self,width=4500, height=4000, font_color=(190,190,190,255)) :
        self.count = 0
        self.padding = 50
        self.font_size = 120
        self.pic_size = 120
        self.width = width
        self.height = height
        self.font_color = font_color
        self.font = ImageFont.truetype("unicode.ttf", self.font_size, encoding="unic")
        self.canvas = Image.new( "RGBA", (self.width,self.height) )
        self.draw = ImageDraw.Draw( self.canvas )
        self.questInit()
        self.quest_option = [[],[]]
        self.test_option = [[],[]]
        self.student_option = [[],[]]
        self.questStart = -1
        self.border_offset = 10
        self.border_width = 10


###############################################################
                    # Make Model
###############################################################
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
            # print(self.quest_down)

    def questNum(self):
        self.count += 1
        yield '{:0>2}\n'.format( str(self.count) )

    def drawQuest(self,num,max,sequence):
        self.optionRect( num,sequence, \
                         (self.quest_left + self.font_size*2, int(self.padding/2) +  self.questStart +(self.count%max)*(self.font_size)), \
                         self.quest_option)
        for x in range(num):
            location = (self.quest_left + self.padding, self.questStart+(self.count%max)*(self.font_size))
            self.drawText(''.join(self.questNum()), location=location )

    def optionChain(self,sequence):
        files = ['icon/{}.png'.format(c) for c in sequence ]
        images = list(map(Image.open, files))
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)
        assert max_height == self.pic_size and total_width == (len(sequence) * self.pic_size), \
            'Make Sure the size of icon/*.png is {}x{}'.format(self.pic_size,self.pic_size)
        option = Image.new('RGBA', (total_width, max_height),(255,255,255,0))
        x = 0
        block = []
        for im in images:
            option.paste(im, (x,0))
            block.append((x,0))
            x += im.size[0]
        self.questBorderX(x)
        return option,np.array(block)


    def optionRect(self,num,sequence,location,stored):
        if num == 0 :
            return
        options, blockX = self.optionChain(sequence)
        temp = Image.new('RGBA', ((len(sequence) * self.pic_size), num*self.pic_size),(255,255,255,0))
        block = []
        y_offset = 0
        for quest in range(num):
            stored[0].append(sequence)
            temp.paste(options, (0,y_offset))
            block.append(blockX + (0,y_offset))
            y_offset += self.pic_size

        self.questBorderX(self.quest_right + location[0])
        self.questBorderY(y_offset + location[1])
        block = np.array(block) + location
        [stored[1].append(b) for b in block]
        self.paste(temp,location)
        return temp


    def border(self):
        offset = self.border_offset
        cor = (0,0,self.width,self.height)
        cor = (offset,offset,self.width-offset,self.height-offset)

        width = self.border_width
        for i in range(width):
            self.draw.rectangle(cor ,outline=(0,0,0))
            cor = (cor[0]+1,cor[1]+1, cor[2]-1,cor[3]-1)


    def paste(self, image, location):
        self.canvas.paste(image,location)


    def save(self):
        self.canvas.save( "model.png" )


    def quest(self,num,sequence='ABCD'):
        self.num = num
        if self.questStart == -1 :
            self.questStart = self.quest_down
        self.questInit(self.quest_left,self.questStart)
        max_height = int((self.height-self.questStart-self.border_offset-self.border_width)/self.pic_size)
        remain = max_height-self.count%max_height
        if num > remain and remain != max_height :
            self.drawQuest(remain,sequence)
            self.questInit(self.quest_right,self.questStart)
            num -= remain
        row = range(num)[::max_height]
        for i,r in enumerate(row) :
            if num > max_height:
                self.drawQuest(max_height,max_height,sequence)
                self.questInit(self.quest_right,self.questStart)
                num-=max_height
            else :
                self.drawQuest(num,max_height,sequence)
                assert self.quest_right < self.width
                if self.count%max_height == 0 :
                    self.questInit(self.quest_right,self.questStart)
                else :
                    self.questInit(self.quest_left,self.quest_down)



####################            自訂              ##############################

    # 學號格
    def studentID(self,digits):
        self.drawText('學',location=(self.padding,200))
        self.drawText('號',location=(self.padding,400))
        image = self.optionRect(digits,'1234567890',(200,self.padding),self.student_option)
        self.questBorderY(image.size[1]+self.pic_size+int(self.padding/2))

    # 測驗格 
    def testID(self):
        offset = int(self.width/2)
        self.drawText('考',location=(offset + self.padding,150))
        self.drawText('卷',location=(offset + self.padding,270))
        self.drawText('編',location=(offset + self.padding,390))
        self.drawText('號',location=(offset + self.padding,510))
        image = self.optionRect(1,'ABCDEFGHIJ',(offset + 200,self.padding), self.test_option)
        image = self.optionRect(5,'1234567890',(offset + 200,image.size[1]+self.padding), self.test_option)
        self.questBorderY(image.size[1]+self.pic_size+int(self.padding/2))




###############################################################
                    # Check Answer
###############################################################

    def inside(self,list_option,dot):
        if dot[1] < list_option[0][1] or dot[1] > (list_option[0][1] + self.pic_size) :
            return -1
        x = dot[0]
        for i,opt in enumerate(list_option):
            if x > opt[0] and x < (opt[0] + self.pic_size) :
                return i
        return -1

    def display_moment(self,moment,options):
        result = {}
        for m in moment :
            for i,opt in enumerate(options[1]) :
                inside = self.inside(opt,m)
                if inside != -1:
                    try :
                        if result[(i+1)].find(options[0][i][inside]) == -1 :
                            result[(i+1)] += options[0][i][inside]
                            result[(i+1)] = ''.join(sorted(result[(i+1)]))
                    except :
                        result[(i+1)] = options[0][i][inside]
        return result

    def getAns(self,cnts):
        ansm = check.getMoment(cnts,bound=(self.font_size*2,self.questStart,self.width-self.padding,self.height-self.padding))
        ans = self.display_moment(ansm,self.quest_option)
        return ans

    def getStudendID(self,cnts):
        sm = check.getMoment(cnts,bound=(self.font_size*2,self.padding,int(self.width/2),self.questStart-self.font_size))
        result = self.display_moment(sm,self.student_option)
        student_id = ''.join([x for x in result.values()])
        return student_id

    def getTestID(self,cnts):
        tm = check.getMoment(cnts,bound=(int(self.width/2),self.padding,self.width-self.padding,self.questStart-self.font_size))
        result = self.display_moment(tm,self.test_option)
        test_id = ''.join([x for x in result.values()])
        return test_id

    def result(self,image):
        cnts = check.getBlack(image)
        allans = self.getAns(cnts)
        ans = ['' for _ in range(self.num)]
        for num, a in allans.items():
            ans[num - 1] = a
        sid = self.getStudendID(cnts)
        tid = self.getTestID(cnts)
        return {'ans':ans,'sid':sid,'tid':tid}


