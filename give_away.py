import json
from datetime import datetime
from pathlib import Path

def read_users():
    path = Path(__file__).parent / 'give_away_users.txt'
    with open(path, "r") as f:
        file_contents = f.read()
        return(json.loads(file_contents))

def read_info():
    path = Path(__file__).parent / 'give_away_specification.txt'
    with open(path, "r") as f:
        file_contents = f.read()
        return(json.loads(file_contents))

def write_file(content):
    path = Path(__file__).parent / 'give_away_users.txt'
    with open(path, "w") as f:
        f.write(json.dumps(content))

def check_time():
    # this smells suspiciously like vibecode

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