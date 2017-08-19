NUM = ['①','②','③','④','⑤','⑥','⑦','⑧','⑨','⓪','⨁','⊖']
ENL = ['ⓐ','ⓑ','ⓒ','ⓓ','ⓔ','ⓕ','ⓖ','ⓗ','ⓘ','ⓙ','ⓚ','ⓛ','ⓜ','ⓝ','ⓞ','ⓟ','ⓠ','ⓡ','ⓢ','ⓣ','ⓤ','ⓥ','ⓦ','ⓧ','ⓨ','ⓩ']
EN  = ['Ⓐ','Ⓑ','Ⓒ','Ⓓ','Ⓔ','Ⓕ','Ⓖ','Ⓗ','Ⓘ','Ⓙ','Ⓚ','Ⓛ','Ⓜ','Ⓝ','Ⓞ','Ⓟ','Ⓠ','Ⓡ','Ⓢ','Ⓣ','Ⓤ','Ⓥ','Ⓦ','Ⓧ','Ⓨ','Ⓩ']
TEST = ['◯ ','◯ ','◯ ','◯ ','◯ ','◯ ','◯ ','◯ ','◯ ','◯ ']
from PIL import Image, ImageDraw, ImageFont

# x,y,w,h = cv2.boundingRect(cnt)
# cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

class Model():

    def __init__(self,width=400, height=1000, total_quest=10, font_size=25, font_color=(190,190,190,255)) :
        self.count = 0
        self.width = width
        self.height = height
        self.total_quest = total_quest
        self.font_size = font_size
        self.font_color = font_color
        self.font = ImageFont.truetype("unicode.ttf", self.font_size, encoding="unic")
        # self.canvas = Image.new( "RGBA", (self.width,self.height) )
        self.canvas = Image.new( "RGBA", (self.width,self.height),'white' )

    # Input the option list and get num of them
    def __option__(self,list,option_num):
        yield from list[:option_num]


    def __line__(self,symbol,option_num):
        self.count += 1
        number = str(self.count)
        mark = '{:0>2}'.format( str(self.count) )
        yield '{:<4}{}{}'.format( mark, ''.join(self.__option__(symbol,option_num)), '\n')
        # yield '{}{}'.format(''.join(self.__option__(symbol,option_num)), '\n')


    def question(self, question_num, option_num,*,type='EN'):
        if type == 'EN':
            symbol = EN
        if type == 'ENL':
            symbol = ENL
        if type == 'NUM':
            symbol = NUM
        if type == 'TEST':
            symbol = TEST
        for _ in range(question_num):
            self.drawing( ''.join(self.__line__(symbol,option_num)), location=(self.font_size, (self.count)*self.font_size) )


    def drawing(self,text,location=(0,0)):
        draw = ImageDraw.Draw( self.canvas )
        draw.text( (location), text, font=self.font, fill=self.font_color )
        # self.canvas.save( "test.png", "PNG" )
        self.canvas.save( "test.jpg" )


    def border(self,offset=5, width=5):
        draw = ImageDraw.Draw( self.canvas )
        cor = (offset,offset, self.width-offset-width,self.height-offset-width)
        for i in range(width):
            draw.rectangle(cor ,outline=(0,0,0))   
            cor = (cor[0]+1,cor[1]+1, cor[2]+1,cor[3]+1) 
        # self.canvas.save( "test.png", "PNG" )
        self.canvas.save( "test.jpg" )
        
        
    def setAnswer(self):
        pass

model = Model()
model.question(25,10,type='EN')
# model.question(25,8,type='TEST')
# model.question(20,20)
# model.question(20,12,type='NUM')
# model.question(2,2,type='ENL')
# model.question(6,7,type='NUM')
# model.question(2,17,type='EN')
model.border()
