import glob
import os

DIR_NAME = "fastener/output/YOLO-PascalVOC-export/ImageSets/Main/"

os.chdir(DIR_NAME)

for file_type in ["train", "val"]:
    file_names = []
    for file_name in glob.glob("*_{}.txt".format(file_type)):
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
        image_file_ids = list(map(lambda x: os.path.splitext(x)[0], image_file_names))
        image_ids = image_file_ids

    with open("{}.txt".format(file_type), "w") as f:
        for image_id in image_ids:
            f.write("%s\n" % image_id)

# NOTE: Coz VoTT creates train and val files on each classes as trainval and test.
os.rename("train.txt", "trainval.txt")
os.rename("val.txt", "test.txt")
