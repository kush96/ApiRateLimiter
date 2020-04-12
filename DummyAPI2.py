import requests as re
import json
import random

# r = re.get('http://jsonplaceholder.typicode.com/users')
# print r.text
# num = random.randint(0,9)
# js = json.loads(r.text)
#
def dummyAPI2():
    print '#'*40
    print 'Welcome to Dummy API 2'
    print "press any key for random phone number or 'q' to quit "
    inp = raw_input()
    if inp == 'q':
        print "END OF Dummy API 2"
        print '#' * 40
        return

    r = re.get('http://jsonplaceholder.typicode.com/users')
    num = random.randint(0,9)
    js = json.loads(r.text)
    print js[num]['phone']

    print "END OF Dummy API 2"
    print '#'*40