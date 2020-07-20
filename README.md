# fohm-transcripting

## Pre requisites

* bash (e.g. Ubuntu Linux)
* ffmpeg (in standard repos)
* tesseract (in standard repos)
* GNU parallel (in standard repos)

Tested on Ubunto 20.04 Desktop

## Example result

https://gist.github.com/jorgenponder/9a3079fba92c5631c1e7107470da4445

## Commands

Crop it down to the subtitle area (crop=335:64:25:279), invert the colors (negate), grayscale it (hue=s=0), dump it to a new PNG file once per second (fps=fps=1), name the files sequentially with 4 digits (%04d):

```ffmpeg -i video.mp4 -vf "fps=fps=1,hue=s=0,negate,crop=335:64:25:279" pics/videocr6%04d.png```

Run tesseract OCR on each PNG file and save the result to one text file per PNG:

```find . -iname \*.png -print0 | parallel -0 --bar 'tesseract -l swe {} {.}.txt > /dev/null 2>&1'```

Compile to file:

```ls|grep txt.txt|sort|xargs cat > allcompiled.txt```
