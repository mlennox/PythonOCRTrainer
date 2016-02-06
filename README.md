# PythonOCRTrainer
Generates ersatz scanned diagrams and calculates bounding boxes for each character. Useful for training neural networks for OCR work.

## Scope
I am writing this as part of a project that will be OCRing text in real-world photographs so I needed something that can generate a range of training images from different fonts, with varying contrast, and exhibiting perspective, skew, blur and other distortions.

## Examples
![Character bounding boxes](https://github.com/mlennox/PythonOCRTrainer/blob/master/Example.png)

Each red box above is a bounding box for the character 'e'. You can see that it is not exactly perfect just yet - I'm still working with calculating the kerning properly.

![Character bounding boxes](https://github.com/mlennox/PythonOCRTrainer/blob/master/Example2.png)

## Why am I getting a 'list index out of range' error when I run the script?
Well, you'll need to copy some TTF fonts into the fonts folder - I've been using the [Google fonts](https://www.google.com/fonts) so far. If you only need to train against one font then only include that one!

You will also need some TXT files in the texts directory. Although, there is one example file with a bunch of [pangrams](https://en.wikipedia.org/wiki/Pangram). [Project Gutenberg](https://www.gutenberg.org/) is a good source, or if you have known texts you will need to OCR you could use those (beware over-fitting your neural net!)

## Note on work in progress
Currently the kerning tests pairs of characters, stores the values and then apples it to each pair in the source text. Observation shows that kerned characters at the end of a word seem to effect the next word. Some fonts also seem to have bizzare baselines resulting in poor tracking of bounding boxes.

