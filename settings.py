import json
import os
import platform


<<<<<<< HEAD
=======
# TODO: Anything other than darwin and windows will cause an error
>>>>>>> b458c2bca592641c3a61e7a6868c83c247aea1b9
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
