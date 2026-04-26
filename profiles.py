
import json
import os
from datetime import datetime, timezone

path = "/home/pi/Python_Projects/ByteBank/profile.txt"

def read_file():
    if not os.path.exists(path):
        return "{}"
    with open(path, "r") as f:
        contents = f.read().strip()
    return contents if contents else "{}"

def write_file(content):
    with open(path, "w") as f:
        print(content)
        json.dump(content, f, indent=2)

def add_data(user, key, value):

    user_key = str(user) 
    
    data = json.loads(read_file())

    # Ensure user exists
    if user_key not in data:
        data[user_key] = {}

    # Add or update key
    data[user_key][str(key)] = str(value)
    write_file(data)
    print(f"Added data for {user_key}: {key} = {value}")
    return "done"

def view_data(user="wvzack", key="all"):
    # ... (No change needed here, assuming input user is a string)
    user_key = str(user) # Defensive str conversion
    data = json.loads(read_file())

    if user_key == "all":
        return data
    elif key == "all":
        return data.get(user_key, {})
    else:
        return data.get(user_key, {}).get(key, None)

def add_achievement(user, achievement):
    
    user_key = str(user) 
    
    # Load existing achievements
    data = json.loads(read_file())
    if user_key not in data:
        data[user_key] = {}
    if "achievements" not in data[user_key]:
        data[user_key]["achievements"] = []
        
    # Add to list
    data[user_key]["achievements"].append(achievement)
    write_file(data)
    print(f"🏆 Added achievement '{achievement}' for {user_key}")
    return "done"

def check_achievement(user, balance):
    # ... (No change needed here)
    # bytes
    if balance > 1025:
        add_achievement(user, "decakibibyteaire")