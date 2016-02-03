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
		# read in some of the file
		text_content = ""
		for text_file_line in text_file:
			text_content += text_file_line
			if (len(text_content) > 5000):
				break
		source_texts.append(text_content)
		text_file.close()

	return source_texts

def fetch_font_files():
	fonts = []
	font_path = "./fonts"

	for root, dirs, files in os.walk(font_path):
		for fnt in files:
			if fnt.endswith(".ttf"):
				fonts.append(os.path.join(root,fnt))

	return fonts

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

def get_a_kerning_value(font_descriptor, char1, char2):
	"""See if there is some kerning value defined for a pair of characters
	Return the kerning value as an approximated percentage of the row height."""

	imagefont= ImageFont.truetype(font_descriptor, SAMPLE_SIZE)

	width1= imagefont.getsize(char1)[0]
	width2= imagefont.getsize(char2)[0]
	widths, height= imagefont.getsize(char1 + char2)

	return (widths - (width1 + width2))/float(height)

def calculate_kernings(font, lines):
	"""Runs through the entire text recording if there is a kerning value between each paired character and records it if so"""

	# {'Ta':4,'he':2, etc.}
	kernings = {}
	for line in lines:
		prev = ''
		prev_w = 0
		line_w = len(line)
		line_pos = 1
		for char in line:
			char_w = font.getsize(char)[0]
			# if one of the chars is empy or a space then skip
			# if we are at the end of the line then skip
			# if the character pair already recorded then calculate and print, but skip
			if (char != ' ' and prev != '' and line_pos < line_w):
				char_pair = prev + char
				char_pair_w, char_pair_h = font.getsize(char_pair)
				if (char_pair_w != char_w + prev_w):
					kern = (char_pair_w - (prev_w + char_w)) / float(char_pair_h)
					if not (char_pair in kernings):
						kernings[char_pair] = kern
					print("kern : {0} - {1}".format(char_pair, kern))
			prev = char
			prev_w = char_w
			line_pos += 1

	return kernings

# bounding boxes are slightly off due to kerning and metrics
# http://stackoverflow.com/questions/2100696/can-i-get-the-kerning-value-of-two-characters-using-pil
# be we can estimate it?
def highlight_letter(font, lines, w_shift, h_shift, kernings):
	# TODO : find collection of unique chars in text (by line?) then run through them to find the bounding box
	# split each line by the provided letter then find the end of the line without the letter
	# and then with the letter, and find the line height to calculate the bounding box
	
	# is dictionary : { 'a':[((left, top), (right, bottom)),((top, height), right)], 'b':[etc]}
	chars_bounds = {}
	line_top = h_shift

	for line in lines:
		chars = ''.join(set(line))
		line_height = font.getsize(line)[1]
		for letter in chars:
			# does line contain the character
			if (line.find(letter) != -1):
				splits = line.split(letter)
				sofar = ""
				for split in splits:
					# print("{0} : {1}".format(letter, sofar))
					sofar += split
					# grab last letter sofar
					kern_test = sofar[-1:] + letter
					kern_correct = 0
					sans = font.getsize(sofar)
					sofar += letter
					avec = font.getsize(sofar)
					if (kern_test in kernings):
						kern_correct = kernings[kern_test] * avec[1]
					bounding_box = [(w_shift + sans[0] + kern_correct, line_top), (w_shift + avec[0] + kern_correct, line_top + avec[1])]
					# print("bounding box : {0}".format(bounding_box))
					if letter in chars_bounds:
						chars_bounds[letter].append(bounding_box)
					else:
						chars_bounds[letter] = [bounding_box]
		line_top += line_height

	return chars_bounds

# create base image
def create_image(w,h,source_text,line_length, font_file):
	font = ImageFont.truetype(font_file, 16)
	lines = textwrap.wrap(source_text, width=line_length)
	w_shift = int(w/size_factor) * 2
	h_shift = int(h/size_factor) * 2
	bg_color = random_color(color_base + 80)
	txt_color = random_color(30)
	image = Image.new("RGB", (w + w_shift,h + h_shift), bg_color)
	# we will choose this font randomly too
	font = ImageFont.truetype(font_file, 16)
	draw = ImageDraw.Draw(image)

	# calculate any kerning for pairs of letters for the entire text
	kernings = calculate_kernings(font, lines)
	# first draw bounding boxes (for now, of first char found)
	char_bounds = highlight_letter(font, lines, w_shift, h_shift, kernings)
	char_keys = list(char_bounds.keys())
	print("char keys : %s" % len(char_keys))
	bounds = char_bounds[list(char_bounds.keys())[0]]
	for bound in bounds:
		#print("bounds : {0}".format(bound))
		draw.rectangle(bound, fill="red")


	# now draw the text
	liney = h_shift
	for line in lines:
		width, height = font.getsize(line)
		pos = (w_shift, liney)
		draw.text(pos, line, font=font, fill=txt_color)
		liney += height

	return image

# rather than having random fonts, we should probably have the following for each font:
# 	pristine at different sizes and contrasts
# 	blurred/sharpened/grimed/dust " " "
# 	perspectived " " " "
# 	with all messups
font_files = fetch_font_files()
print("font files : %s" % font_files)
for source_text in fetch_text_files():
	font_file = int(random.random() * len(font_files)) - 1
	image = create_image(ex_w,ex_h,source_text,60, font_files[font_file])
	perspective = create_perspective(image)
	perspective.show()

# TODO : 
# add random amounts of blur, sharpen etc. to mess up the text
# also allow for a certain percentage of the texts to be pristine? 
