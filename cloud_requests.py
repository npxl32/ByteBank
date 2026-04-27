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

from configs import secrets, config
from validate_secrets_and_config import check

check(secrets, config)

#print('test')
#sys.exit(0)

import scratchattach as sa
import time
import traceback
import main
import profiles
import notifications_transactions
import leaderboard
import secrets as python_secrets_module # i should not have named the other thing secrets
from datetime import datetime
import turbowarp_verify_check

platform = "tw"
ver_project = config.get('project')
ver_time = {}

tw_verification_project = config.get('tw_verification_project')
if not tw_verification_project:
    print("There is no TurboWarp verification project set in your .config.json. Set the property \"tw_verification_project\" to the project ID of the verification project, so users can comment on it. This is required for TurboWarp support.")
    if platform == "tw":
        print("Exiting due to no TurboWarp verification project.")
        sys.exit(1)
else:
    tw_verification_project = sa.get_project(tw_verification_project)

if platform == "s":
    
    if secrets.get('password'):
        session = sa.login(secrets.get('username'), secrets.get('password'))
    elif secrets.get('session'):
        session = sa.login_by_id(secrets.get('session'), username=secrets.get('username'))

    cloud = session.connect_cloud(config.get('project')) #replace with your project id


    client = cloud.requests()
    
if platform == "tw":
    if not config.get('tw_purpose') or not config.get('tw_contact'):
        print("You will need to set up bot purpose and contact information in your .config.json to use TurboWarp!")
        print("Example:")
        print("{")
        print("...")
        print("  \"tw_purpose\":\"The reason I am using TurboWarp cloud variables is to operate the bot that is running ByteBank\",")
        print("  \"tw_contact\":\"You can contact me on my Scratch profile which is myusername123.\"")
        print("}")
        print("This is required so the TurboWarp developer knows why you are using the TurboWarp cloud servers and how to contact you.")
        sys.exit(1)

    if secrets.get('password'):
        session = sa.login(secrets.get('username'), secrets.get('password'))
    elif secrets.get('session'):
        session = sa.login_by_id(secrets.get('session'), username=secrets.get('username'))

    cloud = session.connect_tw_cloud(config.get('project'), purpose=config.get('tw_purpose'), contact=config.get('tw_contact'))
    client = cloud.requests()

    cloud = sa.get_tw_cloud(config.get('project')) #replace with your project id
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
def check_tw_verify(requester):
    if platform == 'tw':
        try:
            # todo: change so that it sends a "Verifying..." message to the user and then later sends back a success or failure
            # actually maybe not...
            verifyResult = turbowarp_verify_check.checkVerification(tw_verification_project, str(requester))
            print(verifyResult)
            if verifyResult:
                print(str(requester) + " verified on TurboWarp for " + verifyResult.get('goal'))
                return verifyResult.get('goal')
            else:
                print(str(requester) + " failed to verify on TurboWarp")
                return "n"
        except Exception as e:
            print("Error TurboWarp verifying " + str(requester) + ": " + str(e))
            traceback.print_exc()
            return "n"
        
    elif platform == 's':
        return "n"    

@client.request
def pay(to, amount, message, requester=""):
    if platform == "s":
        
        try:
            user = sa.get_user(to)
            from_user = session.connect_user(client.get_requester().lower()) # Returns a sa.User object
        except:
            return("user non existent")
    if platform == "tw":
        try:
            user = sa.get_user(to)
        except:
            return "user non existent"

        token = python_secrets_module.token_hex(12)
        turbowarp_verify_check.pendVerification(requester, token, 'pay')
        return "verif" + token
        #from_user = session.connect_user(str(requester).lower())


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