#coding: utf8
import plistlib #analyze plist
import json     #analyze json
import hashlib  #calculate SHA1
import os       #file stream
import getpass  #enter password
import base64   #base64 library
import requests #HTTP POST

plist_names = ['banquet','blueprint','card','dialog','equipment','lm_dialog','map','quests','skin','spell','system']
plists = dict(zip(plist_names,[None for i in range(len(plist_names))]))
is_json = dict(zip(plist_names,[True for i in range(len(plist_names))]))
is_json['lm_dialog'] = False
is_json['system'] = False

ip_login = 'http://121.40.19.137:8070/'
ip_info = ''
login_url = 'TouHouServer/logi/login'
data_url = 'TouHouServer/actor/playerdata'
fengna_url = 'TouHouServer/actor/fengna'
news_url = 'TouHouServer/actor/newsdata'
gift_url = 'TouHouServer/equipment/gift'
sell_url = 'TouHouServer/equipment/sell'
questdata_url = 'TouHouServer/quests/questsData'
acceptquest_url = 'TouHouServer/quests/acceptQuests'
cancelquest_url = 'TouHouServer/quests/cancelQuests'
client_key = 'konakona'
client_version = '1.0.2.0'
username = ''
password = ''
session = ''
userequipments = None   #JSONList
usercards = None        #JSONList
userquests = None       #JSONList
newsid = None           #string (unicode)
teamlist = None         #JSONList
cardequip = None        #JSONList
mapstatus = None        #JSONList
banquetstatus = None    #JSONObject
resources = None        #JSONObject
dataip = None           #string (unicode)

def login():
    global session,userequipments,usercards,userquests,newsid,teamlist,cardequip,mapstatus,banquetstatus,resources,dataip
    url = ip_login + login_url 
    param = {'v': client_version,'u': username, 'key': hashlib.sha1(client_key + password).hexdigest()}
    data = {'session': 'UNLOGIN'}
    req = requests.post(url, params = param, data = data)
    returnjson = json.loads(req.text)
    code = returnjson['code']
    if (code!='1'):
        return False
    session = returnjson['session']
    userequipments = returnjson['userequipments']
    usercards = returnjson['usercarddatas']
    userquests = returnjson['userquests']
    newsid = returnjson['newsid']
    teamlist = returnjson['usergrouplist']
    cardequip = returnjson['usercardequipments']
    mapstatus = returnjson['usermaps']
    banquetstatus = returnjson['userbanquet']
    resources = returnjson['userresources']
    dataip = returnjson['ip']
    #print json.dumps(usercards,ensure_ascii = False)
    return True

def init_user():
    global username
    global password
    print 'initing user...'
    if(os.path.isfile('user.inf')):
        file = open('user.inf','r')
        username = file.readline().replace('\n','')
        password = base64.b64decode(file.readline())
    else:
        username = raw_input("Username: ")
        password = getpass.getpass()
        file = open('user.inf','w')
        file.write(username + '\n')
        file.write(base64.b64encode(password))
        file.close()
    print 'complete.'

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

def select(max):
    sel = -1
    while(sel < 0 or sel > max):
        s = raw_input('输入选项[0-' + str(max) + ']:')
        if(s.isdigit()):
            sel = int(s)
        if(sel < 0 or sel > max):
            print 'Invalid input "' + s + '"'
    return sel

def testjson(s):
    try:
        returnjson = json.loads(s)
    except ValueError:
        print s
        return False, None
    return True, returnjson

def menu():
    print '===================STATUS==================='
    print resources['gamename'] + ', LV ' + resources['level'] + ', ' + resources['exp'] + '/' + resources['upexp']
    print 'Gold: ' + resources['gold'] + ', faith: ' + resources['faith'] + ', food: ' + resources['food']
    print 'session: ' + session
    print '====================MENU===================='
    print '0. 出击（未实装）'
    print '1. FengNa - 领取赛钱箱'
    print '2. News - 文文新闻'
    print '3. Equipments - 物品'
    print '4. Cards - 整备'
    print '5. Quests - 委托'
    print '6. 宴会（未实装）'
    print '7. 锻造（未实装）'
    print '8. 命令行（未实装）'
    print '9. 退出'
    return select(9)

def itemmenu():
    print '==================ITEMMENU=================='
    print '0. 赠送'
    print '1. 出售'
    print '2. 返回'
    return select(2)

def cardmenu():
    print '==================CARDMENU=================='
    print '0. 查看人物'
    print '1. 返回'
    return select(1)

def questmenu():
    print '=================QUESTSMENU================='
    print '0. 刷新任务列表'
    print '1. 敲击任务'
    print '2. 返回'
    return select(2)

def updatedata():
    global userquests
    global newsid
    global resources
    url = dataip + data_url
    param = {'m1': 1}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    # print req.text
    returnjson = json.loads(req.text)
    userquests = returnjson['userquests']
    newsid = returnjson['newsid']
    resources = returnjson['userresources']

def updatequests():
    global userquests
    url = dataip + questdata_url
    param = {'m1': 1}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    returnjson = json.loads(req.text)
    userquests = returnjson

def fengna():
    global resources
    url = dataip + fengna_url
    param = {'m1': 1}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    if(req.text == '0'):
        print '赛钱箱空空如也'
        return
    status, returnjson = testjson(req.text)
    print 'Goldget: ' + returnjson['gold'] + ', Faithget: ' + returnjson['faith'] + ', Foodget: ' + returnjson['food']
    resources['gold'] = unicode(int(resources['gold']) + int(returnjson['gold']))
    resources['faith'] = unicode(int(resources['faith']) + int(returnjson['faith']))
    resources['food'] = unicode(int(resources['food']) + int(returnjson['food']))

def getnews():
    url = dataip + news_url
    param = {'m1': 1}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    status, returnjson = testjson(req.text)
    print 'Title: ' + returnjson['newsname']
    print 'Author: ' + returnjson['actorname']
    print returnjson['newscontent']

def printitem(itemlist):
    for item in itemlist:
        print item['equipmentid'] + '\t' + item['equipmentname'] + ' * ' + item['countnumber']

def senditem():
    itemid = raw_input("Input item id:")
    cardid = raw_input("Input char id:")
    if(not itemid in plists['equipment'] or not cardid in plists['card']):
        print 'Input error.'
        return
    count_str = raw_input("Count:")
    if not count_str.isdigit():
        print 'Input error.'
        return
    count = int(count_str)
    dosenditem(cardid,itemid,count)
    
def dosenditem(cardid,itemid,count):
    url = dataip + gift_url
    param = {'cardid': cardid, 'equipmentid':itemid, 'count': count}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    # print req.text
    updatedata()
    status, returnjson = testjson(req.text)

def sellitem():
    itemid = raw_input("Input item id:")
    if not itemid in plists['equipment']:
        print 'Input error.'
        return
    count_str = raw_input("Count:")
    if not count_str.isdigit():
        print 'Input error.'
        return
    count = int(count_str)
    dosellitem(itemid,count)

def dosellitem(itemid,count):
    url = dataip + sell_url
    param = {'equipmentid':itemid, 'count': count}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    # print req.text
    updatedata()
    status, returnjson = testjson(req.text)

def itemfunc():
    itemlists = {'1':[],'2':[],'3':[],'4':[]}
    for equip in userequipments:
        id = equip['equipmentid']
        num = equip['countnumber']
        compactequip = {'equipmentid': id, 'countnumber': num, 'equipmentname': plists['equipment'][id]['equipmentname']}
        itemlists[plists['equipment'][id]['type']].append(compactequip)
    print 'Weapons:'
    printitem(itemlists['1'])
    print 'Armors:'
    printitem(itemlists['2'])
    print 'Items:'
    printitem(itemlists['3'])
    print 'Materials:'
    printitem(itemlists['4'])
    sel = itemmenu()
    if(sel == 2):
        return
    print '============================================'
    {0:senditem, 1:sellitem}[sel]()

def carddetail(cardlist):
    cardid = raw_input("Input card id:")
    if not cardid in plists['card']:
        print 'Input error.'
        return
    if not cardid in cardlist:
        print 'You do not possess this card.'
        return
    card = cardlist[cardid]
    print cardid + '\t' + card['cardname'] + ', LV' + card['level'] + ', ' + card['exp'] + '/' + card['upexp']
    print 'Loyalty: ' + card['loyalty'] + ', Points: ' + card['feat']
    print 'Skinid: ' + card['skinid'] + ', ' + plists['skin'][card['skinid']]['skinname'] + ', HasSkins: ' + card['haveskinids']
    print 'HP: ' + card['hp'] + ', Def: ' + card['def'] + ', A.rate: ' + card['avoid'] + ', Luck: ' + card['lucky']
    print 'AtkMel: ' + card['atk_mel'] + ', AtkRang: ' + card['atk_rang'] + ', H.rate: ' + card['hitrate'] + ', Crit: ' + card['crit']
    print 'Block: ' + card['block'] + ', Speed: ' + card['speed'] 
    if card['equipment_id_wq'] == '':
        print 'Weapon: None,', 
    else:
        print 'Weapon: ' + card['equipment_id_wq'] + ' ' + plists['equipment'][card['equipment_id_wq']]['equipmentname'] + ',',
    if card['equipment_id_fj'] == '':
        print 'Armor: None'
    else:
        print 'Armor: ' + card['equipment_id_fj'] + ' ' + plists['equipment'][card['equipment_id_fj']]['equipmentname']
    spell_atk = plists['spell'][card['spell_card_id_atk']]
    spell_def = plists['spell'][card['spell_card_id_def']]
    spell_aid = plists['spell'][card['spell_card_id_aid']]
    print 'Spell Atk: ' + card['spell_card_id_atk'] + ' ' + spell_atk['name'] + spell_atk['spell_point'] + ', NeedLevel: ' + spell_atk['need_level'] + ', ' + spell_atk['spell_rate'] + '%'
    print spell_atk['content']
    print 'Spell Def: ' + card['spell_card_id_def'] + ' ' + spell_def['name'] + spell_def['spell_point'] + ', NeedLevel: ' + spell_def['need_level'] + ', ' + spell_def['spell_rate'] + '%'
    print spell_def['content']
    print 'Spell Aid: ' + card['spell_card_id_aid'] + ' ' + spell_aid['name'] + spell_aid['spell_point'] + ', NeedLevel: ' + spell_aid['need_level'] + ', ' + spell_aid['spell_rate'] + '%'
    print spell_aid['content']
    #TODO
    print 'TODO: 加点，切换装备，咕了'

def cardfunc():
    cardlist = {}
    for card in usercards:
        cardlist[card['cardid']] = card
        print card['cardid'] + '\t' + card['cardname']
    sel = cardmenu()
    if(sel == 1):
        return
    print '============================================'
    {0:carddetail}[sel](cardlist)

def questfunc():
    sel = 0
    updatequests()
    while sel != 2:
        operations = {}
        questlist = {}
        for quest in userquests:
            id = quest['questsid']
            questdetail = plists['quests'][id]
            questlist[id] = quest
            if int(quest['acceptflag']) == 0:
                print '[未接受]\t',
                operations[id] = doacceptquest
            elif quest['complete'] == 'false':
                print '[进行中]\t',
                operations[id] = docancelquest
            else:
                print '[已完成]\t',
                operations[id] = None #TODO
            print id + '\t' + questdetail['cyclename'] + questdetail['name']
            # print json.dumps(quest, ensure_ascii=False)
        sel = questmenu()
        if(sel != 2):
            print '============================================'
        if(sel == 0):
            updatequests()
        elif(sel == 1):
            questid = raw_input('Input questid: ')
            if questid not in plists['quests']:
                print 'Invalid input'
            elif questid not in operations:
                print 'Quest not in list'
            else:
                operations[questid](questid,questlist[questid])
    updatedata()

def doacceptquest(questid,quest):
    url = dataip + acceptquest_url
    param = {'questsid':questid}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    # print req.text
    if req.text == 'success':
        quest['acceptflag'] = '1'

def docancelquest(questid,quest):
    url = dataip + acceptquest_url
    param = {'questsid':questid}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    # print req.text
    if req.text == 'success':
        quest['acceptflag'] = '0'

def dosubmitquest(questid,quest):
    url = dataip + submitquest_url
    param = {'questsid':questid}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    # print req.text
    status, returnjson = testjson(req.text)
    updatequests()

if __name__ == '__main__':
    init_user()
    init_plist()
    if(login()==False):
        print 'Login failed.'
        print 'Please delete user.inf and login again.'
        #TODO: Enter username and password again at this situation
        exit()
    print 'Login success.'
    #exit()
    while(1):
        sel = menu()
        print '============================================'
        {
            0: None, 1: fengna, 2: getnews,
            3: itemfunc, 4: cardfunc, 5: questfunc,
            6: None, 7: None, 8: None, 9: exit,
        }[sel]()
