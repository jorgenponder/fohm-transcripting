# fohm-transcripting

## Pre requisites

* bash (e.g. Ubuntu Linux)
* ffmpeg (in standard repos)
* ImageMagick (in standard repos)
* ocrad  (in standard repos)
* (optional) GNU parallel (in standard repos)

* (deprecated, not needed) tesseract (in standard repos)


Tested on Ubuntu 20.04 Desktop

## Example result

https://gist.github.com/jorgenponder/9a3079fba92c5631c1e7107470da4445

## Purpose

To make what is said at Folkhälsomyndighetens press conferences available in text format, so it is searchable. Preferrably with time stamps.

## Overview

1 Use ffmpeg to only keep the box outlined in red

![bild](https://raw.githubusercontent.com/jorgenponder/fohm-transcripting/master/bild.png)

2 Use ffmpeg to produce pngs from every nth frame, with only the text bands in the pngs

3 Use ImageMagick to increase resolution by factor 2 and convert to npm format

3 Run Ocrad OCR on that

4 Collate into one file, in order

Another way is of course to just ask Folkhälsomyndigheten for the text files. Please do try if you want to!

## New method


Crop it down to the subtitle area (crop=335:64:25:279), invert the colors (negate), grayscale it (hue=s=0), dump it to a new PNG file once per second (fps=fps=1), name the files sequentially with 4 digits (%04d):

```
for i in *.mp4; do 
    mkdir pngs/$i-cropped-pngs-for-ocr
    ffmpeg -i "$i" -vf "fps=fps=1,hue=s=0,negate,crop=335:64:25:279" "pngs/$i-cropped-pngs-for-ocr/%04d.png"
done
```
Run image conversion and OCR:

```
for d in */ ; do
    cd "$d"
    mogrify -format ppm  -resize 200%  *.png
    cd ..
    echo "$d imagemagick done"
done

for d in */ ; do
    cd "$d"
    for i in *.ppm; do 
        ocrad -F utf8 $i >>"$i.txt"
    done
    cd ..
    echo "$d ocrad done"
done

for d in */ ; do
    cd "$d"
    ls|grep ppm.txt|sort|xargs cat |perl -n -e 's/[^a-zA-ZåäöÅÄÖ0-9.;, \-\n]//g;print' > "../${d%/}-utskrift.txt"
    cd ..
    echo "$d utskrift done"
done

```

## Overview of old method

1 Use ffmpeg to only keep the box outlined in red

![bild](https://raw.githubusercontent.com/jorgenponder/fohm-transcripting/master/bild.png)

2 Use ffmpeg to produce pngs from every nth frame, with only the text bands in the pngs

3 Run OCR on that

4 Collate into one file, in order

Another way is of course to just ask Folkhälsomyndigheten for the text files. Please do try if you want to!

## Old method, commands

Crop it down to the subtitle area (crop=335:64:25:279), invert the colors (negate), grayscale it (hue=s=0), dump it to a new PNG file once per second (fps=fps=1), name the files sequentially with 4 digits (%04d):

```ffmpeg -i video.mp4 -vf "fps=fps=1,hue=s=0,negate,crop=335:64:25:279" pics/videocr6%04d.png```

Run tesseract OCR on each PNG file and save the result to one text file per PNG:

```find . -iname \*.png -print0 | parallel -0 --bar 'tesseract -l swe {} {.}.txt > /dev/null 2>&1'```

Compile to file:

```ls|grep txt.txt|sort|xargs cat > allcompiled.txt```

Clean up the file:

```cat allcompiled.txt | perl -n -e 's/[^a-zA-ZåäöÅÄÖ0-9.; \-\n]//g;print' > allcompiled-cleaned.txt```
