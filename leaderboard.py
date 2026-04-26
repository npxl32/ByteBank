import heapq
import json
import main



def read_file():
    f = open("/home/pi/Python_Projects/ByteBank/leaderboard.txt", "r")
    file_contents = f.read()
    f.close()
    return(file_contents)

def write_file(content):
    f = open("/home/pi/Python_Projects/ByteBank/leaderboard.txt", "w")
    f.write(json.dumps(content))
    f.close()

def sort(data):
	
	sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)[:10]
	write_file(sorted_data)
	print(sorted_data)
	
	return(sorted_data)
	
def get():
	data = read_file()
	return(data)


	

