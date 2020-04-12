import requests as re
import json
import random

def dummyAPI1():
    print '#'*40
    print 'Welcome to Dummy API 1'
    print "press any key for random name or 'q' to quit "
    inp = raw_input()
    if inp == 'q':
        print "END OF Dummy API 1"
        print '#' * 40
        return
    r = re.get('http://jsonplaceholder.typicode.com/users')
    num = random.randint(0,9)
    js = json.loads(r.text)
    print js[num]['username']

    print "END OF Dummy API 1"
    print '#'*40
