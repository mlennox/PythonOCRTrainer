from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import textwrap

# will use random Project Gutenberg texts instead of this
pangram = "Pack my box with five dozen liquor jugs. Cwm fjordbank glyphs vext quiz. Jackdaws love my big sphinx of quartz. A quick movement of the enemy will jeopardize six gunboats. Wafting zephyrs quickly vexed Jumbo. Brick quiz whangs jumpy veldt fox. The five boxing wizards jump quickly. Crazy Fredericka bought many very equisite opal jewels. Amazingly few discotheques provide jukeboxes. Sphinx of black quartz, judge my vow! Brawny gods just flocked up to quiz and vex him."



# create base image
w = 500
h = 400
image = Image.new("RGB", (w,h), "#fff0ee")
font = ImageFont.truetype("./fonts/apache/roboto/Roboto-Black.ttf", 16)
draw = ImageDraw.Draw(image)

# the key here is how to determine where the required characters are on the final image
# font.getsize(line_of_text) will return the width and height
# by a laborious process, we can find every character we require to classify
# then find the width of the line without it and then with it 
# to determine the bounding box - if we ignore descenders and risers etc.

# split the text into lines 40 characters long
lines = textwrap.wrap(pangram, width=40)

liney = 0
for line in lines:
	width, height = font.getsize(line)
	pos = ((w - width) / 2, liney)
	draw.text(pos, line, font=font, fill=(30,30,30))
	liney += height

image.show()

