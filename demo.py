from __future__ import print_function, unicode_literals
from facepplib import FacePP
from PIL import Image, ImageDraw

import json

api_key = 'o7rhF6OZEJDMYwWrAPjhT-fZ2g3iu1bP'
api_secret = 'MazgWDEXoDC05CyJhvxHjXOratdvhi-H'

app = FacePP(api_key=api_key, api_secret=api_secret)

img_file = '/home/alexk/dataset/yuka_group.jpg'
img = app.image.get(image_file=img_file,return_attributes=['age'])
print('image', '=', img)
print('faces_count', '=', len(img.faces))

image = Image.open(img_file)
image = image.convert('RGB')
canvas = ImageDraw.Draw(image)

for (idx, face_) in enumerate(img.faces):
  print('-', ''.join(['[', str(idx), ']']))
  print('face', '=', face_)
  gender=face_.gender['value']
  age=face_.age['value']
  print('gender', '=', face_.gender['value'])
  print('age', '=', face_.age['value'])
  
  print('face_rectangle', '=', json.dumps(face_.face_rectangle, indent=4))  
  face_rect = face_.face_rectangle
  if(gender=='Female'):
    outline_color=(153,50,204)
    pass
  elif(gender=='Male'):
    outline_color=(0,255,0)
    pass
    
  x0=face_rect['left']
  y0=face_rect['top']
  w =face_rect['width']
  h =face_rect['height']
    
  canvas.rectangle(xy=[x0,y0,x0+w,y0+h],outline=outline_color,width=2)
  canvas.text(xy=[x0-10,y0-10],text='age={}'.format(age),fill=outline_color)
  
image.save('test.png')