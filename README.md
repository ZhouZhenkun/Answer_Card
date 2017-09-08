# Answer_Card
The Answer Card Model & Check Test with OpenCV

```python
from model import *

model = Model()
model.studentID()
model.testID()
model.quest(75 ,'ABCDEFGHIJ')
model.border()
model.save()
```

<img src="https://github.com/bearbear1100/Answer_Card/blob/master/display/01.jpg" width="500">

Read image (Black Enough)

```python
image = cv2.imread('./test/test600-p2.png')
print(model.result(image))
```

<img src="https://github.com/bearbear1100/Answer_Card/blob/master/display/02.jpg" width="500">


Result : 

![](https://github.com/bearbear1100/Answer_Card/blob/master/display/03.png )