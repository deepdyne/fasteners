# Fasteners

# Dependencies

```
$ yay -S opencv2
$ pipenv install
```

# CODE

- SXXX = Screw
- BXXX = Bolt
- NXXX = Nut

# Flow

1. Create dataest in datasets folder
  - like `datasets/xxx_datasets/xxx_class/xxx.jpg`
1. Do annotation by VoTT
  - Firstly, create Security Token and save somewhere private space
  - Create Connections:
    - select local storage of datasets_vott/xxxx_datasets as source connection
    - select local storage of voc_data as target connection
  - Create Local Project and chose those settings


# CMD

```
$ python increase_img.py # before annotation for data augumentation
```

conv VoTT to YOLO

- aggregate all image ids to the trainval.txt and test.txt files from indivisual classname_train/val.txt which is created by VoTT.

```
$ python voc_summary.py 
```

- create lables files
- create test.txt from Main/test.txt and 
- create trainval.txt from Main/trainval.txt
- the difference between Main/xxx.txt and xxx.txt is that latter has image path and former has image id

```
$ python voc_label.py
```

# REFERENCES:

- original: https://github.com/wakuphas/wakuphas/blob/master/AI/Scripts/increase_img.py
- reference: https://wakuphas.hatenablog.com/entry/2018/09/19/025941
