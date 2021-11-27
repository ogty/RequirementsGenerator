from flask import Flask
from flask import render_template, request, jsonify
import json

from src.base import RequirementsGenerator

app = Flask(__name__)


@app.route("/generate", methods=["POST"])
def generate():
    language = request.form["language"]
    dir_name = request.form["dir_name"]
    # RequirementsGenerator(dir_name, language)

    return_json = {
        "message": f"{language}, {dir_name}"
    }
    return jsonify(values=json.dumps(return_json))

@app.route("/")
def base():
    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True)