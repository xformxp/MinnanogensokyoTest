#coding: utf8
import plists
import utils
import userinf
import requests
import general
import db

def banquetfunc():
    utils.drawline('BANQUET')
    print userinf.banquetstatus
    if userinf.banquetstatus['state'] == '2':
        banquet_type = userinf.banquetstatus['type']
        print '筹备中:', plists.get_plist('banquet')[banquet_type]['name']
        print '剩余:', userinf.banquetstatus['readyendsecond'] + 's'
        print 'TODO: 快速筹备' #TODO

def dostartbanquet(cardid, banquet_type):
    url = userinf.dataip + db.startbanquet_url
    param = {'cardid': cardid, 'type': banquet_type}
    data = {'session': userinf.session}
    req = requests.post(url, params = param, data = data)

#TODO: banquets
