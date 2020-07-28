
for d in */ ; do
    cd "$d"
    output="../${d%/}tesseract-utskrift.tsv"
    echo '' > "$output"
    for f in *.txt.txt; do
        echo $f >> "$output"
        cat $f >> "$output"
        echo $'\t' >> "$output"
    done
    cd ..
    echo "$d utskrift done"
done

