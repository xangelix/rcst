#!/usr/bin/bash

echo "WARN: Moving this directory after install will cause failure."

# Finds the path of this install.sh
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ -f "$BASE_DIR/config.json" ]; then
    echo "$BASE_DIR/config.json exists."
else
    echo "$FILE does not exist."
    touch $BASE_DIR/config.json
    echo "{}" > $BASE_DIR/config.json
fi

if [ -f "$BASE_DIR/history.json" ]; then
    echo "$BASE_DIR/history.json exists."
else
    touch $BASE_DIR/history.json
    echo "{}" > $BASE_DIR/history.json
fi

konsole -e "$BASE_DIR/rcst_config.py add"
konsole -e "$BASE_DIR/rcst_build.py"

sudo chmod +x $BASE_DIR/rcst.py

sudo rm -f /usr/share/kservices5/ServiceMenus/rclone_share_tools.desktop

sudo cp $BASE_DIR/rclone_share_tools.desktop /usr/share/kservices5/ServiceMenus/rclone_share_tools.desktop

echo "Done"
