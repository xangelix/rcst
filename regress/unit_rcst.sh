#!/usr/bin/bash

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

touch unit_temp.txt
echo "this is some testing text." > unit_temp.txt

./rcst.py $BASE_DIR/unit_temp.txt $1 $2

rm unit_temp.txt
