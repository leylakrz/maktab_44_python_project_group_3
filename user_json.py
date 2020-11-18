# from user import User
import json
# from message import Message
# from bson import json_util
#



def write_json(data, filename='user.json'):
    with open(filename, "+w") as f:
        json.dump(data, f, indent=4)

# user_dict = {"name": "users", "data": [{
#             "User": "",
#             "Password": "}$^\u0001/\u00172kk&\u000b\u0004'\u000b`\u0003\u0016\u05de\u001b2Y",
#             "Inbox": [],
#             "Draft": [],
#             "Send": [],
#             "Salt": "2852635b7d89f7caf01dbea9b422dbd9b8baaf2008937dfb6551d855c5bfbe20"
#         }]}
# write_json(user_dict)


def add_user_info(user_info, filename='user.json'):
    data = read_json(filename)
    temp = data['data']
    temp.append(user_info)
    write_json(data)

def read_json(file_name='user.json'):
    with open(file_name, 'r') as f:
        data = json.load(f)
        return data

#
# m = Message(sender='roya', receiver='ali', body='hi roya', title='hi')
# k = Message(sender='Sadegh', receiver='ali', body='hi roya', title='hi')

# r = User("roya", "123")
# user_info = {"Id": 1, "user": r.username, "Pass": list(r.hash_password), "Draft": []}
# add_user_info(user_info)
# data = read_json()
# for item in data['data']:
#     if item['Id'] == 1:
#         item['Draft'].append(json.dumps(m.__dict__))
#         item['Draft'].append(json.dumps(k.__dict__))
#
#     write_json(data)
#
# for item in data['data']:
#     item["Draft"].remove(json.dumps(m.__dict__))
#     write_json(data)


