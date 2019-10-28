# Fasteners

- SXXX = Screw
- BXXX = Bolt
- NXXX = Nut

# CMD

```
$ python increase_img.py # before annotation for data augumentation
$ # conv VoTT to YOLO
$ python voc_summary.py # create yolo train/text.txt from yolo files that created by VoTT.
$ python voc_label.py # need to exec on note-book instance. conv VOC train/test to YOLO train/test files
```

REFERENCES:

- original: https://github.com/wakuphas/wakuphas/blob/master/AI/Scripts/increase_img.py
- reference: https://wakuphas.hatenablog.com/entry/2018/09/19/025941
