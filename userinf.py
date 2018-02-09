#coding: utf8
import os
import base64

# User info (client variants)
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

def init_user():
    global username, password
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

