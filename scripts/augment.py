import glob
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

INPUT_DIR = "input/settings-PascalVOC-export"
OUTPUT_DIR = "output"
AUGMENT_SIZE = 1


def main():
    # augments images and annotation xmls
    for file in glob.glob("%s/Annotations/*.xml" % INPUT_DIR):
        print("Augmenting %s ..." % file)
        annotation = an.parse_xml(file)
        augment(annotation)

    # check augmented objects about if there is a detected object or not
    for file in glob.glob("%s/*.xml" % OUTPUT_DIR):
        an.inspect(file)


def augment(annotation):
    seq = sequence.get()

    for i in range(AUGMENT_SIZE):
        filename = annotation["filename"]
        sp = filename.split(".")
        outfile = "%s/%s-%02d.%s" % (OUTPUT_DIR, sp[0], i, sp[-1])

        seq_det = seq.to_deterministic()

        image = cv2.imread("%s/JPEGImages/%s" % (INPUT_DIR, annotation["filename"]))
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

        writer = Writer(
            outfile, annotation["size"]["width"], annotation["size"]["height"]
        )
        for bb in bbs_aug.bounding_boxes:
            writer.addObject(
                bb.label, float(bb.x1), float(bb.y1), float(bb.x2), float(bb.y2)
            )

        cv2.imwrite(outfile, image_aug)
        writer.save("%s.xml" % outfile.split(".")[0])


if __name__ == "__main__":
    main()
