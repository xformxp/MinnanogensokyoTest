#coding: utf8
import plists
import utils
import userinf
import requests
import general
import db

def questmenu():
    utils.drawline('QUESTMENU')
    print '0. 刷新任务列表'
    print '1. 敲击任务'
    print '2. 返回'
    return utils.select(2)

def updatequests():
    global userquests
    url = userinf.dataip + db.questdata_url
    param = {'m1': 1}
    data = {'session': userinf.session}
    req = requests.post(url, params = param, data = data)
    status, returnjson = utils.testjson(req.text)
    if status == False:
        return
    userquests = returnjson

def questfunc():
    utils.drawline('QUEST')
    sel = 0
    updatequests()
    while sel != 2:
        operations = {}
        questlist = {}
        for quest in userquests:
            id = quest['questsid']
            questdetail = plists.get_plist('quests')[id]
            questlist[id] = quest
            if int(quest['acceptflag']) == 0:
                print '[未接受]\t',
                operations[id] = doacceptquest
            elif quest['complete'] == 'false':
                print '[进行中]\t',
                operations[id] = docancelquest
            else:
                print '[已完成]\t',
                operations[id] = dosubmitquest
            print id + '\t' + questdetail['cyclename'] + questdetail['name'] + ': ' + questdetail['true_content']
            # print json.dumps(quest, ensure_ascii=False)
        sel = questmenu()
        if(sel != 2):
            print '============================================'
        if(sel == 0):
            updatequests()
        elif(sel == 1):
            questid = raw_input('Input questid: ')
            if questid not in plists.get_plist('quests'):
                print 'Invalid input'
            elif questid not in operations:
                print 'Quest not in list'
            else:
                operations[questid](questid,questlist[questid])
    general.updatedata()

def doacceptquest(questid,quest):
    url = userinf.dataip + db.acceptquest_url
    param = {'questsid':questid}
    data = {'session': userinf.session}
    req = requests.post(url, params = param, data = data)
    # print req.text
    if req.text == 'success':
        quest['acceptflag'] = '1'

def docancelquest(questid,quest):
    url = userinf.dataip + db.acceptquest_url
    param = {'questsid':questid}
    data = {'session': userinf.session}
    req = requests.post(url, params = param, data = data)
    # print req.text
    if req.text == 'success':
        quest['acceptflag'] = '0'

def dosubmitquest(questid,quest):
    url = userinf.dataip + db.submitquest_url
    param = {'questsid':questid}
    data = {'session': userinf.session}
    req = requests.post(url, params = param, data = data)
    print 'test: submitquest:', req.text #TODO
    status, returnjson = utils.testjson(req.text)
    general.analyze_results(returnjson)
    updatequests()

