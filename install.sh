#!/usr/bin/bash

# Finds the path of this install.sh
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

sudo chmod +x $BASE_DIR/rcst.py

cp $BASE_DIR/rclone_share_tools.desktop $BASE_DIR/temp.desktop

sed -i "s+/this/path/should/be/replaced/on/install+$BASE_DIR/rcst.py+g" $BASE_DIR/temp.desktop
sed -i "s+dst_route_1+$1+g" $BASE_DIR/temp.desktop
sed -i "s+dst_dir_1+$2+g" $BASE_DIR/temp.desktop

sudo rm -f /usr/share/kservices5/ServiceMenus/rclone_share_tools.desktop

sudo cp $BASE_DIR/temp.desktop /usr/share/kservices5/ServiceMenus/rclone_share_tools.desktop

touch $BASE_DIR/config.json
echo "{}" > $BASE_DIR/config.json

touch $BASE_DIR/history.json
echo "{}" > $BASE_DIR/history.json

rm $BASE_DIR/temp.desktop

echo "Done"
