from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        pass
    else:
        return render_template("main.html")


if __name__ == "__main__":
    app.run(debug=True)