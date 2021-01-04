#!/usr/bin/python3

# Def for debug messages
verbose = True
def debug(str):
    if (verbose == True):
        print(str)

# Imports
import os, subprocess, json, datetime, re
import argparse, pyperclip

working_dir = os.path.dirname(os.path.realpath(__file__))

#TODO: Add notif_decay_time to config

notif_decay_time = 25000
direct_link = True

# Load config
config = {}
with open(f'{working_dir}/config.json') as f:
    config = json.load(f)

# Load current history
history = {}
with open(f'{working_dir}/history.json') as f:
    history = json.load(f)

# Parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument('file_path')
parser.add_argument('dst_route')
parser.add_argument('dst_dir')
parser.add_argument('--exp', type=str, default='0')
args = parser.parse_args()

file_path = args.file_path
dst_route = args.dst_route + ':'
dst_dir = args.dst_dir
exp_time = args.exp

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

if (direct_link):
    rc_link = rc_link.replace('https://drive.google.com/open?id=', 'https://drive.google.com/uc?id=')

debug(rc_link)

pyperclip.copy(rc_link)

if 'uploads' not in history:
    history.update({'uploads': []})

upload = {}
utc_now = datetime.datetime.now(datetime.timezone.utc)


exp_sec = exp_min = exp_hour = exp_day = exp_week = exp_month = exp_year = 0
exp_unit = exp_time[-1]


time_units = ['s', 'm', 'h', 'd', 'w', 'n', 'y']
time_inputs = {}
for unit in time_units:
    time_inputs.update({unit: 0})

debug(exp_time)

tu = ''.join(re.findall(r'[a-zA-Z]', exp_time))

debug(tu)

time_inputs[tu] = int(exp_time[0:-1])

# TODO: Months are always 4 weeks
# TODO: Years are always 365 days

time_delta = datetime.timedelta(seconds=time_inputs['s'],
                                minutes=time_inputs['m'],
                                hours=time_inputs['h'],
                                days=(time_inputs['y'] * 365) + time_inputs['d'],
                                weeks=(time_inputs['n'] * 4) + time_inputs['w'])

upload.update({'upload_time': utc_now.strftime("UTC-%Y-%m-%d-%H-%M-%S-%f")})
if (time_delta == 0):
    upload.update({'expiration': 'none'})
else:
    exp_now = utc_now + time_delta
    upload.update({'expiration': exp_now.strftime("UTC-%Y-%m-%d-%H-%M-%S-%f")})

upload.update({'link': rc_link})
upload.update({'name': basename})
upload.update({'upload_src': file_path})

history['uploads'].append(upload)

with open(f'{working_dir}/history.json', 'w', encoding='utf-8') as f:
    json.dump(history, f, ensure_ascii=False, indent=4)

notification = subprocess.run(['notify-send',
                                '--app-name=RCShareTools',
                                f'--expire-time={str(notif_decay_time)}',
                                '--icon=cloud-upload',
                                f'Uploaded {basename} to {dst_route}{dst_dir}',
                                f'{rc_link}'])


