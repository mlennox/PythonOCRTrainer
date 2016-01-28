from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import textwrap
import numpy
import random
import os
# from os import listdir
# from os.path import isfile, join

line_length=60


# will be used to divide the image size to determine limit of perspective shift
size_factor = 10
color_range = 100
color_base = 255 - color_range
ex_w = 500
ex_h = 400


def fetch_text_files():
	source_texts = []
	source_text_files = []
	source_text_path = "./texts"

	for root, dirs, files in os.walk(source_text_path):
		for f in files:
			if f.endswith(".txt"):
				source_text_files.append(f)

	for src in source_text_files:
		text_file = open(source_text_path + "/" + src)
		source_texts.append(text_file.read())

	return source_texts

# the key here is how to determine where the required characters are on the final image
# font.getsize(line_of_text) will return the width and height
# by a laborious process, we can find every character we require to classify
# then find the width of the line without it and then with it 
# to determine the bounding box - if we ignore descenders and risers etc.


# https://github.com/nathancahill/snippets/blob/master/image_perspective.py
# pa - starting points
# pb - ending points
# func will find the relevant coeffs that will result in the transformation of pa to pb
# and this will be used to transform the entire image
def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

def generate_random_shifts(img_size):
	w = img_size[0] / size_factor
	h = img_size[1] / size_factor
	shifts = []
	for s in range(0,4):
		w_shift = (random.random() - 0.5) * w
		h_shift = (random.random() - 0.5) * h
		shifts.append((w_shift,h_shift))
	return shifts


# create random perspective
def create_perspective(img):
	img_size=img.size
	w = img_size[0]
	h = img_size[1]
	shifts = generate_random_shifts(img_size)
	coeffs = find_coeffs(
		[(shifts[0][0],shifts[0][1]),
		(w + shifts[1][0],shifts[1][1]),
		(w + shifts[2][0],h + shifts[2][1]),
		(shifts[3][0],h + shifts[3][1])],
		[(0,0),(w,0),(w,h),(0,h)])
	return img.transform((w,h), Image.PERSPECTIVE, coeffs, Image.BICUBIC)

def random_color(base_color_add):
	result_color = ()
	for c in range(0,3):
		color = base_color_add + int(color_range * random.random())
		result_color = result_color + (255 if color > 255 else color ,)
	return result_color

# create base image
def create_image(w,h,source_text,line_length):
	lines = textwrap.wrap(source_text, width=line_length)
	w_shift = int(w/size_factor) * 2
	h_shift = int(h/size_factor) * 2
	bg_color = random_color(color_base + 80)
	txt_color = random_color(30)
	image = Image.new("RGB", (w + w_shift,h + h_shift), bg_color)
	# we will choose this font randomly too
	font = ImageFont.truetype("./fonts/apache/roboto/Roboto-Black.ttf", 16)
	draw = ImageDraw.Draw(image)

	# now draw the text
	liney = h_shift
	for line in lines:
		width, height = font.getsize(line)
		pos = (w_shift, liney)
		draw.text(pos, line, font=font, fill=txt_color)
		liney += height

	return image

for source_text in fetch_text_files():
	image = create_image(ex_w,ex_h,source_text,60)
	perspective = create_perspective(image)
	perspective.show()

