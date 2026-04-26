import json
from datetime import datetime

def read_users():
    f = open("/home/pi/Python_Projects/ByteBank/give_away_users.txt", "r")
    file_contents = f.read()
    f.close()
    return(json.loads(file_contents))

def read_info():
    f = open("/home/pi/Python_Projects/ByteBank/give_away_specification.txt", "r")
    file_contents = f.read()
    f.close()
    return(json.loads(file_contents))

def write_file(content):
    f = open("/home/pi/Python_Projects/ByteBank/give_away_users.txt", "w")
    f.write(json.dumps(content))
    f.close()

def check_time():
    data = read_info()
    print(data)
    # No need to convert to dict(data) if data is already a dictionary from json.loads
    # data = dict(data)

    now = datetime.now()

    # Convert the 'expires' string from your data to a datetime object
    # Assuming the format in give_away_specification.txt is "%Y-%m-%d %H:%M"
    expiration_time_str = data["expires"]
    expiration_time = datetime.strptime(expiration_time_str, "%Y-%m-%d %H:%M")

    if now < expiration_time:
        return True
    else:
        return False

def check_type():
    data = read_info()
    print(data)
    type = data["type"]
    return type

print(check_type())
