from datetime import datetime, timedelta

pending = {}
hasPendingVerification = set()

def pendVerification(username, code, goal):
  expiry = datetime.now() + timedelta(minutes=10)
  newVerification = {"username": username, "expiry": expiry, "goal": goal}

  if not username in hasPendingVerification:
    hasPendingVerification.add(username)
    pending[code] = newVerification # no need to ratelimit because scratch has its own cloud rate limits
  else:
    verificationsToPop = []
    for verification in pending:
      if pending[verification].get('username').lower() == username.lower():
        verificationsToPop.append(verification)
    
    for verification in verificationsToPop:
      pending.pop(verification)

    pending[code] = newVerification
    

def checkVerification(project, username):
  comments = project.comments(limit=40, offset=0)
  for comment in comments:
    author = comment.author()

    content = comment.content.strip()
    verifyResult = verifyCode(content, author.username, username)
    if verifyResult:
      return verifyResult
  
  return None

def verifyCode(message, username, expectedUsername):
  now = datetime.now()
  if pending.get(message):
    verification = pending.get(message)

    if verification.get('username').lower() == username.lower():
      if username == expectedUsername:
        if now < verification.get('expiry'):
          hasPendingVerification.remove(username)
          return pending.pop(message)
  
  return False