#coding: utf8
import json     #analyze json
import hashlib  #calculate SHA1
import getpass  #enter password
import requests #HTTP POST
import io       #write unicode into file

import plists
import userinf
import utils
import general
import equipments
import card
import quest

# Client Constants
ip_login = 'http://121.40.19.137:8070/'
login_url = 'TouHouServer/logi/login'
mapdata_url = 'TouHouServer/map/mapdata'
battledata_url = 'TouHouServer/battle/battledata'
client_key = 'konakona'
client_version = '1.0.2.0'

def login():
    url = ip_login + login_url 
    param = {'v': client_version,'u': userinf.username, 'key': hashlib.sha1(client_key + userinf.password).hexdigest()}
    data = {'session': 'UNLOGIN'}
    req = requests.post(url, params = param, data = data)
    returnjson = json.loads(req.text)
    code = returnjson['code']
    if (code!='1'):
        return False
    userinf.session = returnjson['session']
    userinf.userequipments = returnjson['userequipments']
    userinf.usercards = returnjson['usercarddatas']
    userinf.userquests = returnjson['userquests']
    userinf.newsid = returnjson['newsid']
    userinf.teamlist = returnjson['usergrouplist']
    userinf.cardequip = returnjson['usercardequipments']
    userinf.mapstatus = returnjson['usermaps']
    userinf.banquetstatus = returnjson['userbanquet']
    userinf.resources = returnjson['userresources']
    userinf.dataip = returnjson['ip']
    #print json.dumps(usercards,ensure_ascii = False)
    return True

def menu():
    utils.drawline('STATUS')
    print userinf.resources['gamename'] + ', LV ' + userinf.resources['level'] + ', ' + userinf.resources['exp'] + '/' + userinf.resources['upexp']
    print 'Gold: ' + userinf.resources['gold'] + ', faith: ' + userinf.resources['faith'] + ', food: ' + userinf.resources['food']
    print 'session: ' + userinf.session
    utils.drawline('MENU')
    print '0. Battle - 出击（维护中）'
    print '1. FengNa - 领取赛钱箱'
    print '2. News - 文文新闻'
    print '3. Equipments - 物品'
    print '4. Cards - 整备'
    print '5. Quests - 委托'
    print '6. Banquet - 宴会（维护中）'
    print '7. 锻造（未实装）'
    print '8. 命令行（未实装）'
    print '9. 退出'
    return utils.select(9)


def banquetfunc():
    utils.drawline('BANQUET')
    print banquetstatus
    if banquetstatus['state'] == '2':
        banquet_type = banquetstatus['type']
        print '筹备中:', plists['banquet'][banquet_type]['name']
        print '剩余:', banquetstatus['readyendsecond'] + 's'
        print 'TODO: 快速筹备' #TODO

def dostartbanquet(cardid, banquet_type):
    url = dataip + startbanquet_url
    param = {'cardid': cardid, 'type': banquet_type}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)

#TODO: banquets

def battlefunc():
    utils.drawline('BATTLE')
    bootyns = {}
    avail_maps = []
    for m in mapstatus:
        bootyns[m['mapid']] = m['bootyn']
    maps = plists['map']
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
    for group in teamlist:
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
        print positionlist[position] + ': ' + card['cardid'], plists['card'][card['cardid']]['cardname'] + ', tag = ' + card['tag']

def gotomap(mapname, sel, sel_group):
    print 'Gotomap!'
    bn = dogetmapdata(mapname, 2, sel, sel_group)
    nextflag = dogetbattledata(bn, sel_group)
    if nextflag != '0':
        delaytime = chi2_rand_time()
        print 'Sleeping: ' + str(delaytime) + 's'
        time.sleep(delaytime)
        nextflag = dogetbattledata(bn, sel_group)

def dogetmapdata(mapid, difficulty, groupid, groupdata):
    url = dataip + mapdata_url
    s = ''
    for card in groupdata['useractors']:
        s += card['cardid'] + ',' + card['mappointx'] + ',' + card['mappointy'] + ';'
    param = {'mapid': mapid, 'difficulty': difficulty, 'groupid': groupid, 'data':s}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    status, returnjson = testjson(req.text)
    if status == True:
        return returnjson['bn']
    else:
        return None

def dogetbattledata(bn, groupdata):
    url = dataip + battledata_url
    s = ''
    for card in groupdata['useractors']:
        s += card['cardid'] + ',' + card['mappointx'] + ',' + card['mappointy'] + ';'
    param = {'m1': 'battledata', 'data': s, 'or': 0, 'bk': hashlib.sha1(client_key + bn).hexdigest(), 'equipmentid': '', 'iskszd': 0, 'kw': 'K' + str(chi2_rand())}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    status, returnjson = testjson(req.text)
    if status == False:
        return None
    nextflag = returnjson['battleData'][-1]['nextFlag']
    printbattledata(returnjson)
    return nextflag
    
def printbattledata(battledata):
    attacktypes = {u'3001': u'弹幕', u'1001': u'体术（撞击）', u'1002': u'体术（爪击）', u'1003': u'体术（响子）'}
    damagetypes = {u'0': u'(miss)', u'1': u'', u'2': u'(block)', u'3': u'(crit)'} 
    filename = 'log/' + gettime() + '.log'
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

if __name__ == '__main__':
    #for i in range(10):
    #   print chi2_rand_time()
    #exit()
    userinf.init_user()
    plists.init_plist()
    if(login()==False):
        print 'Login failed.'
        print 'Please delete user.inf and login again.'
        #TODO: Enter username and password again at this situation
        exit()
    print 'Login success.'
    #exit()
    while(1):
        sel = menu()
        {
            0: battlefunc, 1: general.fengna, 2: general.getnews,
            3: equipments.itemfunc, 4: card.cardfunc, 5: quest.questfunc,
            6: banquetfunc, 7: None, 8: None, 9: exit,
        }[sel]()
