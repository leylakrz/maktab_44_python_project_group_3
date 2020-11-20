import json


# write_json: let to write info to json file
def write_json(data, filename='user.json'):
    with open(filename, "+w") as f:
        json.dump(data, f, indent=4)


# user_dict = {"name": "users", "data": []}
# write_json(user_dict)

# add_user_info: add info to data list
def add_user_info(user_info, filename='user.json'):
    data = read_json(filename)
    temp = data['data']
    temp.append(user_info)
    write_json(data)


# read_json: read data from json file
def read_json(file_name='user.json'):
    with open(file_name, 'r') as f:
        data = json.load(f)
        return data
