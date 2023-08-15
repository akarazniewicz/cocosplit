Simple tool to split a multi-label coco annotation dataset with preserving class distributions among train and test sets.

The code is an updated version from [akarazniewicz/cocosplit](https://github.com/akarazniewicz/cocosplit) original repo, where the functionality of splitting multi-class data while preserving distributions is added.


## Installation

``cocosplit`` requires python 3 and basic set of dependencies:

specifically, in addition to the requirements of the original repo, (``scikit-multilearn``) is required, it is included the requirements.txt file

```
pip install -r requirements
```


## Usage

The same as the original repo, with adding an argument (``--multi-class``) to preserve class distributions
The argument is optional to ensure backward compatibility

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
  --multi-class         Split a multi-class dataset while preserving class
                        distributions in train and test sets
```

# Running

```
$ python cocosplit.py --having-annotations --multi-class -s 0.8 /path/to/your/coco_annotations.json train.json test.json
```

will split ``coco_annotation.json`` into ``train.json`` and ``test.json`` with ratio 80%/20% respectively. It will skip all images (``--having-annotations``) without annotations.

The order of the COCO sections are: images, annotations, categories, info and licenses. In the case the original COCO file doesn't have info nor licenses, it will just skip them.
