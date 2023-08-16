import json
import argparse
import funcy
from sklearn.model_selection import train_test_split
from skmultilearn.model_selection import iterative_train_test_split
import numpy as np


def save_coco(file, info, licenses, images, annotations, categories):
    with open(file, 'wt', encoding='UTF-8') as coco:
        if info and licenses:
            json.dump({ 'images': images, 'annotations': annotations, 'categories': categories, 
                    'info': info, 'licenses': licenses}, coco, indent=2, sort_keys=False)
        elif info:
            json.dump({ 'images': images, 'annotations': annotations, 'categories': categories, 
                    'info': info}, coco, indent=2, sort_keys=False)
        elif licenses:
            json.dump({ 'images': images, 'annotations': annotations, 'categories': categories, 
                    'licenses': licenses}, coco, indent=2, sort_keys=False)
        else:
            json.dump({ 'images': images, 'annotations': annotations, 'categories': categories}, 
                      coco, indent=2, sort_keys=False)

def filter_annotations(annotations, images):
    image_ids = funcy.lmap(lambda i: int(i['id']), images)
    return funcy.lfilter(lambda a: int(a['image_id']) in image_ids, annotations)


def filter_images(images, annotations):

    annotation_ids = funcy.lmap(lambda i: int(i['image_id']), annotations)

    return funcy.lfilter(lambda a: int(a['id']) in annotation_ids, images)


parser = argparse.ArgumentParser(description='Splits COCO annotations file into training and test sets.')
parser.add_argument('annotations', metavar='coco_annotations', type=str,
                    help='Path to COCO annotations file.')
parser.add_argument('train', type=str, help='Where to store COCO training annotations')
parser.add_argument('test', type=str, help='Where to store COCO test annotations')
parser.add_argument('-s', dest='split', type=float, required=True,
                    help="A percentage of a split; a number in (0, 1)")
parser.add_argument('--having-annotations', dest='having_annotations', action='store_true',
                    help='Ignore all images without annotations. Keep only these with at least one annotation')

parser.add_argument('--multi-class', dest='multi_class', action='store_true',
                    help='Split a multi-class dataset while preserving class distributions in train and test sets')
# parser.add_argument('--seq-id', dest='seq_id', action='store_true',help='Consider seq_id for grouping images into subsets')

args = parser.parse_args()

def main(args):

    with open(args.annotations, 'rt', encoding='UTF-8') as annotations:
        coco = json.load(annotations)
        # Check if 'info' and 'licenses' keys exist in the COCO annotations
        if 'info' in coco:
            info = coco['info']
        else:
            info = None
        
        if 'licenses' in coco:
            licenses = coco['licenses']
        else:
            licenses = None
            
        images = coco['images']
        annotations = coco['annotations']
        categories = coco['categories']

        number_of_images = len(images)

        images_with_annotations = funcy.lmap(lambda a: int(a['image_id']), annotations)

        if args.having_annotations:
            images = funcy.lremove(lambda i: i['id'] not in images_with_annotations, images)


        if args.multi_class:

            annotation_categories = funcy.lmap(lambda a: int(a['category_id']), annotations)

            #bottle neck 1
            #remove classes that has only one sample, because it can't be split into the training and testing sets
            annotation_categories =  funcy.lremove(lambda i: annotation_categories.count(i) <=1  , annotation_categories)

            annotations =  funcy.lremove(lambda i: i['category_id'] not in annotation_categories  , annotations)


            X_train, y_train, X_test, y_test = iterative_train_test_split(np.array([annotations]).T,np.array([ annotation_categories]).T, test_size = 1-args.split)

            save_coco(args.train, info, licenses, filter_images(images, X_train.reshape(-1)), X_train.reshape(-1).tolist(), categories)
            save_coco(args.test, info, licenses,  filter_images(images, X_test.reshape(-1)), X_test.reshape(-1).tolist(), categories)

            print("Saved {} entries in {} and {} in {}".format(len(X_train), args.train, len(X_test), args.test))

        else:

            X_train, X_test = train_test_split(images, train_size=args.split)

            anns_train = filter_annotations(annotations, X_train)
            anns_test=filter_annotations(annotations, X_test)

            save_coco(args.train, info, licenses, X_train, anns_train, categories)
            save_coco(args.test, info, licenses, X_test, anns_test, categories)

            print("Saved {} entries in {} and {} in {}".format(len(anns_train), args.train, len(anns_test), args.test))
            


if __name__ == "__main__":
    main(args)
