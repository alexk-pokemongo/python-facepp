from __future__ import print_function, unicode_literals
import os
import glob2
import json

from facepplib import FacePP
from PIL import Image, ImageDraw


api_key = 'o7rhF6OZEJDMYwWrAPjhT-fZ2g3iu1bP'
api_secret = 'MazgWDEXoDC05CyJhvxHjXOratdvhi-H'

unfiltered_dir='/home/alexk/dataset/unfiltered/'
combined_dir='/home/alexk/dataset/samples/combined/'

files = glob2.glob(os.path.join(unfiltered_dir, "*.jpg"))

file_idx = 0
app = FacePP(api_key=api_key, api_secret=api_secret)

for f in files:
  print("processing:"+f)
  pil_image = Image.open(f)
  pil_image = pil_image.convert('RGB')
  
  img = app.image.get(image_file=f)
  print('faces found', '=', len(img.faces))
  for (img_idx, face_) in enumerate(img.faces):
    face_rect = face_.face_rectangle
    #cut out and save
    print('face_rectangle', '=', json.dumps(face_.face_rectangle, indent=4))
    x0=face_rect['left']
    y0=face_rect['top']
    w =face_rect['width']
    h =face_rect['height']
    imcrop = pil_image.crop((x0,y0,x0+w,y0+h))
    out_fname="sample_%d_%d.jpg" %(file_idx,img_idx)
    out_path = os.path.join(combined_dir,out_fname)
    imcrop.save(out_path)
    pass 
    
  file_idx += 1
  pass
