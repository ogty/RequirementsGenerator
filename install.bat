@echo off
pip install -r requirements.txt && ^
pyinstaller -w -F --add-data "templates;templates" --add-data "static;static" --add-data "src;src" main.py