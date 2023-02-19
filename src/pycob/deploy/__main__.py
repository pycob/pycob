print("----------------------------------------------------------------")
print("PyCob Deploy")
print("----------------------------------------------------------------")

import os
import sys
from pathlib import Path
import gitignore_parser

args = sys.argv[1:]
print("Args: " + str(args))

if len(args) > 0:
    api_key = args[0]

# Check for API key
if api_key is None:
    # Check PYCOB_API_KEY environment variable
    api_key = os.environ.get("PYCOB_API_KEY")

    if api_key is None:
        if Path("pycob_api_key.txt").is_file():
            # Check for api_key.txt file
            f = open("pycob_api_key.txt", "r")
            api_key = f.read()

        if api_key is None:
            print("No API key found. ")
            print("Go to https://www.pycob.com to get an API key.")
            # Exit
            sys.exit(1)

# Recursively list all files in the current directory, excluding everything covered by .gitignore

# Get the list of ignored files
try:
    matches = gitignore_parser.parse_gitignore(".gitignore")
except:
    matches = None

for root, dirs, files in os.walk("."):
    for file in files:
        path = os.path.join(root, file)
        if not path.startswith("./."):
            try:
                if matches and matches(os.path.join(root, file)):
                    continue
            except:
                continue
            print(path)

