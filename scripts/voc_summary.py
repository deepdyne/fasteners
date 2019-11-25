"""
create trainval.txt and test.txt
"""

import argparse
import glob
import os
import shutil
import sys
import xml.etree.ElementTree as ET

DIR_NAME = ""
FILE_NAMES = []


def main():
    os.chdir(DIR_NAME)

    for file_name in FILE_NAMES:
        image_file_names = (
            open(file_name)
            .read()
            .strip()
            .split()[0::2]  # [0::2] means only takes odd no items
        )
        image_file_ids = list(map(lambda x: os.path.splitext(x)[0], image_file_names))

    with open("test.txt", "w") as f:
        for image_id in image_file_ids:
            f.write("%s\n" % image_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dsname", "-d", help="dataset name", type=str)
    parser.add_argument("--filenames", "-f", help="filenames", type=str)
    args = parser.parse_args()

    if args.dsname is None:
        raise Exception("dataset name is need!")
    if args.filenames is None:
        raise Exception("filenames is need!")

    if "," in args.filenames:
        FILE_NAMES = args.filenames.split(",")
    else:
        FILE_NAMES.append(args.filenames)
    DIR_NAME = "datasets_voc/{}/ImageSets/Main/".format(args.dsname)

    main()
