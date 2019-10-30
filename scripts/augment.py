import glob
import os
import shutil
import sys
import xml.etree.ElementTree as ET

import cv2
import imgaug as ia
import numpy as np
from imgaug import augmenters as iaa
from pascal_voc_writer import Writer

from util import annotation as an
from util import sequence

VOC_DIR_NAME = "datasets_voc"
DATASET_NAME = "video_one_class"
INPUT_DIR = f"{VOC_DIR_NAME}/{DATASET_NAME}"
AUG_INPUT_DIR = f"{VOC_DIR_NAME}/{DATASET_NAME}_aug"
AUGMENT_SIZE = 1


def create_dir():
    if not os.path.exists(AUG_INPUT_DIR):
        os.makedirs(AUG_INPUT_DIR)
    if not os.path.exists(AUG_INPUT_DIR + "/Annotations/"):
        os.makedirs(AUG_INPUT_DIR + "/Annotations/")
    if not os.path.exists(AUG_INPUT_DIR + "/ImageSets/"):
        os.makedirs(AUG_INPUT_DIR + "/ImageSets/")
    if not os.path.exists(AUG_INPUT_DIR + "/JPEGImages/"):
        os.makedirs(AUG_INPUT_DIR + "/JPEGImages/")


def main():
    create_dir()

    # augments images and annotation xmls
    for file in glob.glob("%s/Annotations/*.xml" % INPUT_DIR):
        print("Augmenting %s ..." % file)
        annotation = an.parse_xml(file)
        augment(annotation)

    # check augmented objects about if there is a detected object or not
    for file in glob.glob("%s/Annotations/*.xml" % AUG_INPUT_DIR):
        an.inspect(file)


def augment(annotation):
    seq = sequence.get()

    for i in range(AUGMENT_SIZE):
        filename = annotation["filename"]
        sp = os.path.splitext(filename)
        old_filename_except_ext = sp[0]
        new_filename_except_ext = "%s-%03d" % (old_filename_except_ext, i)
        old_filename_ext = sp[1]  # included dot
        new_image_filename = "%s%s" % (new_filename_except_ext, old_filename_ext)
        new_image_file_path = "%s/JPEGImages/%s" % (AUG_INPUT_DIR, new_image_filename)
        new_xml_file_path = "%s/Annotations/%s.xml" % (
            AUG_INPUT_DIR,
            new_filename_except_ext,
        )

        seq_det = seq.to_deterministic()

        image = cv2.imread("%s/JPEGImages/%s" % (INPUT_DIR, filename))
        _bbs = []
        for obj in annotation["objects"]:
            bb = ia.BoundingBox(
                x1=float(obj["xmin"]),
                y1=float(obj["ymin"]),
                x2=float(obj["xmax"]),
                y2=float(obj["ymax"]),
                label=obj["name"],
            )
            _bbs.append(bb)

        bbs = ia.BoundingBoxesOnImage(_bbs, shape=image.shape)

        image_aug = seq_det.augment_images([image])[0]
        bbs_aug = (
            seq_det.augment_bounding_boxes([bbs])[0]
            .remove_out_of_image()
            .cut_out_of_image()
        )

        xml_writer = Writer(
            new_image_file_path,
            annotation["size"]["width"],
            annotation["size"]["height"],
        )
        for bb in bbs_aug.bounding_boxes:
            xml_writer.addObject(
                bb.label, float(bb.x1), float(bb.y1), float(bb.x2), float(bb.y2)
            )

        cv2.imwrite(new_image_file_path, image_aug)
        xml_writer.save(new_xml_file_path)


if __name__ == "__main__":
    main()
