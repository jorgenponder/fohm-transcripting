
for d in */ ; do
    cd "$d"
    echo '[' > "../${d%/}tesseract-utskrift.json"
    for f in *.txt.txt; do
        cat $f |perl -n -e 's/[^a-zA-ZåäöÅÄÖ0-9.;, \-\n]//g;s/\n/\\n/g;print "[\"$_\"],\n"' >> "../${d%/}tesseract-utskrift.json"
    done
    echo '""]' >> "../${d%/}tesseract-utskrift.json"
    cd ..
    echo "$d utskrift done"
done
