from __future__ import print_function, unicode_literals
import os
import glob2
import json

from facepplib import FacePP
from PIL import Image, ImageDraw


api_key = 'o7rhF6OZEJDMYwWrAPjhT-fZ2g3iu1bP'
api_secret = 'MazgWDEXoDC05CyJhvxHjXOratdvhi-H'

def create_samples(app,dirname):
  files = glob2.glob(os.path.join(dirname, "*"))
  file_idx = 0
  out_dir = os.path.join(dirname,"samples")
  try:
    os.mkdir(out_dir)
  except:
    print("unable to create:%s , already exists ?" % out_dir)

  for f in files:
    print("processing:"+f)
    pil_image = Image.open(f)
    pil_image = pil_image.convert('RGB')
    
    img = app.image.get(image_file=f)
    basename = os.path.basename(f)
    name_noext = os.path.splitext(basename)[0]
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
      out_fname=("sample_%d_%d_"+name_noext + ".jpg") %(file_idx,img_idx)
      #ToDo make sample dir
      
      out_path = os.path.join(out_dir,out_fname)
      imcrop.save(out_path)
      pass 
    
    file_idx += 1

dataset_dir = '/dataset/blackbook_processed'
person_names = ['Balaba_Dmitrii_Vladimirovich','Kubrakov_Ivan_Vladimirovich']

app = FacePP(api_key=api_key, api_secret=api_secret)
import pdb; pdb.set_trace()
for name in person_names:
  name_path = os.path.join(dataset_dir,name)
  print("Creating dataset for:%s",name_path)
  create_samples(app,name_path)


