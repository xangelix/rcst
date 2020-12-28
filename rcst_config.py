#!/usr/bin/python3

# Imports
import os, json

info = 'INF: '
sets = 'SET: '
error = 'ERR: '

def prop_in(conf, prop):
    val = ''
    cap = ''

    try:
        val = conf[prop]
    except:
        print(f'{info}[{prop}] has not been set.')

    default = defaults[prop]

    while (True):
        if (val == ''):
            print(f'{sets}[{prop}] (blank for default: {str(default)})')
        else:
            print(f'{sets}[{prop}] (blank for loaded: {val})')

        cap = input()

        if (cap == ''):
            if (val == ''):
                if (default is None):
                    print(f'{error}{prop} must be set.')
                else:
                    conf.update({prop: default})
                    break
            else:
                break
        else:
            conf.update({prop: cap})
            break

# Get Working Directory
working_dir: str = os.path.dirname(os.path.realpath(__file__))

# Load defaults
defaults = {}
with open(f'{working_dir}/config_defaults.json') as f:
    defaults = json.load(f)

# Load config
config = {}
with open(f'{working_dir}/config.json') as f:
    config = json.load(f)

# Set properties
prop_in(config, 'dst_route')
prop_in(config, 'dst_dir')
prop_in(config, 'direct_link')
prop_in(config, 'notif_decay_time')

with open(f'{working_dir}/config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)
