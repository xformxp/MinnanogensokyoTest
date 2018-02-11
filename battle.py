#coding: utf8
import plists
import utils
import userinf
import requests
import general
import hashlib
import io
import json
import time

mapdata_url = 'TouHouServer/map/mapdata'
battledata_url = 'TouHouServer/battle/battledata'
client_key = 'konakona'

def battlefunc():
    utils.drawline('BATTLE')
    bootyns = {}
    avail_maps = []
    for m in userinf.mapstatus:
        bootyns[m['mapid']] = m['bootyn']
    maps = plists.get_plist('map')
    for m in maps:
        if m in bootyns:
            print m + '\t' + maps[m]['groupname'] + ' - ' + maps[m]['mapname'] + ': ' + bootyns[m]
            avail_maps.append(m)
        elif maps[m]['needmapid'] == '' or maps[m]['needmapid'] in bootyns:
            print m + '\t' + maps[m]['groupname'] + ' - ' + maps[m]['mapname'] + ': ?'
            avail_maps.append(m)
    mapname = raw_input('Input map id: ')
    if mapname not in maps:
        print 'Input error.'
        return
    elif mapname not in avail_maps:
        print 'Map not available.'
        return
    sel, sel_group = selectgroup()
    if sel_group == None:
        return
    gotomap(mapname, sel, sel_group)

def selectgroup():
    utils.drawline('SELECT GROUP')
    grouplist = {}
    # eliminate redundancy
    for group in userinf.teamlist:
        if group['groupid'] not in grouplist:
            grouplist[group['groupid']] = group
    for groupid in grouplist:
        printgroup(grouplist[groupid])
    print 'Select a group'
    sel = utils.select(5)
    if str(sel) not in grouplist:
        print 'Invalid group.'
        return -1, None
    sel_group = grouplist[str(sel)]
    utils.drawline('GROUP INFO')
    printgroup(sel_group)
    print 'TODO: Edit group' #TODO
    return sel, sel_group

def printgroup(group):
    positionlist = {'12': 'Atk Mid(Captain)', '14': 'Atk Top', '10': 'Atk Bottom', '03': 'Def Top', '01': 'Def Bottom', '23': 'Aid Top', '21': 'Aid Bottom'}
    print 'Group #' + group['groupid'] + ':'
    for card in group['useractors']:
        position = card['mappointx'] + card['mappointy']
        print positionlist[position] + ': ' + card['cardid'], plists.get_plist('card')[card['cardid']]['cardname'] + ', tag = ' + card['tag']

def gotomap(mapname, sel, sel_group):
    print 'Gotomap!'
    bn = dogetmapdata(mapname, 2, sel, sel_group)
    nextflag = dogetbattledata(bn, sel_group)
    if nextflag != '0':
        delaytime = utils.chi2_rand_time()
        print 'Sleeping: ' + str(delaytime) + 's'
        utils.drawline();
        time.sleep(delaytime)
        nextflag = dogetbattledata(bn, sel_group)

def dogetmapdata(mapid, difficulty, groupid, groupdata):
    url = userinf.dataip + mapdata_url
    s = ''
    for card in groupdata['useractors']:
        s += card['cardid'] + ',' + card['mappointx'] + ',' + card['mappointy'] + ';'
    param = {'mapid': mapid, 'difficulty': difficulty, 'groupid': groupid, 'data':s}
    data = {'session': userinf.session}
    req = requests.post(url, params = param, data = data)
    status, returnjson = utils.testjson(req.text)
    if status == True:
        return returnjson['bn']
    else:
        return None

def dogetbattledata(bn, groupdata):
    url = userinf.dataip + battledata_url
    s = ''
    for card in groupdata['useractors']:
        s += card['cardid'] + ',' + card['mappointx'] + ',' + card['mappointy'] + ';'
    param = {'m1': 'battledata', 'data': s, 'or': 0, 'bk': hashlib.sha1(client_key + bn).hexdigest(), 'equipmentid': '', 'iskszd': 0, 'kw': 'K' + str(utils.chi2_rand())}
    data = {'session': userinf.session}
    req = requests.post(url, params = param, data = data)
    status, returnjson = utils.testjson(req.text)
    if status == False:
        return None
    nextflag = returnjson['battleData'][-1]['nextFlag']
    printbattledata(returnjson)
    return nextflag
    
def printbattledata(battledata):
    attacktypes = {u'3001': u'弹幕', u'1001': u'体术（撞击）', u'1002': u'体术（爪击）', u'1003': u'体术（响子）'}
    damagetypes = {u'0': u'(miss)', u'1': u'', u'2': u'(block)', u'3': u'(crit)'} 
    filename = 'log/' + utils.gettime() + '.log'
    f = io.open(filename, 'w', encoding = 'utf-8')
    f.write(json.dumps(battledata, ensure_ascii = False, indent = 4, separators = (',',': ')))
    for data in battledata['battleData']:
    #    print json.dumps(data, ensure_ascii = False)
        if data['cmd'] == 'R':
            print 'ROUND #' + data['rounds']
        elif data['cmd'] == 'A':
            print 'CHARA #' + data['actorid'] + ' moves.'
        elif data['cmd'] == 'D':
            for unattack in data['unattack']:
                print 'CHARA #' + data['attackid'] + ' attacks CHARA #'+ unattack['unattackid'] + ', damage = ' + unattack['damage'] + damagetypes[unattack['damagetype']] + ', type = ' + attacktypes[unattack['attacktype']]
        elif data['cmd'] == 'S':
            print 'SPELL: ' + data['spellname']
        elif data['cmd'] == 'RESULT':
            print 'RESULT: ' + data['result']
        else:
            print 'UNKNOWN cmd ' + data['cmd']
            print json.dumps(data, ensure_ascii = False)
    return

