import sys
import os
import subprocess
from urllib.parse import quote
from _reader import *

os.chdir(sys.path[0])

filename = '../data/i.json'
config = read_json('../config.json')
if 'shared_dir' in config and config['shared_dir']!='':
        filename = os.path.join(config['shared_dir'],'i.json')

if har(filename, sys.argv[1:]):
    exit()

data = read_json(filename)

cmd = ''
new_window = False
incognito = False
google = False

args = sys.argv[1:]

#parse args
for arg in args:
    if google:
        google = False
        arg = quote(arg)
        cmd += 'https://www.google.com/search?q={}'.format(arg)
    elif arg in data:
        cmd += data[arg]+' '
    elif arg in ['-n','--new-window']:
        new_window = True
    elif arg in ['-i','--incognito']:
        incognito = True
    elif arg in ['-g','--google']:
        google = True
    else:
        exit()

#add options
if new_window:
    cmd+='--new-window '
if incognito:
    cmd+=' --incognito '

#make command
if sys.platform in ['linux', 'linux2']:
    cmd = 'chromium-browser '+cmd+' &'
else:
    cmd = 'chrome '+cmd

subprocess.call(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
