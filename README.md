# fohm-transcripting

## Pre requisites

* bash (e.g. Ubuntu Linux)
* ffmpeg (in standard repos)
* GNU parallel (in standard repos)

## Commands

Crop it down to the subtitle area (crop=335:64:25:279), invert the colors (negate), dump it to a new PNG file once per second (fps=fps=1,),

```ffmpeg -i video.mp4 -vf "fps=fps=1,hue=s=0,negate,crop=335:64:25:279" pics/videocr6%04d.png```

Run tesseract OCR on each PNG file dump result to one text file per PNG

```find . -iname \*.png -print0 | parallel -0 --bar 'tesseract -l swe {} {.}.txt > /dev/null 2>&1'```

Compile to file:

```ls|grep txt.txt|sort|xargs cat > allcompiled.txt``
