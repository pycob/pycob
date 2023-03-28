import os
import sys
from pathlib import Path
import gitignore_parser
import requests
import re
import uuid

build_id = str(uuid.uuid4())
print("----------------------------------------------------------------")
print(f"🌽 PyCob Deploy ---- ID: {build_id} 🌽")
print("----------------------------------------------------------------")

args = sys.argv[1:]

api_key = None

if len(args) > 0:
    print("Checking for API key in args...")
    api_key = args[0]

# Check for API key
if api_key is None or api_key == "":
    # Check PYCOB_API_KEY environment variable
    print("Checking for API key in PYCOB_API_KEY environment variable...")
    api_key = os.environ.get("PYCOB_API_KEY")

    if api_key is None:
        if Path("pycob_api_key.txt").is_file():
            print("Checking for API key in pycob_api_key.txt...")
            f = open("pycob_api_key.txt", "r")
            api_key = f.read()

        if api_key is None:
            print("No API key found. ")
            print("Go to https://www.pycob.com to get an API key.")
            # Exit
            sys.exit(1)

def __send_api_request(endpoint: str, data: dict, api_key: str) -> dict:
    response = requests.post("https://api.pycob.com/rpc/"+endpoint, json=data, headers={"PYCOB-API-KEY": api_key})
    
    if response.status_code != 200:
        error_str = f"🛑 API request '{endpoint}' failed with status code " + str(response.status_code)
        print(error_str)
        return {"error": error_str}

    try:
        json_response = response.json()
        return json_response
    except:
        print("🛑 API request failed to return valid JSON.")
        return {"error": "API request failed to return valid JSON."}

def _url_for_file_storage(file_name):
    file = {
        "filename": file_name,
    }
    rv = __send_api_request("store_file", file, api_key)

    if 'url' in rv:
        return rv['url']
    else:
        print("🛑 Error: Unable to get URL for file storage")
        return ""

def store_code(file_path: str, build_id: str):
    remote_file_path = "code/" + build_id + file_path[1:]
    url = _url_for_file_storage(remote_file_path)

    if url == "":
        print("Error: Unable to store file")
        return

    # Put file with Content-Type: application/octet-stream
    file = open(file_path, 'rb')
    r = requests.put(url, data=file, headers={'Content-Type': 'application/octet-stream'})
    file.close()

    if r.status_code != 200:
        print("🛑 Error: Unable to store file")
        return
    else:
        print("✅")

# Recursively list all files in the current directory, excluding everything covered by .gitignore

# Get the list of ignored files
try:
    matches = gitignore_parser.parse_gitignore(".gitignore")
except:
    matches = None

# Any dotfile in any subdirectory is ignored
dotfile_pattern = re.compile(r'^\..*', re.IGNORECASE)


i = 0
max_files = 25


for root, dirs, files in os.walk("."):
    for file in files:
        path = os.path.join(root, file)
        if not path.startswith("./.") and not path.startswith("./venv/") and not path.startswith("./tmp/"):
            try:
                if matches and matches(os.path.join(root, file)):
                    continue
            
                if dotfile_pattern.match(file):
                    continue
            except:
                continue
            
            i = i + 1
            if i < max_files:
                print(f"📤 Uploading... File #{i}: {path}")
                store_code(path, build_id)
            elif i == max_files:
                print(f"Reached max file count. Skipping the rest...")

print("🍿 Done Uploading.")
server_response = __send_api_request("upload_complete", {"build_id": build_id}, api_key)                

if 'app_name' in server_response:
    app_name = server_response['app_name']

print("----------------------------------------------------------------")
print("🌽         Finish at https://www.pycob.com/deploy            🌽")
print("----------------------------------------------------------------")

import webbrowser
webbrowser.open("https://www.pycob.com/deploy?build_id="+build_id+"&app_name="+app_name)