import os, sys

#LOCKFILE = "/tmp/cloud_requests.lock"

#if os.path.exists(LOCKFILE):
 #   print("Another instance is already running. Exiting.")
  #  sys.exit(1)

#with open(LOCKFILE, "w") as f:
#    f.write(str(os.getpid()))

#atexit.register(lambda: os.remove(LOCKFILE) if os.path.exists(LOCKFILE) else None)

#import signal, sys

#def handler(sig, frame):
#    print("Received signal:", sig, "? shutting down")
#    sys.exit(0)

#signal.signal(signal.SIGTERM, handler)
#signal.signal(signal.SIGINT, handler)

import scratchattach as sa
import time
import traceback
import main
import profiles
import notifications_transactions
import leaderboard
import my_secrets  # This imports USERNAME and PASSWORD

platform = "s"
ver_project = "1026899140"
ver_time = {}

if platform == "s":
    
    session = sa.login(my_secrets.USERNAME, my_secrets.PASSWORD)
    cloud = session.connect_cloud("1026899140") #replace with your project id


    client = cloud.requests()
    
if platform == "tw":
    #session = sa.login(my_secrets.USERNAME, my_secrets.PASSWORD)
    #cloud = session.connect_tw_cloud("026899140", purpose="Bot running ByteBank project", contact="Contact me on scratch: wvzack. Use wvzackscratch@gmail.com for more important matters.")
    #client = cloud.requests()
    
    # thats hilarious
    session = sa.login(my_secrets.USERNAME, my_secrets.PASSWORD)

    cloud = sa.get_tw_cloud("1026899140") #replace with your project id
    client = cloud.requests()


@client.request
def ping(): #called when client receives request
    print("pong")
    return "pong" #sends back 'pong' to the Scratch project

@client.request
def get_balance(user):
    print(client.get_requester().lower())

    try:
        balance = main.get_value(user)
        formatted_message = f"You have {balance} dollar(s)"
        return balance
    except Exception as e:
        print(f"Error retrieving balance for {client.get_requester()}: {e}")
        return "Error retrieving balance. Check the Python console for details."

    

@client.request
def pay(to, amount, message, requester=""):
    if platform == "s":
        
        try:
            user = sa.get_user(to)
            from_user = session.connect_user(client.get_requester().lower()) # Returns a sa.User object
        except:
            return("user non existent")
    if platform == "tw":
        user = sa.get_user(to)
        from_user = session.connect_user(str(requester).lower())


    if from_user.is_new_scratcher() == False:
        
        try:
            print(from_user)
            print(to)
            print(int(amount))

            profiles.check_achievement(user, main.get_value(str(from_user)))
            return_value = main.pay_user(str(from_user), str(to).lower(), amount, message)
            
            if return_value == "failed":
                return("error")
            else:
                return main.get_value(str(from_user))  # Simply return the value from main.pay_user()
        except Exception as e:
            print(e)
            traceback.print_exc()

            return("error")
    else:
        return("error")


@client.request
def get_notifications():
    return main.view_notifications(str(client.get_requester()).lower())

@client.request
def get_all_info(user=""):
    if platform == "s":
        username = str(client.get_requester()).lower()
    if platform == "tw":
        username = str(user.lower())
        if username in ver_time:
            if time() - ver_time[username] < 120:
                bytes = str(main.get_value(username))
        
            notif = main.view_notifications(username)
        
            return bytes + "^" + notif
        else:
            return "verify"
    
    bytes = str(main.get_value(username))
    
    notif = main.view_notifications(username)
    
    return bytes + "^" + notif
    
    
    

@client.request
def clear_notifications(username=""):
    if platform == "s":
        username = str(client.get_requester()).lower()
    if platform == "tw":
        username = str(username.lower())
    notifications_transactions.clear_notifications(username)
    return()



@client.request
def get_leaderboard():
    return leaderboard.get()

def get_profile(user, key):
    return profiles.view_data(user, key)

@client.request
def verify(user):
    comments = project.comments(limit=40, offset=0) #Returns all project comments as list of sa.Comment objects
    code = ver_time[user][1]
    


    return


@client.request
def get_transactions(keyword):
    return notifications_transactions.find_transactions(keyword)


@client.event
def on_ready():
    print("Request handler is running")

client.start() #make sure this is ALWAYS at the bottom of your Python file5