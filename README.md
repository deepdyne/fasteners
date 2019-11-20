# Fasteners

# Dependencies

```
$ # DL VoTT snap from github
$ sudo snap install "~/Downloads/vott-2.1.0-linux.snap --dangerous
$ yay -S opencv2
$ pipenv install
```

# CODE

- SXXX = Screw
- BXXX = Bolt
- NXXX = Nut
- OXXX = Others


# Token

```
my_token: maRMdjSQEkuaDCcGoqmA/LSt3wotOZFxlLgrDNTlhkQ=
```


# 1. Data preparation

First of all, it's need to make directories by following cmd.

```
$ mkdir {datasets_raw,datasets_vott,datasets_voc}/xxx_dataset
```

# 2. VoTT Flow

do Annotion by VoTT

- Firstly, create Security Token and save it to somewhere private space
- Connections:
  - target connection
    - name is target_xxx_dataset
    - select local storage of datasets_vott/xxx_dataset
  - source connection
    - name is source_xxx_dataset
    - select local storage of datasets_raw/xxx_dataset
- Project settings
  - name is `xxx_dataset`
  - select security token and target/source connection that i have created
  - name is like `xxx_dataset_vott.vott` since there is already same name folder.
  - video frame rate is 1 sec
- Export Setings
  - providor: pascal voc
  - asset state: only tagged assets
  - test:training = 20:80
  - export unsinged: check

after annotation is done, export proj as Pascal VOC

# 3. Copy exported Pascal VOC files to the datasets folder

```
$ DSNAME=xxx_dataset; cp -R ./datasets_vott/${DSNAME}/${DSNAME}-PascalVOC-export/* ./datasets_voc/${DSNAME}/
```

# 4. Auto annotation

```
$ python scripts/augment.py --dsname=three_class_trainval --size=5 --train_percentage=1
```

# 5. create train.txt and test.txt

```
$ python scripts/voc_label.py --dsname=three_class_trainval --classes=S001,O001,O002 --sets=trainval,test
```

# REFERENCES:

- https://github.com/wakuphas/wakuphas/blob/master/AI/Scripts/increase_img.py
- https://wakuphas.hatenablog.com/entry/2018/09/19/025941
- https://github.com/zchrissirhcz/imageset-viewer
- http://mukopikmin.hatenablog.com/entry/2018/12/05/002339
- https://github.com/tzutalin/labelImg
- https://github.com/aleju/imgaug
