print("----------------------------------------------------------------")
print("PyCob Deploy")
print("----------------------------------------------------------------")

import os
import sys
from pathlib import Path
import gitignore_parser
import requests
import re

args = sys.argv[1:]
print("Args: " + str(args))

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
        error_str = "API request failed with status code " + str(response.status_code)
        print(error_str)
        return {"error": error_str}

    try:
        json_response = response.json()
        return json_response
    except:
        print("API request failed to return valid JSON.")
        return {"error": "API request failed to return valid JSON."}

def _url_for_file_storage(file_name):
    file = {
        "filename": file_name,
    }
    rv = __send_api_request("store_file", file, api_key)

    if 'url' in rv:
        return rv['url']
    else:
        print("Error: Unable to get URL for file storage")
        return ""

def store_code(file_path: str):
    remote_file_path = "code" + file_path[1:]
    url = _url_for_file_storage(remote_file_path)

    if url == "":
        print("Error: Unable to store file")
        return

    # Put file with Content-Type: application/octet-stream
    file = open(file_path, 'rb')
    r = requests.put(url, data=file, headers={'Content-Type': 'application/octet-stream'})
    file.close()
    print("Response: " + str(r.status_code))

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
        if not path.startswith("./."):
            try:
                if matches and matches(os.path.join(root, file)):
                    continue
            
                if dotfile_pattern.match(file):
                    continue
            except:
                continue
            
            i = i + 1
            if i < max_files:
                print(f"Uploading... File #{i}: {path}")
                store_code(path)
            else:
                print(f"Reached max file count. Skipping... File #{i}: {path}")

print("Done Uploading. Beginning deployment...")
__send_api_request("begin_build", {}, api_key)                

