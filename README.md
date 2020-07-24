# fohm-transcripting

## Pre requisites

* bash (e.g. Ubuntu Linux)
* ffmpeg (in standard repos)
* GNU parallel (in standard repos)
* tesseract (in standard repos)


Tested on Ubuntu 20.04 Desktop



## Purpose

To make what is said at Folkhälsomyndighetens press conferences available in text format, so it is searchable. Preferrably with time stamps.

## Overview

1 Use ffmpeg to only keep the box outlined in red

![bild](https://raw.githubusercontent.com/jorgenponder/fohm-transcripting/master/bild.png)

2 Use ffmpeg to produce pngs from every nth frame, with only the text bands in the pngs

3 Run Tesseract OCR on that

4 Collate into one file, in order

Another way is of course to just ask Folkhälsomyndigheten for the text files. Please do try if you want to!

## Tesseract has a giant bug that slows it down 250 times

In order to avoid that bug you *must* set the environment variable

```
OMP_THREAD_LIMIT=1
```

## Scripts

```bash
for d in */ ; do
    cd $d
    for i in *.mp4; do 
        mkdir pngs/$i-cropped-pngs-for-ocr
        ffmpeg -i "$i" -vf "fps=fps=1,hue=s=0,negate,crop=335:64:25:279" "pngs/$i-cropped-pngs-for-ocr/%04d.png"
    done
    cd ..
done
```


```bash

for d in */ ; do
    cd "$d"
    find . -iname \*.png -print0 | parallel -0 --bar 'OMP_THREAD_LIMIT=1 tesseract -l swe {} {.}.txt > /dev/null 2>&1'
    cd ..
done


for d in */ ; do
    cd "$d"
    ls|grep txt.txt|sort|xargs cat |perl -n -e 's/[^a-zA-ZåäöÅÄÖ0-9.;, \-\n]//g;print' > "../${d%/}-utskrift.txt"
    cd ..
    echo "$d utskrift done"
done

```


## Explanation


Crop it down to the subtitle area (crop=335:64:25:279), invert the colors (negate), grayscale it (hue=s=0), dump it to a new PNG file once per second (fps=fps=1), name the files sequentially with 4 digits (%04d):

```
for i in *.mp4; do 
    mkdir pngs/$i-cropped-pngs-for-ocr
    ffmpeg -i "$i" -vf "fps=fps=1,hue=s=0,negate,crop=335:64:25:279" "pngs/$i-cropped-pngs-for-ocr/%04d.png"
done
```
