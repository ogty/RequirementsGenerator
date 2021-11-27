from flask import Flask
from flask import render_template, request

from src.base import RequirementsGenerator

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main():
    data = {}
    if request.method == "POST":
        language = request.form["language"]
        dir_name = request.form["dir_name"]
        RequirementsGenerator(dir_name, language)
        return render_template("main.html", data=data)
    else:
        return render_template("main.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)