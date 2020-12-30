#!/usr/bin/bash

# Finds the path of this install.sh
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

konsole -e "$BASE_DIR/rcst_config.py edit"
konsole -e "$BASE_DIR/rcst_build.py"

sudo chmod +x $BASE_DIR/rcst.py

sudo rm -f /usr/share/kservices5/ServiceMenus/rclone_share_tools.desktop

sudo cp $BASE_DIR/rclone_share_tools.desktop /usr/share/kservices5/ServiceMenus/rclone_share_tools.desktop

echo "Done"
