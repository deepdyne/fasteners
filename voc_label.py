"""
original: http://pjreddie.com/media/files/voc_label.py
"""

import os
import pickle
import xml.etree.ElementTree as ET
from os import getcwd, listdir
from os.path import join

sets = ["trainval", "test"]
classes = ["fastener"]

DIR_NAME = "fastener/output/YOLO-PascalVOC-export"


def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id):
    in_file = open(DIR_NAME + "/Annotations/%s.xml" % (image_id))
    out_file = open(DIR_NAME + "/labels/%s.txt" % (image_id), "w")
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)

    for obj in root.iter("object"):
        difficult = obj.find("difficult").text
        cls = obj.find("name").text
        if (
            cls not in classes or int(difficult) == 1
        ):  # TODO: Y if difficult is 1 then it will be skipped?
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find("bndbox")
        b = (
            float(xmlbox.find("xmin").text),
            float(xmlbox.find("xmax").text),
            float(xmlbox.find("ymin").text),
            float(xmlbox.find("ymax").text),
        )
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + "\n")


for image_set in sets:
    if not os.path.exists(DIR_NAME + "/labels/"):
        os.makedirs(DIR_NAME + "/labels/")
    image_ids = (
        open(DIR_NAME + "/ImageSets/Main/%s.txt" % (image_set)).read().strip().split()
    )
    image_ids = list(map(lambda x: os.path.splitext(x)[0], image_ids))

    for image_id in image_ids:
        convert_annotation(image_id)

    wd = getcwd()
    # Create full path file
    list_file = open("%s.txt" % (image_set), "w")
    for image_id in image_ids:
        list_file.write("%s/%s/JPEGImages/%s.jpg\n" % (wd, DIR_NAME, image_id))
    list_file.close()
