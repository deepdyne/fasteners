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
