<h1 align="center">requirements.txt Generator</h1>

<div align="center">
 
![release](https://img.shields.io/github/v/release/ogty/requirements.txt-generator?style=social)&nbsp;![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ogty/requirements.txt-generator?style=social)
 
</div>

![demo](static/images/demo.gif)

***

## Features

 - [x] Windows, Mac, and Linux compatible
 - [x] Select Language
 - [x] Search Folders
 - [x] Detail View
 - [x] Select Package
 - [x] Select Multiple Folders
 - [x] Add Version

***

## Supported languages

 - Python
 - Python(ipynb)
 - Julia
 - Julia(ipynb)
 - Go

***

## How to install packages in each language using requirements.txt

**Python**

```
$ pip install -r requirements.txt
```

**Julia**

```julia
# install.jl
using Pkg; Pkg.add(open(f -> readlines(f), "./requirements.txt"))
```

```
$ julia install.jl
```

***

## Tip

For Python and Julia, you can check the version checkbox to verify that the generated `requirements.txt` can successfully install the package.
For example, if you install `python-dotenv` in Python, the call to `python-dotenv` will be `dotenv`, 
which means you cannot install `python-dotenv`(because the name of the package is different when it is installed). 
So, by checking the version checkbox, we indicate that if the version is not marked, 
the package cannot be installed correctly.

---

## Note

 - If you have a large number of folders on your `Desktop`, it may not work properly.  
 - If you download it, there is a good chance it won't work. If you want to use it, please clone it.
 - It is assumed that you have a Python and Julia runtime environment built.

**Packaging**

```
$ pyinstaller --add-data "src;src" --add-data "static;static" --add-data "templates;templates" --noconsole app.py
```
