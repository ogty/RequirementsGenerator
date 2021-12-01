<h1 align="center">Requirements.txt Generator</h1>

<div align="center">

 [![Download Now](https://img.shields.io/badge/-Download%20Now!-%2322A6F2)](https://github.com/ogty/RequirementsGenerator/releases/download/v1.0.1/ReqirementsGenerator.zip)
 ![release](https://img.shields.io/github/v/release/ogty/RequirementsGenerator?style=social)
 ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ogty/RequirementsGenerator?style=social)
 
</div>

![demo](./static/sample.gif)

***

## Features

 - [x] Basic Features
 - [x] Can be built on Windows
 - [ ] Can be built on MacOS
 - [ ] Creation of original icons
 - [x] Percentage display
 - [ ] Library selection
 - [ ] Execution by command
 - [ ] Display not only folders but also requirements.txt
 - [x] Search function

***

## Supported languages

 - Python
 - Julia
 - Go

***

## Install the library and build the app

To build the application and install the required libraries, run the following command. The generated file will be in "exe" format and will work only on Windows. It will take a few minutes to complete execution.

 - `>` : Windows
 - `$` : Mac

```console
> pip install -r requirements.txt
> pyinstaller -w -F --add-data "templates;templates" --add-data "static;static" --add-data "src;src" main.py
```

```bash
$ pip3 install -r requirements.txt
$ pyinstaller -w -F main.py
```

However, it is easier to run "install.bat".

```console
> install.bat
```

```bash
$ source install.sh
```

The built executable will be generated directly under dist.

I don't know, I haven't tried it yet, but you may be able to use the application by downloading this repository and running the exe file...

Note: This RequirementsGenerator is based on the assumption that users will write some clean code.
