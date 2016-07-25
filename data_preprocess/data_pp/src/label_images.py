#!/usr/bin/env python3
'''
Zhiang Chen
July,2016
'''

"Label the depth images, and store them as the format of 3D volume, which is consistent with the input of convnet"

import os
import numpy as np
from PIL import Image
from scipy import ndimage
from six.moves import cPickle as pickle

pixel_depth = 225.0
image_size = 80
num_image = 0

lf_x = 30
lf_y = 120
rt_x = lf_x + image_size
rt_y = lf_y + image_size

labels = dict()
label_num = 0

wd = os.getcwd()
print("Current directory is \""+wd+"\"")
print("Start to label the images in this directory? (yes/no)")
cmd = input()
assert cmd == "yes" or cmd == "no"
if cmd == "no":
	print("Input correct directory:")
	wd = input()
	assert os.path.isdir(wd)

input("Before labeling, make sure there is no subdirectories in this folder!\nPress Enter to continue")

files = os.listdir(wd)

num_images = 0
for name in files:
	debris = name.split('.')
	if debris[-1] != 'bmp':
		continue
	elif name.startswith('cropped'):
		continue
	else:
		num_images += 1
print("There are %d images to label" %num_images)
dataset = np.ndarray(shape=(num_images, image_size, image_size),dtype=np.float32)
labelset = np.ndarray(shape=(num_images, 1),dtype=np.float32)

for name in files:
	print("--------------------------------")
	debris = name.split('.')
	if debris[-1] != 'bmp':
		continue
	elif name.startswith('cropped'):
		continue
	else:
		image_file = os.path.join(wd, name)
		img0 = Image.open(image_file)
		img = img0.crop((lf_x,lf_y,rt_x,rt_y))
		img.show()
		img.save(wd+"/cropped_"+name)
		image_file = os.path.join(wd, "cropped_"+name)

		image_data = (ndimage.imread(image_file).astype(float) - pixel_depth / 2) / pixel_depth
		if image_data.shape != (image_size, image_size):
			raise Exception('Unexpected image shape: %s' % str(image_data.shape))
		print("The file name: "+name)
		label = input("Input the label of the image: ")
		if label in labels:
			label_num = labels[label]
		else:
			label_num += 1
			labels.setdefault(label,label_num)
		dataset[num_image,:,:] = image_data
		labelset[num_image,:]=label_num
		num_image += 1


print(dataset.shape)
print(labelset.shape)

data_file = wd + '/depth_data'
with open(data_file,'wb') as f:
	save={
		'dataset': dataset,
		'labelset':labelset
	}
	pickle.dump(save,f,pickle.HIGHEST_PROTOCOL)
	f.close()
statinfo = os.stat(data_file)
print('Compressed data size:', statinfo.st_size)
