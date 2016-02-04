# PythonOCRTrainer
WIP!!

Generates ersatz scanned diagrams and calculates bounding boxes for each character. Useful for training neural networks for OCR work.

![Character bounding boxes](https://github.com/mlennox/PythonOCRTrainer/blob/master/Example.png)

## Note
Pillow/PIL does not have proper access to the details of font kerning, baselines etc. we estimate the kerning by calculating the character widths on their own, then together.

Some fonts seem to have a problem with the measured bounding box not surrounding each character due to the baseline being too low - I can't see a solution for that just yet...
