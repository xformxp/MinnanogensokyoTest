#coding: utf8
import plistlib
import json

plist_names = ['banquet','blueprint','card','dialog','equipment','lm_dialog','map','quests','skin','spell','system']
plists = dict(zip(plist_names,[None for i in range(len(plist_names))]))
is_json = dict(zip(plist_names,[True for i in range(len(plist_names))]))
is_json['lm_dialog'] = False
is_json['system'] = False

# read the plists
def init_plist():
    global plists
    print 'initing plists...'
    for name in plist_names:
        filename = 'data/' + name + '.plist'
        file = open(filename,'r')
        content = file.read().replace('&','&amp;')
        plist = plistlib.readPlistFromString(content)
        if(is_json[name]):
            for key in plist:
                plist[key] = json.loads(plist[key])
            plists[name] = plist
        else:
            plists[name] = plist
        file.close()
    print 'complete.'

# get plist
# Parameter: name of plist
# Return: the plist, in json if in json format, or in string
def get_plist(name):
    return plists[name]
