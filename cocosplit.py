import json
import argparse
import funcy
from sklearn.model_selection import train_test_split
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description='Splits COCO annotations file into training and test sets.')
parser.add_argument('annotations', metavar='coco_annotations', type=str,
                    help='Path to COCO annotations file.')
parser.add_argument('train', type=str, help='Where to store COCO training annotations')
parser.add_argument('test', type=str, help='Where to store COCO test annotations')
parser.add_argument('-s', dest='split', type=float, required=True,
                    help="A percentage of a split; a number in (0, 1)")
parser.add_argument('--having-annotations', dest='having_annotations', action='store_true',
                    help='Ignore all images without annotations. Keep only these with at least one annotation')
parser.add_argument('--images_folder', type=str, help='Path to images folder')

args = parser.parse_args()

def save_coco(file, info, licenses, images, annotations, categories):
    with open(file, 'wt', encoding='UTF-8') as coco:
        json.dump({ 'info': info, 'licenses': licenses, 'images': images, 
            'annotations': annotations, 'categories': categories}, coco, indent=2, sort_keys=True)

def filter_annotations(annotations, images):
    image_ids = funcy.lmap(lambda i: int(i['id']), images)
    return funcy.lfilter(lambda a: int(a['image_id']) in image_ids, annotations)

def split_images(images_folder, images, category):
    images_folder = Path(images_folder)
    new_dir = Path(images_folder.name + '_' + category)
    new_dir.mkdir(exist_ok=True)

    print(f"Copying {category} images...")
    for img in images:
        if (img["file_name"]).endswith('.jpg'):
            shutil.copy(images_folder / img["file_name"], new_dir)

def main(args):
    with open(args.annotations, 'rt', encoding='UTF-8') as annotations:
        coco = json.load(annotations)

        if 'info' in coco:
            info = coco['info']
        else:
            info = []

        if 'licences' in coco:
            licenses = coco['licenses']
        else:
            licenses = []

        images = coco['images']
        annotations = coco['annotations']
        categories = coco['categories']

        number_of_images = len(images)

        images_with_annotations = funcy.lmap(lambda a: int(a['image_id']), annotations)

        if args.having_annotations:
            images = funcy.lremove(lambda i: i['id'] not in images_with_annotations, images)

        x, y = train_test_split(images, train_size=args.split)

        save_coco(args.train, info, licenses, x, filter_annotations(annotations, x), categories)
        save_coco(args.test, info, licenses, y, filter_annotations(annotations, y), categories)

        if args.images_folder is not None:
            split_images(args.images_folder, x, 'train')
            split_images(args.images_folder, y, 'test')


        print("Saved {} entries in {} and {} in {}".format(len(x), args.train, len(y), args.test))


if __name__ == "__main__":
    main(args)
