import glob
import os
import traceback
from random import randint

import numpy as np
from keras.preprocessing.image import (ImageDataGenerator, img_to_array,
                                       load_img)

dataset_name = "5class_fasteners_dataset"
dataset_dir_in = "./{}/{}/".format("inputs", dataset_name)
dataset_dir_out = "./{}/{}/".format("outputs", dataset_name)


def generate_images(class_name, generator):
    read_dir = dataset_dir_in + class_name + "/"
    if not os.path.exists(dataset_dir_out):
        os.mkdir(dataset_dir_out)
    save_dir = dataset_dir_out
    images = glob.glob(read_dir + "/*.jpg")
    print("input files = ", len(images))

    for i, image in enumerate(images):
        # 画像を読み取り
        image = load_img(image)
        # numpy arrayに変換
        x = img_to_array(image)
        # 4次元データに変換
        x = np.expand_dims(x, axis=0)

        g = generator.flow(
            x, save_to_dir=save_dir, save_prefix=class_name, save_format="jpg"
        )
        # output画像をinputの何倍作成するか 1で1倍, 10で10倍
        for j in range(5):
            g.next()

    print("output files = ", len(glob.glob(save_dir + "/*.jpg")))


# NOTE:
# - VoTT dataset does not pick data randomly
# - it follows file name order that's why i add random number to filename prefx
# - ref https://github.com/microsoft/VoTT/issues/915
def add_random_prefix():
    for filename in os.listdir(dataset_dir_out):
        rand_no = str(randint(0, 9999)).rjust(4, "0")
        src = f"{dataset_dir_out}{filename}"
        dst = f"{dataset_dir_out}{rand_no}_{filename}"
        os.rename(src, dst)


if __name__ == "__main__":

    try:
        # 画像データの拡張パラメータを設定
        train_datagen = ImageDataGenerator(
            rotation_range=0.0,  # 画像をランダムに回転する回転範囲（0-180）
            width_shift_range=0.0,  # ランダムに水平シフトする範囲
            height_shift_range=0.0,  # ランダムに垂直シフトする範囲
            shear_range=0.2,  # シアー強度（反時計回りのシアー角度（ラジアン））
            zoom_range=0.2,  # ランダムにズームする範囲
            horizontal_flip=True,  # 水平方向に入力をランダムに反転
            vertical_flip=True,  # 垂直方向に入力をランダムに反転
            rescale=1.0 / 255,  # 与えられた値をデータに積算する
        )

        generate_images("S001", train_datagen)
        generate_images("S002", train_datagen)
        generate_images("S003", train_datagen)
        # generate_images("S004", train_datagen)
        # generate_images("S005", train_datagen)

    except Exception as e:
        traceback.print_exc()

    add_random_prefix()
