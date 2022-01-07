import json
import os


DESKTOP_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
TOP_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(TOP_DIR, "static")
TREE_PATH = os.path.join(STATIC_DIR, "tree.json")

with open(os.path.join(STATIC_DIR, "config.json"), "r") as config_file:
    CONFIG = json.load(config_file)
