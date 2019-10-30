import glob
import shutil
import xml.etree.ElementTree as ET

import imgaug as ia
import numpy as np
from imgaug import augmenters as iaa

EMPTY_DIR = "empty"


def parse_xml(filename):
    tree = ET.parse(filename)
    elem = tree.getroot()
    result = {
        "filename": elem.find(".//filename").text,
        "size": {
            "width": elem.find(".//size/width").text,
            "height": elem.find(".//size/height").text,
            "depth": elem.find(".//size/depth").text,
        },
        "objects": [],
    }

    for e in elem.findall(".//object"):
        obj = {
            "name": e.find(".//name").text,
            "xmin": e.find(".//bndbox/xmin").text,
            "ymin": e.find(".//bndbox/ymin").text,
            "xmax": e.find(".//bndbox/xmax").text,
            "ymax": e.find(".//bndbox/ymax").text,
        }
        result["objects"].append(obj)

    return result


def inspect(filename):
    annotation = parse_xml(filename)
    if len(annotation["objects"]) == 0:
        print(f"filename={filename}, data={annotation}")
        raise Exception("There is a file that does not contain any objects!")
