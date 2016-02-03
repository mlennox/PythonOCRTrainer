# we'll find all the fonts
# run through some brute-force (for now) choices of neighbour characters
# and calculate the kerning for each case
# and save that out to a file (in some format)
# this will then be loaded with the createCharacterTraining.py file
# to more closely approximate the bounding box for rendered text

# data stored as:


import ImageFont
SAMPLE_SIZE= 128 # should provide sufficient resolution for kerning values

def get_a_kerning_value(font_descriptor, char1, char2):
    """See if there is some kerning value defined for a pair of characters
    Return the kerning value as an approximated percentage of the row height."""

    imagefont= ImageFont.truetype(font_descriptor, SAMPLE_SIZE)

    width1= imagefont.getsize(char1)[0]
    width2= imagefont.getsize(char2)[0]
    widths, height= imagefont.getsize(char1 + char2)

    return (widths - (width1 + width2))/float(height)