#!/usr/bin/bash

# Finds the path of this install.sh
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

konsole -e "python3 $BASE_DIR/rcst_config.py edit"
python3 $BASE_DIR/rcst_build.py

pkexec --user root rm -f /usr/share/kservices5/ServiceMenus/rclone_share_tools.desktop

pkexec --user root cp $BASE_DIR/rclone_share_tools.desktop /usr/share/kservices5/ServiceMenus/rclone_share_tools.desktop

echo "Done"
