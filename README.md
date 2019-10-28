# Fasteners

- SXXX = Screw
- BXXX = Bolt
- NXXX = Nut

# CMD

```
$ python increase_img.py # before annotation for data augumentation
```

conv VoTT to YOLO

- aggregate all image ids to the trainval.txt and test.txt files from indivisual classname_train/val.txt which is created by VoTT.

```
$ python voc_summary.py 
```

- create trainval.txt and test.txt from Main/trainval/test.txt
- the difference between them is that txt files that is cretated by this cmd has image_path not image_id

```
$ python voc_label.py # create label files from annotation files
```

# REFERENCES:

- original: https://github.com/wakuphas/wakuphas/blob/master/AI/Scripts/increase_img.py
- reference: https://wakuphas.hatenablog.com/entry/2018/09/19/025941
