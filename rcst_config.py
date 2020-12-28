# Imports
import json

# Get Working Directory
working_dir: str = os.path.dirname(os.path.realpath(__file__))

# Load defaults
defaults = {}
with open(f'{working_dir}/defaults.json') as f:
    defaults = json.load(f)

# Load config
config = {}
with open(f'{working_dir}/config.json') as f:
    config = json.load(f)

# Defaults
direct_link_def: bool = True
notif_decay_time_def: int = -1

# Destination Route
in_set: str = ''
dst_route: str = ''
try:
    dst_route = config['dst_route']

while (True):
    if (dst_route == ''):
        in_set = input('SET: dst_route (default MUST SPECIFY)')
    else:
        in_set = input(f'SET: dst_route (loaded {dst_route})')

    if (in_set == ''):
        if (dst_route != ''):
            config['dst_route'] = dst_route
            break
    else:
        config.update({'dst_route': in_set})
        break

# TODO: Object oriented on config


prop_in('dst_route')


# Destination Directory
in_set = ''
dst_dir = ''
try:
    dst_dir = config['dst_dir']

while (True):
    if (dst_dir == ''):
        in_set = input('SET: dst_dir (default MUST SPECIFY)')
    else:
        in_set = input(f'SET: dst_dir (loaded) {dst_dir}')

    if (in_set != ''):
        if (dst_dir == ''):
            config.update({'dst_dir': in_set})
        else:
            config['dst_dir'] = dst_dir
        break



# Direct Link
in_set = ''
direct_link = NULL
try:
    direct_link = config['direct_link']

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

    if (in_set != ''):
        if (direct_link == NULL):
            config.update({'direct_link': in_set})
        else:
            config['direct_link'] = direct_link
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

def prop_in(prop):
    val = ''
    cap = ''

    try:
        val = config[prop]

    #if (defaults[prop] == NULL):
    #    defaults[prop] = None

    default = defaults[prop]

    while (True):
        if (val == ''):
            cap = input(f'SET: {prop} (blank for default: {str(default)})')
        else:
            cap = input(f'SET: {prop} (blank for loaded: {val})')

        if (cap == ''):
            if (val == ''):
                if (default is NULL):
                    print(f'ERROR: {prop} must be set.')
                else:
                    config.update({prop: default})
                    break
            else:
                break
        else:
            config.update({prop: cap})
            break
