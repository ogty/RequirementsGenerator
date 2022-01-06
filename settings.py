import json
import os


data = open(f"{os.getcwd()}/static/config.json", "r")
CONFIG = json.load(data)
TREE_PATH = f"{os.getcwd()}/static/tree.json"
