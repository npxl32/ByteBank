import heapq
import json
import main

from pathlib import Path

def read_file():
    path = Path(__file__).parent / 'leaderboard.txt'
    with open(path, "r") as f:
        file_contents = f.read()
        return(file_contents)

def write_file(content):
    path = Path(__file__).parent / 'leaderboard.txt'
    with open(path, "w") as f:
        f.write(json.dumps(content))
    
def sort(data):
	sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)[:10]
	write_file(sorted_data)
	print(sorted_data)
	
	return(sorted_data)
	
def get():
	data = read_file()
	return(data)


	

