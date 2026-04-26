import json
import re
from datetime import datetime, timezone
import main

data = {
}

def read_file():
    f = open("/home/pi/Python_Projects/ByteBank/notifications.txt", "r")
    file_contents = f.read()
    f.close()
    return(file_contents)

def write_file(content):
    f = open("/home/pi/Python_Projects/ByteBank/notifications.txt", "w")
    f.write(json.dumps(content))
    f.close()

def add_data(key, value):
    data = json.loads(read_file())
    data[key] = value
    write_file(data)
    print(f"Added notification to user: {key} notifications: {value}")  # Print confirmation message
    return "done"

def new_notification(user, from_user, amount, message_id):
    timestamp = datetime.now(timezone.utc)
    timestamp = str(timestamp.strftime("%Y-%m-%d %H:%M"))

    data = json.loads(read_file())
    if user in data:
        old_noti = data[user]
        data[user] = old_noti + "|" + from_user + "," + amount + "," + timestamp + "," + message_id  # Update notification
        print(f"Added notification to user: {user} notifications: {data[user]}")
    else:
        data[user] = from_user + "," + amount + "," + timestamp + "," + message_id # Add new user with notification
        print(f"New notification for user: {user} - {data[user]}")
    write_file(data)  # Write updated data
    add_transaction(user + "," + str(main.get_value(user)) + "," + from_user + ","  + str(main.get_value(from_user)) + "," + amount + "," + timestamp + "," + str(message_id) + "\n")
    return "done"


def view_notifications(user):
    data = json.loads(read_file())
    if user in data:
        return_notification = data[user]
        return return_notification
    else:
        return"no notifications"
    
def clear_notifications(user):
    try:
        data = json.loads(read_file())
        del data[user]
        write_file(data)
        return
    except:
        return("failed")
    
def get_transaction_history():
    f = open("/home/pi/Python_Projects/ByteBank/transaction_history.txt", "r")
    file_contents = f.read()
    f.close()
    return(file_contents)

def write_transaction_history(content):
    f = open("/home/pi/Python_Projects/ByteBank/transaction_history.txt", "w")
    f.write(content)
    f.close()

def add_transaction(transaction):
	data = get_transaction_history()
	data = data + transaction
	write_transaction_history(data)
	
def find_transactions(keyword):
	keyword = str(keyword)
	data = str(get_transaction_history())
	strings = re.findall(keyword, data)
	return strings
	
	
	
		
    
    

    
