#coding: utf8
# libraries
import json     #analyze json
import hashlib  #calculate SHA1
import getpass  #enter password
import requests #HTTP POST
import io       #write unicode into file

# modules
import plists
import userinf
import utils
import general
import equipments
import card
import quest
import banquet
import battle
import db

# Client Constants

def login():
    url = db.ip_login + db.login_url 
    param = {'v': db.client_version,'u': userinf.username, 'key': hashlib.sha1(db.client_key + userinf.password).hexdigest()}
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
    print '0. Battle - 出击'
    print '1. FengNa - 领取赛钱箱'
    print '2. News - 文文新闻'
    print '3. Equipments - 物品'
    print '4. Cards - 整备'
    print '5. Quests - 委托'
    print '6. Banquet - 宴会'
    print '7. 锻造（未实装）'
    print '8. 命令行（未实装）'
    print '9. 退出'
    return utils.select(9)

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
            0: battle.battlefunc, 1: general.fengna, 2: general.getnews,
            3: equipments.itemfunc, 4: card.cardfunc, 5: quest.questfunc,
            6: banquet.banquetfunc, 7: None, 8: None, 9: exit,
        }[sel]()
