import json

def read_file(filename):
    """Reads a file and attempts to parse it as JSON. Returns an empty list if not valid JSON."""
    with open(filename, "r") as f:
        content = f.read()
        
        return json.loads(content)

def write_file(filename, content):
    """Writes content to a file, handling lists and other data types."""
    if isinstance(content, list):  # Check if content is a list
        json_content = json.dumps(content)
    else:
        json_content = str(content)  # Handle non-list content (e.g., dictionary)
    with open(filename, "w") as f:
        f.write(json_content)

def vote(username, choice):
    """Casts a vote for a choice and updates the vote data."""
    usernames = read_file("vote_usernames.txt")
    votes = dict(read_file("vote_choices.txt"))

    if username not in usernames:
        usernames.append(username)
        
        if choice not in votes:
            votes[choice] = 0
    
        vote2 = int(votes[choice])
    
        vote2 += 1  # Increment the count for the chosen option
    
        votes[choice] = vote2
        
        write_file("vote_choices.txt", votes)  # Write votes dictionary as JSON
    
        write_file("vote_usernames.txt", usernames)

vote("wvzack", "test")
print(read_file("vote_usernames.txt"))