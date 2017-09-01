from model import *

model = Model()
model.studentID(6)
model.testID()
model.quest(75 ,'ABCDEFGHIJ')
model.border()
model.save()

image = cv2.imread('./test/test600-p2.png')
print(model.result(image))
