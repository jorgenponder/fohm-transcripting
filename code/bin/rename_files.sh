#! /bin/bash

convert_date () {
    local months=( januari februari mars april may juni juli augusti september oktober november december )
    local i
    for (( i=0; i<11; i++ )); do
        [[ $2 = ${months[$i]} ]] && break
    done
    printf "%4d-%02d-%02d\n" $3 $(( i+1 )) $1
}

# set -- "${1:-$(</dev/stdin)}" "${@:2}"

for f in *.txt ; do
    date_part=$( echo $f | grep -P -o '\d\d \w+ \w+' )
    # echo $date_part
    keep_part=$( echo $f | grep -P -o '.*\d\d \w+ \w+' )
    d=$( convert_date $date_part)
    new_name="$d-$keep_part.txt"
    echo $new_name
    mv "$f" "$new_name"
done
