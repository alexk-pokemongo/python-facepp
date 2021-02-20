from __future__ import print_function, unicode_literals
from facepplib import FacePP
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import os
import json
import glob2

num_persons = 6
max_num_samples = 8
dataset_dir = '/dataset/samples/combined/'

max_samples = max_num_samples+1

plt.figure(figsize=(max_samples, num_persons))

images=[]
colors=[(0,0,255),(0,255,0),(255,0,0),(0,255,255),(255,0,255),(255,255,0)]

colorsize = (64,64)

for p in range(num_persons):
  images.append([])
  
files = glob2.glob(os.path.join(dataset_dir, "*.jpg")) 

for f in files:
  base=os.path.basename(f)
  for word in base.split():
    if(word.isdigit()):
      person_id = int(word)
  #blah

idx=0
for person in range(num_persons):
  for sample in range(max_num_samples):
    #display appropriate image
    plt.subplot(num_persons, max_samples, idx + 1)
    plt.imshow(images[person][sample])
    idx += 1
    pass
  imcolor = colors[person]
  color_img = Image.new(mode='RGB', size=colorsize, color=imcolor)
  plt.subplot(num_persons, max_samples, idx + 1)
  plt.imshow(color_img)
  idx += 1
  #display color
  
#save
plt.savefig('yuka_table.png')
