from logging import debug
from flask import Flask
from flask import render_template, request, jsonify
import json
import os
import platform
from pyfladesk import init_gui

from src.base import RequirementsGenerator

app = Flask(__name__)


def generate_tree():
    # Get all directory information directly under the default path written in settings.json
    os_name = platform.system()
    user_name = os.getlogin()
    path = settings["os"][os_name].replace("<user_name>", user_name)
    
    # Store the retrieved information in a dict
    main_data = {"data": list()}
    for data in os.walk(path):
        base_dict = {
            "id": "",
            "parent": "",
            "text": ""
            }
        
        if os_name == "Windows":
            dir_constract = data[0]
            dir_list = dir_constract.split("\\")
            parent = "\\".join(dir_list[:-1])

        elif os_name == "Darwin":
            dir_constract = data[0].replace("/", "//")
            dir_list = dir_constract.split("//")
            parent = "//".join(dir_list[:-1])
            
        child = dir_list[-1]

        base_dict["id"] = dir_constract
        base_dict["text"] = child
        base_dict["parent"] = parent

        if path == data[0]:
            base_dict["parent"] = "#"

        main_data["data"].append(base_dict)

    with open(f"{os.getcwd()}\\static\\tree.json", "w", encoding="utf-8") as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)

# generate requirements.txt(main)
@app.route("/generate", methods=["POST"])
def generate():
    language = request.form["language"]
    selected_dirs = request.form["dir_list"]
    dirs = list(set(selected_dirs.split(",")))

    for dir in dirs:
        RequirementsGenerator(dir, language)

    return jsonify()

# update directory information
@app.route("/update", methods=["POST"])
def update():
    generate_tree()
    return jsonify()

# base
@app.route("/")
def base():
    if not os.path.exists(f"{os.getcwd()}\\static\\tree.json"):
        generate_tree()

    lang_data = {lang.capitalize(): lang for lang in settings["languages"]}
    return render_template("main.html", data=lang_data)

# Global variables are currently more efficient. maybe...
data = open(f"{os.getcwd()}\\src\\settings.json", "r")
settings = json.load(data)

if __name__ == "__main__":
    app.run(debug=True)