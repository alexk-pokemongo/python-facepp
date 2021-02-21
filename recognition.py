from __future__ import print_function, unicode_literals
from facepplib import FacePP
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import os
import json
import glob2

def build_annotation_table():
  num_persons = 6
  max_num_samples = 8
  dataset_dir = '/dataset/samples/combined/'

  max_samples = max_num_samples+1

  plt.figure(figsize=(max_samples, num_persons))

  images=[]
  image_files=[]
  colors=[(0,0,255),(0,255,0),(255,0,0),(0,255,255),(255,0,255),(255,255,0)]

  colorsize = (64,64)

  for p in range(num_persons):
    images.append([])
    image_files.append([])
    
  files = glob2.glob(os.path.join(dataset_dir, "*.jpg")) 

  for f in files:
    base=os.path.basename(f)
    person_id = -1
    print("processing file:%s" % base)
    #read image
    img = Image.open(f)
    person_id=base[0] #This only works as long as we only have <10 persons ToDo add regex
    print("person_id=%s" % person_id)
    if(person_id.isdigit()):
      person_id = int(person_id) 
      images[person_id].append(img)
      image_files[person_id].append(f)
      print("Appending person= %d sample = %d" %(person_id,len(images[person_id])-1))

  idx=0
  for person in range(num_persons):
    for sample in range(max_num_samples):
      try:
        print("person=%d sample=%d" % (person,sample))
        #display appropriate image
        plt.subplot(num_persons, max_samples, idx + 1)
        plt.imshow(images[person][sample])
        idx += 1
      except:
        print("image not found")
        idx += 1

    imcolor = colors[person]
    color_img = Image.new(mode='RGB', size=colorsize, color=imcolor)
    plt.subplot(num_persons, max_samples, idx + 1)
    plt.imshow(color_img)
    idx += 1
    #display color
    
  #save
  plt.savefig('yuka_table.png')
  return image_files,colors

def argmax(iterable):
    return max(enumerate(iterable), key=lambda x: x[1])

def compare_vs(app,img_file,reference_vec):
  scores = []
  num_persons = len(reference_vec)
  for i in range(num_persons):
    f = reference_vec[i] 
    cmp_ = app.compare.get(image_file1=f,image_file2=img_file)
    confidence = cmp_.confidence
    thresholds = cmp_.thresholds
    print("f=%s confidence=%d" % (f,confidence))
    print('thresholds', '=', json.dumps(thresholds, indent=4))
    scores.append(confidence)
    pass

  ret = (idx,val) = argmax(scores)
  print("Result for: %s Index= %d confidence = %f",(img_file,idx,val))

  return ret

#toDo - in memory
def run_recognition(image_files,colors):
  #and finally recognition
  api_key = 'o7rhF6OZEJDMYwWrAPjhT-fZ2g3iu1bP'
  api_secret = 'MazgWDEXoDC05CyJhvxHjXOratdvhi-H'

  #given a person, which sample to compare against  
  reference = [3,0,1,0,0,1]
  num_persons = len(reference)

  reference_vec = []
  for i in range(num_persons):
    reference_vec.append(image_files[i][reference[i]])

  app = FacePP(api_key=api_key, api_secret=api_secret)
  img_file = '/dataset/yuka_group.jpg'
  #detect all

  fname_only = os.path.basename(img_file)
  fname_noext = os.path.splitext(fname_only)[0]
  img = app.image.get(image_file=img_file,return_attributes=['age'],calculate_all=1)

  print('image', '=', img)
  print('faces_count', '=', len(img.faces))

  image = Image.open(img_file)
  image = image.convert('RGB')
  canvas = ImageDraw.Draw(image)

  for (idx, face_) in enumerate(img.faces):
    face_rect = face_.face_rectangle
    x0=face_rect['left']
    y0=face_rect['top']
    w =face_rect['width']
    h =face_rect['height']
    #cut out a face
    imcrop = image.crop((x0,y0,x0+w,y0+h))
    #long term: convert to base64 ?
    #fine if we just use file system for now
    compare_path = "test_%d.jpg" % idx
    imcrop.save(compare_path)
    #compare vs. imgs
    compare_result = compare_vs(app,compare_path,reference_vec)
    

    #highlight face
    pass