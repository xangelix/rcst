#!/usr/bin/python3

# Imports
import os, json

def get_body_part(dst, dr):
    return f"""
[Desktop Action Dst{str(dst['id'])}]
Exec={dr}/rcst.py "%f" "{dst['dst_route']}" "{dst['dst_dir']}"
Name={dst['name']}
Icon={dst['icon']}
"""

# Get working directory
working_dir = os.path.dirname(os.path.realpath(__file__))

# Load config
config = {}
with open(f'{working_dir}/config.json') as f:
    config = json.load(f)

actions = ''
body = ''
for dst in config['destinations']:
    actions = f'{actions}Dst{dst["id"]};'
    body = f'{body}{get_body_part(dst, working_dir)}'

header = f"""
[Desktop Entry]
Type=Service
Name=rcst
Icon=cloud-upload
Actions={actions}Cfg;AddDst;
ServiceTypes=KonqPopupMenu/Plugin
MimeType=all/allfiles;
X-KDE-Priority=TopLevel
X-KDE-Submenu=rclone To...
"""

footer = f"""
[Desktop Action Cfg]
Exec=kdialog --msgbox "Not implemented yet :("
Name=Configure Destinations...
Icon=kstars_satellites

[Desktop Action AddDst]
Exec=kdialog --msgbox "Not implemented yet :("
Name=Add Destination...
Icon=format-add-node
"""

out = header + body + footer

with open(f'{working_dir}/rclone_share_tools.desktop', 'w', encoding='utf-8') as f:
    f.write(out)
