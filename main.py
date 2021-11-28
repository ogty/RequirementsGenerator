from flask import Flask
from flask import render_template, request, jsonify
import json
import os
import platform
from pyfladesk import init_gui

from src.base import RequirementsGenerator

app = Flask(__name__)


def generate_tree(settings: dict):
    os_name = platform.system()
    user_name = os.getlogin()
    path = settings["os"][os_name].replace("<user_name>", user_name)
    
    main_data = {"data": list()}
    for data in os.walk(path):
        base_dict = {
            "id": "",
            "parent": "",
            "text": ""
            }
        dir_constract = data[0]
        dir_list = dir_constract.split("\\")
        parent = "\\".join(dir_list[:-1])
        child = dir_list[-1]

        base_dict["id"] = dir_constract
        base_dict["text"] = child
        base_dict["parent"] = parent

        if path == data[0]:
            base_dict["parent"] = "#"

        main_data["data"].append(base_dict)

    with open("../static/tree.json", "w", encoding="utf-8") as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)

@app.route("/generate", methods=["POST"])
def generate():
    language = request.form["language"]
    selected_dirs = request.form["dir_list"]
    dirs = list(set(selected_dirs.split(",")))

    for dir in dirs:
        print(dir, language)
        RequirementsGenerator(dir, language)

    return jsonify()

@app.route("/")
def base():
    data = open("../src/settings.json", "r")
    settings = json.load(data)

    generate_tree(settings)
    lang_data = {lang.capitalize(): lang for lang in settings["languages"]}
    return render_template("main.html", data=lang_data)

if __name__ == "__main__":
    init_gui(app, window_title="Requirements.txt Generator")