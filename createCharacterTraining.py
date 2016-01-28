from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import textwrap
import numpy
import random
from os import listdir
from os.path import isfile, join

source_texts = []
source_text_path = "./texts"
source_text_files = [f for f in listdir(source_text_path) if isfile(join(source_text_path, f))]
for src in source_text_files:
	text_file = open(source_text_path + "/" + src)
	source_texts.append(text_file.read())


# will use random Project Gutenberg texts instead of this
# pangram = "Pack my box with five dozen liquor jugs. Cwm fjordbank glyphs vext quiz. Jackdaws love my big sphinx of quartz. A quick movement of the enemy will jeopardize six gunboats. Wafting zephyrs quickly vexed Jumbo. Brick quiz whangs jumpy veldt fox. The five boxing wizards jump quickly. Crazy Fredericka bought many very equisite opal jewels. Amazingly few discotheques provide jukeboxes. Sphinx of black quartz, judge my vow! Brawny gods just flocked up to quiz and vex him. MONDAY -- This new creature with the long hair is a good deal in the way. It is always hanging around and following me about. I don't like this; I am not used to company. I wish it would stay with the other animals. . . . Cloudy today, wind in the east; think we shall have rain. . . . WE? Where did I get that word-the new creature uses it. TUESDAY -- Been examining the great waterfall. It is the finest thing on the estate, I think. The new creature calls it Niagara Falls-why, I am sure I do not know. Says it LOOKS like Niagara Falls. That is not a reason, it is mere waywardness and imbecility. I get no chance to name anything myself. The new creature names everything that comes along, before I can get in a protest. And always that same pretext is offered -- it LOOKS like the thing. There is a dodo, for instance. Says the moment one looks at it one sees at a glance that it 'looks like a dodo.'' It will have to keep that name, no doubt. It wearies me to fret about it, and it does no good, anyway. Dodo! It looks no more like a dodo than I do. WEDNESDAY -- Built me a shelter against the rain, but could not have it to myself in peace. The new creature intruded. When I tried to put it out it shed water out of the holes it looks with, and wiped it away with the back of its paws, and made a noise such as some of the other animals make when they are in distress. I wish it would not talk; it is always talking. That sounds like a cheap fling at the poor creature, a slur; but I do not mean it so. I have never heard the human voice before, and any new and strange sound intruding itself here upon the solemn hush of these dreaming solitudes offends my ear and seems a false note. And this new sound is so close to me; it is right at my shoulder, right at my ear, first on one side and then on the other, and I am used only to sounds that are more or less distant from me."

# the key here is how to determine where the required characters are on the final image
# font.getsize(line_of_text) will return the width and height
# by a laborious process, we can find every character we require to classify
# then find the width of the line without it and then with it 
# to determine the bounding box - if we ignore descenders and risers etc.

line_length=60


# will be used to divide the image size to determine limit of perspective shift
size_factor = 10
color_range = 100
color_base = 255 - color_range
ex_w = 500
ex_h = 400



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

for b in range(0,2):
	image = create_image(ex_w,ex_h,source_texts[b],60)
	perspective = create_perspective(image)
	perspective.show()

