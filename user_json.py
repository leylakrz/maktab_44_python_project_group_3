import json


def write_json(data, filename='user.json'):
    with open(filename, "+w") as f:
        json.dump(data, f, indent=4)


def add_user_info(user_info, filename='user.json'):
    data = read_json(filename)
    temp = data['data']
    temp.append(user_info)
    write_json(data)


def read_json(file_name='user.json'):
    with open(file_name, 'r') as f:
        data = json.load(f)
        return data
