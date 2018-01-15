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
fengna_url = 'TouHouServer/actor/fengna'
news_url = 'TouHouServer/actor/newsdata'
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
    if (code==1):
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

def menu():
    print '===================STATUS==================='
    print resources['gamename'] + ', LV ' + resources['level'] + ', ' + resources['exp'] + '/' + resources['upexp']
    print 'Gold: ' + resources['gold'] + ', faith: ' + resources['faith'] + ', food: ' + resources['food']
    print 'session: ' + session
    print '====================MENU===================='
    print '0. 出击（未实装）'
    print '1. FengNa - 领取赛钱箱'
    print '2. News - 文文新闻'
    print '3. 物品（半实装）'
    print '4. 整备（未实装）'
    print '5. 委托（未实装）'
    print '6. 宴会（未实装）'
    print '7. 锻造（未实装）'
    print '8. 退出'
    return select(8)

def itemmenu():
    print '==================ITEMMENU=================='
    print '0. 赠送'
    print '1. 出售'
    print '2. 返回'
    return select(2)

def fengna():
    global resources
    url = dataip + fengna_url
    param = {'m1': 1}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    if(req.text == '0'):
        print '赛钱箱空空如也'
        return
    returnjson = json.loads(req.text)
    print 'Goldget: ' + returnjson['gold'] + ', Faithget: ' + returnjson['faith'] + ', Foodget: ' + returnjson['food']
    resources['gold'] = unicode(int(resources['gold']) + int(returnjson['gold']))
    resources['faith'] = unicode(int(resources['faith']) + int(returnjson['faith']))
    resources['food'] = unicode(int(resources['food']) + int(returnjson['food']))

def getnews():
    url = dataip + news_url
    param = {'m1': 1}
    data = {'session': session}
    req = requests.post(url, params = param, data = data)
    returnjson = json.loads(req.text)
    print 'Title: ' + returnjson['newsname']
    print 'Author: ' + returnjson['actorname']
    print returnjson['newscontent']

def printitem(itemlist):
    print 'ID\tname'
    for item in itemlist:
        print item['equipmentid'] + '\t' + item['equipmentname'] + ' * ' + item['countnumber']

def itemfunc():
    print 'items'
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
    {0:None, 1:None}[sel]()

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
            3: itemfunc, 4: None, 5: None,
            6: None, 7: None, 8: exit
        }[sel]()
