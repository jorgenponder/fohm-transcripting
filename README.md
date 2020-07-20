# fohm-transcripting

## Pre requisites

* bash (e.g. Ubuntu Linux)
* ffmpeg (in standard repos)
* tesseract (in standard repos)
* GNU parallel (in standard repos)

Tested on Ubuntu 20.04 Desktop

## Example result

https://gist.github.com/jorgenponder/9a3079fba92c5631c1e7107470da4445

## Purpose

To make what is said at Folkhälsomyndighetens press conferences available in text format, so it is searchable. Preferrably with time stamps.

## Overview of current method

1 Use ffmpeg to only keep the box outlined in red

![bild](https://raw.githubusercontent.com/jorgenponder/fohm-transcripting/master/bild.png)

2 Use ffmpeg to produce pngs from every nth frame, with only the text bands in the pngs

3 Run OCR on that

4 Collate into one file, in order

Another way is of course to just ask Folkhälsomyndigheten for the text files. Please do try if you want to!

## Commands

Crop it down to the subtitle area (crop=335:64:25:279), invert the colors (negate), grayscale it (hue=s=0), dump it to a new PNG file once per second (fps=fps=1), name the files sequentially with 4 digits (%04d):

```ffmpeg -i video.mp4 -vf "fps=fps=1,hue=s=0,negate,crop=335:64:25:279" pics/videocr6%04d.png```

Run tesseract OCR on each PNG file and save the result to one text file per PNG:

```find . -iname \*.png -print0 | parallel -0 --bar 'tesseract -l swe {} {.}.txt > /dev/null 2>&1'```

Compile to file:

```ls|grep txt.txt|sort|xargs cat > allcompiled.txt```

## Batched version

A batch script for multiple mp4 files to PNG:

```
for i in *.mp4; do 
    mkdir pngs/$i-cropped-pngs-for-ocr
    ffmpeg -i "$i" -vf "fps=fps=1,hue=s=0,negate,crop=335:64:25:279" "pngs/$i-cropped-pngs-for-ocr/%04d.png"
done
```
