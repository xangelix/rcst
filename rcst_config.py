# Imports
import json

# Get Working Directory
working_dir = os.path.dirname(os.path.realpath(__file__))

# Load config
config = {}
with open(f'{working_dir}/config.json') as f:
    config = json.load(f)

# Defaults
direct_link_def = True
notif_decay_time_def = -1

# In Buffer
in_set = ''

# Destination Route
dst_route = ''
try:
    dst_route = config['dst_route']
except:
    config.update({'dst_route': dst_route})

while (True):
    if (dst_route == ''):
        in_set = input('SET: dst_route (default MUST SPECIFY)')
    else:
        in_set = input(f'SET: dst_route (loaded) {dst_route}')

    if (dst_route == '' and inset != ''):
        config['dst_route'] = bool(in_set)
        break

# Destination Directory
in_set = ''
dst_dir = ''
try:
    dst_dir = config['dst_dir']
except:
    config.update({'dst_dir': dst_dir})

while (True):
    if (dst_dir == ''):
        in_set = input('SET: dst_dir (default MUST SPECIFY)')
    else:
        in_set = input(f'SET: dst_dir (loaded) {dst_dir}')

    if (dst_dir == '' and in_set != ''):
        config['dst_dir'] = bool(in_set)
        break

# Direct Link
in_set = ''
direct_link = NULL
try:
    direct_link = config['direct_link']
except:
    config.update({'direct_link': direct_link})

while (True):
    if (direct_link == NULL):
        in_set = input('SET: direct_link (default MUST SPECIFY)')
    else:
        in_set = input(f'SET: direct_link (loaded) {direct_link}')

    if (in_set == '' and direct_link == NULL):
        config['direct_link'] = direct_link_def
    else if (direct_link == -1):
        config['direct_link'] = bool(in_set)

    if (direct_link != NULL):
        break

# Notification Decay Time
in_set = ''
notif_decay_time = -1
try:
    notif_decay_time = config['notif_decay_time']
except:
    config.update({'notif_decay_time': notif_decay_time})

in_set = input('SET: notif_decay_time (default 25000)')

if (in_set == '' and notif_decay_time == -1):
    config['notif_decay_time'] = notif_decay_time_def
else if (notif_decay_time == -1):
    config['notif_decay_time'] = int(in_set)

while (True):
    if (notif_decay_time == -1):
        in_set = input('SET: notif_decay_time (default 25000)')
    else:
        in_set = input(f'SET: notif_decay_time (loaded) {notif_decay_time}')

    if (in_set == '' and notif_decay_time == -1):
        config['notif_decay_time'] = notif_decay_time_def
    else if (notif_decay_time == -1):
        config['notif_decay_time'] = int(in_set)

    if (notif_decay_time != -1):
        break
