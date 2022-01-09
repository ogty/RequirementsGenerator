import json
import os
import platform


# TODO: Anything other than darwin and windows will cause an error
os_name = platform.system()
if os_name == "Darwin":
    DESKTOP_PATH = os.path.join(os.path.join(os.environ["HOME"]), "Desktop")
elif os_name == "Windows":
    DESKTOP_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

TOP_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(TOP_DIR, "static")
TREE_PATH = os.path.join(STATIC_DIR, "tree.json")

with open(os.path.join(STATIC_DIR, "config.json"), "r") as config_file:
    CONFIG = json.load(config_file)
