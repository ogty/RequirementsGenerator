from flask import Blueprint
from flask import jsonify, request, render_template
import os
import json
import platform

from src.base import SPLIT_WORD, RequirementsGenerator, generate_tree

bp = Blueprint("routes", __name__, url_prefix="/")


# generate requirements.txt
@bp.route("/generate", methods=["POST"])
def generate():
    language = request.form["language"]
    selected_directories = request.form["dir_list"]
    directories = list(set(selected_directories.split(",")))

    # generate
    for dir in directories:
        RequirementsGenerator(dir, language).generate()

    return jsonify()

# update directory information
@bp.route("/update", methods=["POST"])
def update():
    generate_tree()
    return jsonify()

# get selected directory detail
@bp.route("/detail", methods=["POST"])
def detail():
    selected_directories = request.form["dir_list"]
    directories = list(set(selected_directories.split(",")))
    detail_data = RequirementsGenerator().detail(directories)
    return jsonify(values=json.dumps(detail_data))

# base
@bp.route("/")
def base():
    if not os.path.exists(f"{os.getcwd()}{SPLIT_WORD}static{SPLIT_WORD}tree.json"):
        generate_tree()

    lang_data = {}
    for lang_name in SETTINGS["languages"]:
        if "-" in lang_name:
            lang_data[lang_name.capitalize()] = lang_name.replace("-", "")
        else:
            lang_data[lang_name.capitalize()] = lang_name

    return render_template("main.html", data=lang_data)

SPLIT_WORD = "\\" if platform.system() == "Windows" else "/"
data = open(f"{os.getcwd()}{SPLIT_WORD}static{SPLIT_WORD}settings.json", "r")
SETTINGS = json.load(data)