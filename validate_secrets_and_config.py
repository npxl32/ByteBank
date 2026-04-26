import sys
has_sent_tw_warning = False

def check(secrets, config):
  global has_sent_tw_warning
  
  if not secrets.get('loaded'):
    secrets_error = secrets.get('error')
    match secrets_error:
      case 'fileError':
        print('Error! No secrets file was found, create a file in JSON format in the same directory as ByteBank named ".secrets.json" and set two properties, "username" and "password" to be your bot\'s Scratch username and password.')
      case 'jsonDecode':
        print('Error! There was a JSON error when parsing .secrets.json: ' + secrets.get('details'))
      case _:
        print('Error! There was some error loading your secrets file.')
    sys.exit(1)


  if not secrets.get('username'):
    print("Error! No username was set in your secrets file. Set one. It must be set to your bot's Scratch username.")
    sys.exit(1)
  if not secrets.get('password') and not secrets.get('session'):
    print("Error! No password or session ID was set in your secrets file. Set one. It must be set to your bot's Scratch password OR your session ID.")
    sys.exit(1)

  if not config.get('loaded'):
    config_error = secrets.get('error')
    match config_error:
      case 'fileError':
        print('Error! No config file was found, create a file in JSON format in the same directory as ByteBank named ".config.json", refer to documentation for more info.')
      case 'jsonDecode':
        print('Error! There was a JSON error when parsing .config.json: ' + config.get('details'))
      case _:
        print('Error! There was some error loading your config file.')
    sys.exit(1)

  if not config.get('project'):
    print("Error! No project id was set in your config file. Set one. It must be set to your ByteBank project ID.")
    sys.exit(1)

  if not has_sent_tw_warning and (not config.get('tw_contact') or not config.get('tw_purpose')):
    has_sent_tw_warning = True
    print("Note: You will need a reason for using TurboWarp's cloud variables and contact info in your .config.json if you want to support TurboWarp's cloud variables. Set the properties tw_contact (string containing Scratch or email contact info) and tw_purpose (the reason you are using TurboWarp cloud variables) in your .config.json to do this. (Preferably keep them short)")