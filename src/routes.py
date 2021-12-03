from flask import Blueprint
from flask import jsonify, request, render_template
import os
import json
import platform

from src.base import RequirementsGenerator, generate_tree

bp = Blueprint("routes", __name__, url_prefix="/")


# generate requirements.txt(main)
@bp.route("/generate", methods=["POST"])
def generate():
    language = request.form["language"]
    selected_dirs = request.form["dir_list"]
    dirs = list(set(selected_dirs.split(",")))
    [RequirementsGenerator(dir, language).generate() for dir in dirs]

    return jsonify()

# update directory information
@bp.route("/update", methods=["POST"])
def update():
    generate_tree()
    return jsonify()

# get selected directory detail
@bp.route("/detail", methods=["POST"])
def detail():
    selected_dirs = request.form["dir_list"]
    dirs = list(set(selected_dirs.split(",")))
    detail_data = RequirementsGenerator().detail(dirs)
    return jsonify(values=json.dumps(detail_data))

# base
@bp.route("/")
def base():
    if not os.path.exists(f"{os.getcwd()}{split_word}static{split_word}tree.json"):
        generate_tree()

    lang_data = {}
    for lang_name in settings["languages"]:
        if "-" in lang_name:
            lang_data[lang_name.capitalize()] = lang_name.replace("-", "")
        else:
            lang_data[lang_name.capitalize()] = lang_name

    return render_template("main.html", data=lang_data)

# Frequently referenced data
split_word = "\\" if platform.system() == "Windows" else "/"
data = open(f"{os.getcwd()}{split_word}static{split_word}settings.json", "r")
settings = json.load(data)