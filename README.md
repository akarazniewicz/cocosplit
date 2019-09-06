Simple tool to split coco annotations (json) into train and test sets.

## Installation

``cocosplit`` rquires python 3, and basic set of dependencies.

```
pip install -r requirements
```

## Usage

```
$ python cocosplit.py -h
usage: cocosplit.py [-h] -s SPLIT [--having-annotations]
                    coco_annotations train test

Splits COCO annotations file into training and test sets.

positional arguments:
  coco_annotations      Path to COCO annotations file.
  train                 Where to store COCO training annotations
  test                  Where to store COCO test annotations

optional arguments:
  -h, --help            show this help message and exit
  -s SPLIT              A percentage of a split; a number in (0, 1)
  --having-annotations  Ignore all images without annotations. Keep only these
                        with at least one annotation
```

# Running

```
$ python cocosplit.py --having-annotations -s 0.8 /path/to/your/coco_annotations.json train.json test.json
```

will split coco_annotation.json into train.json and test json with ration 80%/20% respectively. It will skip all
images (``--having-annotations``) withouth annotations.
