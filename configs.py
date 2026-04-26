import json
from pathlib import Path

def load_json(filename):
  path = Path(__file__).parent / filename
  try:
    with open(path, 'r') as f:
      file_content = f.read()
      returnedfile = json.loads(file_content)
      returnedfile.update(loaded=True)
    
      return returnedfile
  except FileNotFoundError:
    return {"loaded": False, "error": "fileError"}
  except json.decoder.JSONDecodeError as e:
    return {"loaded": False, "error": "jsonDecode", "details": str(e)}
  
  return None

secrets = load_json('.secrets.json')
config = load_json('.config.json')