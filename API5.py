import json         #json package
import requests     #requests package

def api5():
    print '#' * 40
    print 'Welcome to API 5'
    curr_base = raw_input('enter base currency or q to quit: ')     # Input Base currency name
    if curr_base =="q":
        print "END OF API 5"
        print '#' * 40
        return
    data = requests.get('https://api.exchangeratesapi.io/latest?base='+curr_base+'')      # Requesting data from the Url after concatinating base curr
    data_format = json.loads(data.text)    # Extracting text from the data
    if 'error' in data_format.keys():      # Checking if error occured or not
        print ('Wrong Currency')
    else:
         print(json.dumps(data_format,sort_keys=True,indent=4))
         print "END OF API 5"
         print '#' * 40