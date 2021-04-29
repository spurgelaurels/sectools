import json
import sys
from collections import OrderedDict


with open(sys.argv[1]) as f:
  data_pass = json.load(f)



#for k in data_pass['items']: 
#    print ('Name: ' + k['name'])

unique = { each['name'] : each for each in data_pass['items'] }.values()

for i in unique:
    print ('Name: ' + i['name'])
    print ('User: ' + i['login.username'])
    print ('Pass: ' + i['login.password'])
    
