#!/usr/bin/python3

# Def for debug messages
verbose = True
def debug(str):
    if (verbose == True):
        print(str)

# Imports
import os, subprocess
import argparse, pyperclip

# Add notif_decay_time to config

notif_decay_time = 25000

# Parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument('file_path')
parser.add_argument('dst_route')
parser.add_argument('dst_dir')
args = parser.parse_args()

file_path = args.file_path
dst_route = args.dst_route + ':'
dst_dir = args.dst_dir

#TODO: Account for spaces in file path

basename = os.path.basename(file_path)

debug(basename)

rc_copy_proc = subprocess.run(['rclone',
                                'copy',
                                file_path,
                                f'{dst_route}{dst_dir}'],
                                stdout=subprocess.PIPE)

rc_link_proc = subprocess.run(['rclone',
                                'link',
                                f'{dst_route}{dst_dir}/{basename}'],
                                stdout=subprocess.PIPE)

#TODO: Handle unexpected copy output

#TODO: Handle unexpected link output

rc_link = rc_link_proc.stdout.rstrip().decode('UTF-8')

debug(rc_link)

pyperclip.copy(rc_link)

with open("history.json", "a") as history_f:
    history_f.write(f'{rc_link}\n')

notification = subprocess.run(['notify-send',
                                '--app-name=RCShareTools',
                                f'--expire-time={str(notif_decay_time)}',
                                '--icon=cloud-upload',
                                f'Uploaded {basename} to {dst_route}{dst_dir}',
                                f'{rc_link}'])


