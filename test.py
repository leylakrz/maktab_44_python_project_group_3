from user_json import *
box = 'Send'
num = 1
data = read_json()
for item_delete in data['data']:
    if item_delete["User"] == 'roya':
        print(item_delete[box][num])