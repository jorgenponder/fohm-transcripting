
for d in */ ; do
    cd "$d"
    echo '[' > "../${d%/}tesseract-utskrift.json"
    ls|grep txt.txt|sort|xargs cat |perl -n -e 's/[^a-zA-ZåäöÅÄÖ0-9.;, \-\n]//g;s/\n/\\n/g;print "\"$_\",\n"' >> "../${d%/}tesseract-utskrift.json"
    echo '""]' >> "../${d%/}tesseract-utskrift.json"

    cd ..
    echo "$d utskrift done"
done
