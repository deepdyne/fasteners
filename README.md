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

First of all, make directories.

```
mkdir {datasets,datasets_final,vott_sources,vott_targets}/xxx_datasets
```

About VoTT

- Firstly, create Security Token and save somewhere private space
- Connections:
  - target connection
    - select local storage of vott_targets/xxx_dataset
  - source connection
    - select local storage of vott_sources/xxx_dataset
- Project settings
  - select security token and target/source connection that i have created
  - name is like `xxx_dataset_vott.vott` since there is already same name folder.
  - video frame rate is 1 sec
- Export Setings
  - providor: pascal voc
  - asset state: only tagged assets
  - tarinval:test = 80:20
  - export unsinged: check


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
