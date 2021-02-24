from __future__ import print_function, unicode_literals
from facepplib import FacePP
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import os
import json
import glob2

def get_max_nums(dataset_dir, person_names,blacklisted_persons=[]):
  num_persons = len(person_names)
  max_num_samples = 0
  for name in person_names:
    if(name in blacklisted_persons):
      num_persons -= 1
      continue

    full_dir = os.path.join(dataset_dir,os.path.join(name,"samples"))
    samples = glob2.glob(os.path.join(full_dir,"*"))
    #glob files
    num_samples = len(samples)

    if(num_samples >max_num_samples):
      max_num_samples = num_samples
  return (num_persons,max_num_samples)

def build_annotation_table():
  
  max_num_samples = 8
  dataset_dir = '/dataset/blackbook_processed'
  person_names = ['Balaba_Dmitrii_Vladimirovich','Kubrakov_Ivan_Vladimirovich']

  (num_persons,max_num_samples) = get_max_nums(dataset_dir,person_names)
  
  max_samples = max_num_samples+1

  plt.figure(figsize=(max_samples, num_persons))

  images=[]
  image_files=[]
  colors=[(0,191,255),(252,15,192),(255,0,0),(0,255,255),(255,0,255),(255,255,0)]

  colorsize = (64,64)

  for p in range(num_persons):
    images.append([])
    image_files.append([])
    

  for (person_idx,person) in enumerate(person_names):

    person_dir = os.path.join(dataset_dir,person,"samples","*")

    files = glob2.glob(person_dir) 

    for f in files:
      base=os.path.basename(f)
      print("processing file:%s" % base)
      #read image
      try:
        img = Image.open(f)
      except:
        continue

    images[person_idx].append(img)
    image_files[person_idx].append(f)
    print("Appending person= %d sample = %d" %(person_idx,len(images[person_idx])-1))

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
  plt.savefig('balaba_table.png')
  return image_files,colors

def argmax(iterable):
    return max(enumerate(iterable), key=lambda x: x[1])

def compare_vs(app,img_file,reference_vec):
  scores = []
  num_persons = len(reference_vec)
  for i in range(num_persons):
    f = reference_vec[i] 
    try:
      cmp_ = app.compare.get(image_file1=f,image_file2=img_file)
      confidence = cmp_.confidence
      thresholds = cmp_.thresholds
      #print("f=%s confidence=%d" % (f,confidence))
      #print('thresholds', '=', json.dumps(thresholds, indent=4))
    except:
      print("Unable to compare !")
      confidence = 0

    
    scores.append(confidence)
    pass

  ret = (idx,val) = argmax(scores)
  print("Result for: %s Index= %d confidence = %f" %(img_file,idx,val))

  return ret

#toDo - in memory
def run_recognition(image_files,colors):
  #and finally recognition
  api_key = 'o7rhF6OZEJDMYwWrAPjhT-fZ2g3iu1bP'
  api_secret = 'MazgWDEXoDC05CyJhvxHjXOratdvhi-H'

  #given a person, which sample to compare against  
  reference = [0,0]
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

    age=face_.age['value']
    #cut out a face
    imcrop = image.crop((x0,y0,x0+w,y0+h))
    #long term: convert to base64 ?
    #fine if we just use file system for now
    compare_path = "test_%d.jpg" % idx
    imcrop.save(compare_path)
    #compare vs. imgs
    compare_result = compare_vs(app,compare_path,reference_vec)
    confidence = compare_result[1]
    if(confidence > 66):
      result_idx = compare_result[0]
      color = colors[result_idx]
      #highlight face
      canvas.rectangle(xy=[x0,y0,x0+w,y0+h],outline=color,width=2)
      canvas.text(xy=[x0-10,y0-10],text='age={}'.format(age),fill=color)
    pass

  out_file=fname_noext + '_recognition.png'
  image.save(out_file)


#toDo: main
if __name__ == "__main__":
  image_files,colors = build_annotation_table()
  run_recognition(image_files,colors)
  pass