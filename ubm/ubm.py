#!/bin/python

import json
import sys
import re
import subprocess
import pathlib

CONFIG_DIRECTORY = pathlib.Path.home()
CONFIG_FILE = CONFIG_DIRECTORY / '/.config/ubm/config.json'

if not CONFIG_FILE.is_file() or not CONFIG_DIRECTORY.is_dir() : 
    print("UrlBrowserMapper is not configured. Run ubmctl")
    exit()
else :
    config_file=open(CONFIG_FILE,'r')
    config=json.load(config_file)
    config_file.close()


try:
    config_file = open('./config.json','r')
except : 
    print("File not found!")
    exit()

browser_defaults = {
    "chromium" : {
        "browsers" : ["brave","chromium","google-chrome"],
        "profile_command" : "--profile-directory=",
    },
    "firefox" : {
        "browsers": ["firefox","icecat","librewolf"],
        "profile_command": "-P ",
    },
    "firefox_pwa": {
        "browsers" : ["firefoxpwa"],
        "profile_command" : "site launch ",
    },
    "epiphany" : {
        "browsers" : ["epiphany"],
        "profile_command" : "--profile=",
    }
}

def launch_command(config,url) : 
    command = config["browser"]
    for i in browser_defaults:
        if config["browser"] in browser_defaults[i]["browsers"]:
            command = "{} {}'{}' {}".format(command,browser_defaults[i]["profile_command"],config["profile"],url)
            break
    return command



config = json.load(config_file)
config_file.close()

mappings=config["mappings"]

url = sys.argv[1]


command=''

for i in mappings:
    for j in i["url_patterns"]:
        if re.match(j,url,re.I) :
            command=launch_command(i,url)
            break
    else:
        continue
    break
else:
    if(config["default_browser"]["profile"]==''):
        command = "{} {}".format(config["default_browser"]["browser"],url)
    else:
        command = launch_command(config["default_browser"],url)

print(command)
process = subprocess.Popen(command,start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT,shell=True)
