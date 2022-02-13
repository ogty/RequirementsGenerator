import ast
from distutils.util import strtobool
import json
import os

from flask import (
    Blueprint, 
    jsonify, 
    request, 
    render_template
)

import settings
from src.base import (
    RequirementsGenerator, 
    generate_tree
)


bp = Blueprint("routes", __name__, url_prefix="/")

# Confirm modules
@bp.route("/confirm", methods=["POST"])
def confirm() -> None:
    language = request.form["language"]
    selected_directories = request.form["dir_list"]
    version = request.form["version"]
    directories = list(set(selected_directories.split(",")))

    if directories.count(""):
        directories.remove("")

    directory_and_module = {}
    for dir in directories:
        module_list = RequirementsGenerator(dir, language, version=strtobool(version)).confirm()
        directory_and_module[dir] = module_list

    return jsonify(values=json.dumps(directory_and_module))

# Generate requirements.txt
@bp.route("/generate", methods=["POST"])
def generate() -> None:
    language = request.form["language"]
    data: str = request.form["confirmed_data"]
    data: dict = ast.literal_eval(data)

    for dir, module_list in data.items():
        RequirementsGenerator(dir, language).generate(module_list)

    return jsonify()

# Update directory information
@bp.route("/update", methods=["POST"])
def update() -> None:
    generate_tree()
    return jsonify()

# Get selected directory detail
@bp.route("/detail", methods=["POST"])
def detail() -> None:
    selected_directories = request.form["dir_list"]
    directories = list(set(selected_directories.split(",")))
    detail_data = RequirementsGenerator().detail(directories)
    return jsonify(values=json.dumps(detail_data))

@bp.route("/")
def base() -> None:
    if not os.path.exists(settings.TREE_PATH):
        generate_tree()

    lang_data = {}
    for lang_name in settings.CONFIG["languages"]:
        lang_data[lang_name.capitalize()] = lang_name.replace("-", "") if "-" in lang_name else lang_name

    return render_template("main.html", data=lang_data)
