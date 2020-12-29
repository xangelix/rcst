#!/usr/bin/python3

# Imports
import os, json
import argparse

info = 'INF: '
sets = 'SET: '
error = 'ERR: '

parser = argparse.ArgumentParser()
parser.add_argument('new_num_dst')
args = parser.parse_args()

num_dst = int(args.new_num_dst)

def fix_type(cap: str, typ: str):
    if (typ == 'str'):
        return cap
    elif (typ == 'bool'):
        return (cap in ['True', 'true', 'TRUE', 't', 'T', 'y', 'Y'])
    elif (typ == 'int'):
        return int(cap)
    else:
        print(f'{error}Invalid type specified.')
        exit(1)

def prop_in(conf, prop, typ):
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
            conf.update({prop: fix_type(cap, typ)})
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


try:
    temp = config['destinations']
except:
    config.update({'destinations': []})


for i in range(num_dst):
    config['destinations'].append({})

fin_len = len(config['destinations'])

for i in range(fin_len):

    # Set properties
    prop_in(config['destinations'][i], 'name', 'str')
    prop_in(config['destinations'][i], 'icon', 'str')
    prop_in(config['destinations'][i], 'dst_route', 'str')
    prop_in(config['destinations'][i], 'dst_dir', 'str')
    prop_in(config['destinations'][i], 'direct_link', 'bool')
    prop_in(config['destinations'][i], 'notif_decay_time', 'int')


for i in range(fin_len):
    config['destinations'][i].update({'id': i})

config.update({'size': fin_len})

# Save config
with open(f'{working_dir}/config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)
