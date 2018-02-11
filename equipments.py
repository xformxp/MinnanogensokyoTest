#coding: utf8
import plists
import utils
import userinf
import requests
import general
import db

def itemmenu():
    utils.drawline('ITEMMENU')
    print '0. 赠送'
    print '1. 出售'
    print '2. 返回'
    return utils.select(2)

def printitem(itemlist):
    for item in itemlist:
        print item['equipmentid'] + '\t' + item['equipmentname'] + ' * ' + item['countnumber']

def senditem():
    utils.drawline('SEND')
    itemid = raw_input("Input item id: ")
    cardid = raw_input("Input char id: ")
    if(not itemid in plists.get_plist('equipment') or not cardid in plists.get_plist('card')):
        print 'Input error.'
        return
    count_str = raw_input("Count: ")
    if not count_str.isdigit():
        print 'Input error.'
        return
    count = int(count_str)
    dosenditem(cardid,itemid,count)
    
def dosenditem(cardid,itemid,count):
    url = userinf.dataip + db.gift_url
    param = {'cardid': cardid, 'equipmentid':itemid, 'count': count}
    data = {'session': userinf.session}
    req = requests.post(url, params = param, data = data)
    # print req.text
    status, returnjson = utils.testjson(req.text)
    #TODO: analyze results(char)
    #utils.printjson(returnjson)
    print plists.get_plist('card')[cardid]['cardname'], u'获得', plists.get_plist('equipment')[itemid]['equipmentname'], '*', count

def sellitem():
    utils.drawline('SELL')
    itemid = raw_input("Input item id: ")
    if not itemid in plists.get_plist('equipment'):
        print 'Input error.'
        return
    count_str = raw_input("Count: ")
    if not count_str.isdigit():
        print 'Input error.'
        return
    count = int(count_str)
    dosellitem(itemid,count)

def dosellitem(itemid,count):
    url = userinf.dataip + db.sell_url
    param = {'equipmentid':itemid, 'count': count}
    data = {'session': userinf.session}
    req = requests.post(url, params = param, data = data)
    # print req.text
    status, returnjson = utils.testjson(req.text)
    general.analyze_results(returnjson)

def itemfunc():
    utils.drawline('EQUIPMENT')
    itemlists = {'1':[],'2':[],'3':[],'4':[]}
    for equip in userinf.userequipments:
        id = equip['equipmentid']
        num = equip['countnumber']
        compactequip = {'equipmentid': id, 'countnumber': num, 'equipmentname': plists.get_plist('equipment')[id]['equipmentname']}
        itemlists[plists.get_plist('equipment')[id]['type']].append(compactequip)
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
    {0:senditem, 1:sellitem}[sel]()

