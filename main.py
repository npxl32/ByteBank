import json
import numpy as np
import leaderboard
import notifications_transactions
import pay_message_check as mc
from pathlib import Path


startmoney = 1000

data = {
}


def read_file():
    path = Path(__file__).parent / 'data.txt'
    with open(path, "r") as f:
        file_contents = f.read()
        return(file_contents)

def write_file(content):
    path = Path(__file__).parent / 'data.txt'
    with open(path, "w") as f:
        f.write(json.dumps(content))

def add_save(key, value):
    data = json.loads(read_file())
    data[key] = value
    write_file(data)
    #print(f"Added user: {key} with balance: {value}")  # Print confirmation message
    return "done"

def get_value(username):
    data = dict(json.loads(read_file()))
      # Print the loaded data dictionary

    if not username in data:
        add_save(username, startmoney)

    return data.get(username)

def pay_user(from_user, to_user, amount, message):

    data = json.loads(read_file())
    message_id = mc.get_comment_id(from_user, message)
    print(message_id)

    message_id = str(message_id.id)
    print(message_id)
    
    if not to_user in data:
        data[to_user] = startmoney 
        write_file(data)

    if not int(data.get(from_user)) >= int(amount) or int(amount) <= 0:
            print("failed")
            return("failed")
    else:
        data[from_user] = int(data.get(from_user)) - int(amount)
        data[to_user] = int(data.get(to_user)) + int(amount)
        write_file(data)
        notifications_transactions.new_notification(to_user, from_user, amount, message_id)
       
        return("successful")
    
def view_notifications(user):
    raw_notifications_string = notifications_transactions.view_notifications(user)
    #print(f"DEBUG: String received from notifications_transactions: '{raw_notifications_string}'") # Add this line
    processed_notifications = append_to_notifications_string_based(raw_notifications_string)
    #print(processed_notifications)
    return processed_notifications
    
        
def sort():
    output = leaderboard.sort(json.loads(read_file()))
    return()


def gift_user(to_user, amount):

    data = json.loads(read_file())


    if not to_user in data:
        data[to_user] = startmoney 
        write_file(data)

    else:
        data[to_user] = int(data.get(to_user)) + int(amount)
        write_file(data)
        notifications_transactions.new_notification(to_user, "ByteBank", amount)
       
        return("Successful Gifting")
        
        
        
        
        




#FUNCTIONS

#The following script is made by gemini
# wow okay wow. incredible
# you needed AN AI for this???

def append_to_notifications_string_based(data_string):
    """
    Appends a new value to the end of each notification,
    treating the last segment as a string.

    Args:
        data_string: A string containing multiple notifications separated by '|'.

    Returns:
        A string with processed notifications, where each original notification
        now has an additional comma-separated value at the end.
    """
    notifications = data_string.split('|')
    processed_notifications = []

    for notification in notifications:
        parts = notification.strip().rsplit(',', 1)

        if len(parts) == 2:
            # notification_body is everything before the last comma
            notification_body = parts[0]
            # last_value_str is the content after the last comma (e.g., '478587997', 'n/a')
            last_value_str = parts[1].strip()

            # --- YOUR CUSTOM LOGIC GOES HERE ---
            # This is where you determine the 'value_to_append' based on 'last_value_str'.
            # Only put the code that calculates what you want to add.

            # If you want to use the result of mc.get_content(last_value_str):
            value_to_append = mc.get_content(last_value_str)

            # If you wanted other conditional logic *in addition* to or instead of mc.get_content,
            # you would put it here. For example, if get_content returns "n/a", maybe you want "No Message":
            # if value_to_append == "n/a":
            #     value_to_append = "No Message"
            # elif last_value_str.isdigit():
            #     value_to_append = f"Message ID: {value_to_append}"
            # else:
            #     value_to_append = "Invalid ID"


            # Ensure 'value_to_append' is always a string.
            # -----------------------------------------------

            # Reconstruct the notification by appending the new value
            reconstructed_notification = f"{notification},{value_to_append}"
            processed_notifications.append(reconstructed_notification)
        else:
            # Handles malformed notifications (no comma found for splitting)
            #print(f"Warning: Malformed notification (no comma found for splitting): '{notification}'. Appending original without modification.")
            processed_notifications.append(notification)

    return '|'.join(processed_notifications)



    

    


