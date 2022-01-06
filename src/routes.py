import json
import os

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import render_template

from src.base import RequirementsGenerator, generate_tree
import settings

bp = Blueprint("routes", __name__, url_prefix="/")


# generate requirements.txt
@bp.route("/generate", methods=["POST"])
def generate() -> None:
    language = request.form["language"]
    selected_directories = request.form["dir_list"]
    directories = list(set(selected_directories.split(",")))

    # generate
    for dir in directories:
        RequirementsGenerator(dir, language).generate()

    return jsonify()

# update directory information
@bp.route("/update", methods=["POST"])
def update() -> None:
    generate_tree()
    return jsonify()

# get selected directory detail
@bp.route("/detail", methods=["POST"])
def detail() -> None:
    selected_directories = request.form["dir_list"]
    directories = list(set(selected_directories.split(",")))
    detail_data = RequirementsGenerator().detail(directories)
    return jsonify(values=json.dumps(detail_data))

# base
@bp.route("/")
def base() -> None:
    if not os.path.exists(settings.TREE_PATH):
        generate_tree()

    lang_data = {}
    for lang_name in settings.CONFIG["languages"]:
        if "-" in lang_name:
            lang_data[lang_name.capitalize()] = lang_name.replace("-", "")
        else:
            lang_data[lang_name.capitalize()] = lang_name

    return render_template("main.html", data=lang_data)
