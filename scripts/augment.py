import argparse
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

dataset_name = "video_one_class"
aug_size = 10
input_dir = ""
train_dir = ""
train_percentage = 0


def get_cnt_of_xml_files(xml_files):
    return len(xml_files)


def get_xml_files():
    return glob.glob("%s/Annotations/*.xml" % input_dir)


def get_cnt_of_train(xml_files):
    cnt_of_files = len(xml_files)
    cnt_of_train = int(train_percentage * cnt_of_files)
    return cnt_of_train


def get_all_classes(xml_files):
    class_names = []
    for xml in xml_files:
        annotation = an.parse_xml(xml)
        for obj in annotation["objects"]:
            class_name = obj["name"]
            if not class_name in class_names:
                class_names.append(class_name)
    return class_names


def create_txt(class_name, target_xmls, type_name):
    """
    target_xmls is eigher trainval or test xmls
    """
    with open(f"{train_dir}/{class_name}_{type_name}.txt", "w") as f:
        for xml in target_xmls:
            annotation = an.parse_xml(xml)
            image_id = annotation["filename"]
            has_class = False
            for obj in annotation["objects"]:
                cn = obj["name"]
                if class_name == cn:
                    has_class = True
                    break
            if has_class == True:
                has_obj = 1
            else:
                has_obj = -1
            row = f"{image_id} {has_obj}\n"
            f.write(row)


def create_summary_txt():
    for file_type in ["trainval", "test"]:
        file_names = []
        for file_name in glob.glob(f"{train_dir}/*_{file_type}.txt"):
            file_names.append(file_name)

        image_ids = []
        print("file_names", file_names)
        for file_name in file_names:
            image_file_names = (
                open(file_name)
                .read()
                .strip()
                .split()[0::2]  # [0::2] means only takes odd no items
            )
            image_file_ids = list(
                map(lambda x: os.path.splitext(x)[0], image_file_names)
            )
            image_ids = image_file_ids

        with open("{}/{}.txt".format(train_dir, file_type), "w") as f:
            for image_id in image_ids:
                f.write("%s\n" % image_id)


def create_trainval_and_test(xml_files, cnt_of_train):
    trainval_files = []
    test_files = []
    for i, file in enumerate(xml_files):
        if i < cnt_of_train:
            trainval_files.append(file)
        else:
            test_files.append(file)
    return trainval_files, test_files


def main():
    # augments images and annotation xmls
    for file in glob.glob("%s/Annotations/*.xml" % input_dir):
        print("Augmenting %s ..." % file)
        annotation = an.parse_xml(file)
        augment(annotation)

    # check augmented objects about if there is a detected object or not
    for file in glob.glob("%s/Annotations/*.xml" % input_dir):
        an.inspect(file)

    # delete all files in ImageSets/Main
    for dirpath, dirnames, filenames in os.walk(train_dir):
        for filename in filenames:
            os.remove(os.path.join(dirpath, filename))

    # create xxx_{trainva,text}.txt
    xml_files = get_xml_files()
    cnt_of_xml_files = get_cnt_of_xml_files(xml_files)
    cnt_of_train = get_cnt_of_train(xml_files)
    trainval_files, test_files = create_trainval_and_test(xml_files, cnt_of_train)
    class_names = get_all_classes(xml_files)
    for class_name in class_names:
        create_txt(class_name, trainval_files, "trainval")
        create_txt(class_name, test_files, "test")

    create_summary_txt()


def augment(annotation):
    seq = sequence.get()

    for i in range(aug_size):
        filename = annotation["filename"]
        sp = os.path.splitext(filename)
        old_filename_except_ext = sp[0]
        new_filename_except_ext = "%s-%03d" % (old_filename_except_ext, i)
        old_filename_ext = sp[1]  # included dot
        new_image_filename = "%s%s" % (new_filename_except_ext, old_filename_ext)
        new_image_file_path = "%s/JPEGImages/%s" % (input_dir, new_image_filename)
        new_xml_file_path = "%s/Annotations/%s.xml" % (
            input_dir,
            new_filename_except_ext,
        )

        seq_det = seq.to_deterministic()

        image = cv2.imread("%s/JPEGImages/%s" % (input_dir, filename))
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
            new_image_filename,
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--dsname", "-d", help="dataset name", type=str)
    parser.add_argument(
        "--size", "-s", help="size of augmentation", type=int, default=5
    )
    args = parser.parse_args()
    if args.dsname is None:
        raise Exception("dataset name is needed!")

    # update global variable
    dataset_name = args.dsname
    aug_size = args.size
    input_dir = f"datasets_voc/{dataset_name}"
    train_dir = f"{input_dir}/ImageSets/Main"
    train_percentage = 1

    print(globals())

    main()
