#coding: utf8
import userinf
import utils
import requests
import db

# Clinet constants

def updatedata():
    url = userinf.dataip + db.data_url
    param = {'m1': 1}
    data = {'session': userinf.session}
    req = requests.post(url, params = param, data = data)
    # print req.text
    status, returnjson = utils.testjson(req.text)
    if status == False:
        return
    userinf.userquests = returnjson['userquests']
    userinf.newsid = returnjson['newsid']
    userinf.resources = returnjson['userresources']

def fengna():
    utils.drawline('FENGNA')
    url = userinf.dataip + db.fengna_url
    param = {'m1': 1}
    data = {'session': userinf.session}
    req = requests.post(url, params = param, data = data)
    if(req.text == '0'):
        print '赛钱箱空空如也'
        return
    status, returnjson = utils.testjson(req.text)
    if status == False:
        return
    analyze_results(returnjson)

def analyze_results(returnjson):
    result_names = ['blueprint','exp','faith','food','gold','leather','steel','stone','wood']
    for name in result_names:
        if returnjson[name] != '0':
            print name + ' get: ' + returnjson[name]
            userinf.resources[name] = unicode(int(userinf.resources[name]) + int(returnjson[name]))
    print 'carddata:',
    utils.printjson(returnjson['userCardDatas'])
    print 'equip:',
    utils.printjson(returnjson['userEquipments'])

def getnews():
    utils.drawline('NEWS')
    url = userinf.dataip + db.news_url
    param = {'m1': 1}
    data = {'session': userinf.session}
    req = requests.post(url, params = param, data = data)
    status, returnjson = utils.testjson(req.text)
    if status == False:
        return
    print 'Title: ' + returnjson['newsname']
    print 'Author: ' + returnjson['actorname']
    print returnjson['newscontent']
