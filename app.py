from flask import Flask
from pyfladesk import init_gui

from src import routes


app = Flask(__name__)
app.register_blueprint(routes.bp)


if __name__ == "__main__":
    init_gui(app, window_title="Requirements.txt Generator")
