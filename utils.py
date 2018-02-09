#coding: utf8
import json
import numpy
import time

# Select from 0 to max
def select(max):
    sel = -1
    while(sel < 0 or sel > max):
        s = raw_input('输入选项[0-' + str(max) + ']:')
        if(s.isdigit()):
            sel = int(s)
        if(sel < 0 or sel > max):
            print 'Invalid input "' + s + '"'
    return sel

# Input: string
# Converts string to json
# On success: return True and the json
# On failure: return False and None, and print the string
def testjson(s):
    try:
        returnjson = json.loads(s)
    except ValueError:
        print 'ERROR:', s
        return False, None
    return True, returnjson

# Input: json (dict or array)
# Prints a json
def printjson(js):
    print json.dumps(js, ensure_ascii = False)

# Input: string, int
# Draw a line of the length with the string inside it
def drawline(s = '', length = 50):
    s_len = len(s)
    len1 = (length-s_len)/2
    len2 = length-s_len-len1
    line = ''.join(['=' for i in range(len1)]) + s + ''.join(['=' for i in range(len2)])
    print line

# Return 25000 + 10000 * chi2(4)
def chi2_rand():
    return int(numpy.random.chisquare(4)*10000+25000)

# Return 7 + chi2(4) / 2
def chi2_rand_time():
    return numpy.random.chisquare(4)/2 + 7

# Return a string of the current time
def gettime():
    return time.strftime('%Y%m%d_%H%M%S')
