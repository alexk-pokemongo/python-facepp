from __future__ import print_function, unicode_literals
import os
import glob2

from facepplib import FacePP
from PIL import Image, ImageDraw

unfiltered_dir='/home/alexk/dataset/unfiltered/'

files = glob2.glob(os.path.join(unfiltered_dir, "*.jpg"))

for f in files:
  print(f)
