import json
import os
import platform


SPLIT_WORD = "\\" if platform.system() == "Windows" else "/"
data = open(f"{os.getcwd()}{SPLIT_WORD}static{SPLIT_WORD}settings.json", "r")
SETTINGS = json.load(data)
TREE_PATH = f"{os.getcwd()}{SPLIT_WORD}static{SPLIT_WORD}tree.json"
