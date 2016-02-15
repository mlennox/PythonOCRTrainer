# Bounding boxes
Since the Python libraries have no access to any of the open font data this NodeJs app is required.

## Overview
The app will find all the TTF fonts in the fonts folder and all the example texts in the parent folder.

Looping through each font, and using each example text it will build a list of the bounding boxes and kerning/adjustment of each glyph due to its neighbours. This will be saved (as JSON, but in a format yet to be decided) and used in the Python scripts to generate proper bounding boxes for each piece of mangled text.

## <del>Magnets</del> OpenType fonts; how do they work?

### Short answer
![I'll tell you! I don't know](https://github.com/mlennox/PythonOCRTrainer/blob/master/ill-tell-you.gif)
### Longer answer
As I figure it out, I'll update this page.

## Caveats
* Right now the code is a hot mess as I am figuring out how the tables work together. Once 'the patterns emerge' I will refactor, but for now it is a sophmore-looking amalgamation of procedural functions and clumsily nested IF statements. 
* Only True type / OpenType fonts supported at the moment
* No GSUB (glyph substitution) handled for the moment - any fonts with many ligatures will end up with poor bounding box alignment
* Only latin alphabet based languages supported. Near-English alphabet languages will probably be ok, but arabic, Indian sub-continent languages and probably most asian langauges will suffer badly as they rely on lots of glyph substitution and ligatures.
* Only horizontal layouts will be supported for the moment - I mean vertical layouts may work, but...

