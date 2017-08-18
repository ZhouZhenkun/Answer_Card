NUM = ['①','②','③','④','⑤','⑥','⑦','⑧','⑨','⓪','⨁','⊖']
ENL = ['ⓐ','ⓑ','ⓒ','ⓓ','ⓔ','ⓕ','ⓖ','ⓗ','ⓘ','ⓙ','ⓚ','ⓛ','ⓜ','ⓝ','ⓞ','ⓟ','ⓠ','ⓡ','ⓢ','ⓣ','ⓤ','ⓥ','ⓦ','ⓧ','ⓨ','ⓩ']
EN  = ['Ⓐ','Ⓑ','Ⓒ','Ⓓ','Ⓔ','Ⓕ','Ⓖ','Ⓗ','Ⓘ','Ⓙ','Ⓚ','Ⓛ','Ⓜ','Ⓝ','Ⓞ','Ⓟ','Ⓠ','Ⓡ','Ⓢ','Ⓣ','Ⓤ','Ⓥ','Ⓦ','Ⓧ','Ⓨ','Ⓩ']

from PIL import Image, ImageDraw, ImageFont

class Model():

    def __init__(self,width=400, height=1200, total_quest=10, font_size=18, font_color=(0,0,0,255)) :
        self.count = 0
        self.width = width
        self.height = height
        self.total_quest = total_quest
        self.font_size = font_size
        self.font_color = font_color
        self.font = ImageFont.truetype("unicode.ttf", self.font_size, encoding="unic")
        self.canvas = Image.new( "RGBA", (self.width,self.height) )

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
        for _ in range(question_num):
            self.drawing( ''.join(self.__line__(symbol,option_num)), location=(self.font_size, (self.count)*self.font_size) )


    def drawing(self,text,location=(0,0)):
        draw = ImageDraw.Draw( self.canvas )
        draw.text( (location), text, font=self.font, fill=self.font_color )
        # self.canvas.save( "test.png", "PNG" )
        self.canvas.save( "test.jpg" )


    def border(self,offset=0):
        up,down = '',''
        block = int((self.width - (2*offset))/ (self.font_size/1.5))
        up += '┏' + '━'*(block) + '┓' + '\n'
        down += '┗' + '━'*(block) + '┛' + '\n'
        assert (self.count+3)*self.font_size <= self.height, \
            'Too many questions in this card, Please adjust the size.'
        self.drawing(up, location=(5 ,0 ) )
        self.drawing(down,location=(5, (self.count + 1)*self.font_size))
        
        
    def setAnswer(self):
        pass

model = Model()
model.question(14,5)
model.question(20,20)
model.question(20,12,type='NUM')
# model.question(2,2,type='ENL')
# model.question(6,7,type='NUM')
# model.question(2,17,type='EN')
model.border()
