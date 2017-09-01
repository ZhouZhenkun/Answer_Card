# Answer_Card
The Answer Card Model & Check Test with OpenCV

```python
from model import *

model = Model()
model.studentID(6)
model.testID()
model.quest(75 ,'ABCDEFGHIJ')
model.border()
model.save()
```

<img src="https://github.com/bearbear1100/Answer_Card/blob/master/display/01.jpg" width="200">

Read image (Black Enough)

```python
image = cv2.imread('./test/test600-p2.png')
print(model.result(image))
```

![](https://github.com/bearbear1100/Answer_Card/blob/master/display/02.jpg =250x)


![](https://github.com/bearbear1100/Answer_Card/blob/master/display/03.png )