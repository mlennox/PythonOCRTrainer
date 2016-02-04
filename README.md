# PythonOCRTrainer
Generates ersatz scanned diagrams and calculates bounding boxes for each character. Useful for training neural networks for OCR work.

## Examples
![Character bounding boxes](https://github.com/mlennox/PythonOCRTrainer/blob/master/Example.png)

Each red box above is a bounding box for the character 'e'. You can see that it is not exactly perfect just yet - I'm still working with calculating the kerning properly.

![Character bounding boxes](https://github.com/mlennox/PythonOCRTrainer/blob/master/Example2.png)

## Note
Currently the kerning tests pairs of characters, stores the values and then apples it to each pair in the source text. Observation shows that kerned characters at the ned of a word seem to effect the next word. Some fonts also seem to have bizzare baselines resulting in poor tracking of bounding boxes.

