#!/usr/bin/bash

if [ "$#" -ne 1 ]; then
    echo "You must enter exactly 1 argument"
    exit
fi

echo "WARN: Moving this directory after install will cause failure."

# Finds the path of this install.sh
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

touch $BASE_DIR/config.json
echo "{}" > $BASE_DIR/config.json

touch $BASE_DIR/history.json
echo "{}" > $BASE_DIR/history.json

./rcst_config.py $1
./rcst_build.py

sudo chmod +x $BASE_DIR/rcst.py

sudo rm -f /usr/share/kservices5/ServiceMenus/rclone_share_tools.desktop

sudo cp $BASE_DIR/rclone_share_tools.desktop /usr/share/kservices5/ServiceMenus/rclone_share_tools.desktop

echo "Done"
