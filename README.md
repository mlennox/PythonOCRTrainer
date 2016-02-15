# PythonOCRTrainer
Generates ersatz scanned diagrams and calculates bounding boxes for each character. Useful for training neural networks for OCR work.

## Scope
I am writing this as part of a project that will be OCRing text in real-world photographs so I needed something that can generate a range of training images from different fonts, with varying contrast, and exhibiting perspective, skew, blur and other distortions.

## Bounding boxes
It seems to be easier to find the font metrics using the node library [fontkit](https://www.npmjs.com/package/fontkit).The 'boundingboxes' subfolder contains a nodejs app to generate bounding boxes from same font and text data used to generate the 'scans'.

### Overview
The app will find all the TTF fonts in the fonts folder and all the example texts in the parent folder.

Looping through each font, and using each example text it will build a list of the bounding boxes and kerning/adjustment of each glyph due to its neighbours. This will be saved (as JSON, but in a format yet to be decided) and used in the Python scripts to generate proper bounding boxes for each piece of mangled text.

## <del>Magnets</del> OpenType fonts; how do they work?

### Short answer
![I'll tell you! I don't know](https://github.com/mlennox/PythonOCRTrainer/blob/master/ill-tell-you.gif)
### Longer answer
As I figure it out, I'll update this page.

## Bounding box caveats
* Right now the code is a hot mess as I am figuring out how the tables work together. Once 'the patterns emerge' I will refactor, but for now it is a sophmore-looking amalgamation of procedural functions and clumsily nested IF statements. 
* Only True type / OpenType fonts supported at the moment
* No GSUB (glyph substitution) handled for the moment - any fonts with many ligatures will end up with poor bounding box alignment
* Only latin alphabet based languages supported. Near-English alphabet languages will probably be ok, but arabic, Indian sub-continent languages and probably most asian langauges will suffer badly as they rely on lots of glyph substitution and ligatures.
* Only horizontal layouts will be supported for the moment - I mean vertical layouts may work, but...

## Examples (using Python)
![Character bounding boxes](https://github.com/mlennox/PythonOCRTrainer/blob/master/Example.png)

Each red box above is a bounding box for the character 'e'. You can see that it is not exactly perfect just yet - I'm still working with calculating the kerning properly.

![Character bounding boxes](https://github.com/mlennox/PythonOCRTrainer/blob/master/Example2.png)

## Why am I getting a 'list index out of range' error when I run the script?
Well, you'll need to copy some TTF fonts into the fonts folder - I've been using the [Google fonts](https://www.google.com/fonts) so far. If you only need to train against one font then only include that one!

You will also need some TXT files in the texts directory. Although, there is one example file with a bunch of [pangrams](https://en.wikipedia.org/wiki/Pangram). [Project Gutenberg](https://www.gutenberg.org/) is a good source, or if you have known texts you will need to OCR you could use those (beware over-fitting your neural net!)
