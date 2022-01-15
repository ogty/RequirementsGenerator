<h1 align="center">requirements.txt Generator</h1>

<div align="center">

[![Download for Windows](static/images/download_for_windows.png)](https://github.com/ogty/RequirementsGenerator/releases/download/v1.0.0/requirementstxt_generator_for_windows.zip)&nbsp;&nbsp;&nbsp;[![Download for Mac](static/images/download_for_mac.png)](https://github.com/ogty/RequirementsGenerator/releases/download/v1.0.0/requirementstxt_generator_for_mac.zip)&nbsp;&nbsp;&nbsp;[![Download for Linux](static/images/download_for_linux.png)](https://github.com/ogty/RequirementsGenerator)

![release](https://img.shields.io/github/v/release/ogty/RequirementsGenerator?style=social)&nbsp;![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ogty/RequirementsGenerator?style=social)
 
</div>

![demo](static/images/demo.gif)

***

## Features

 - [x] Windows, Mac, and Linux compatible
 - [x] Select Language
 - [x] Search Folders
 - [x] Detail view
 - [x] Select library
 - [x] Select multiple folders
 - [x] Add version
 - [ ] Execute command

***

## Supported languages

 - Python
 - Python-ipynb
 - Julia
 - Julia-ipynb
 - Go

***

## How to install packages for each language

**Python**

```
$ pip install -r requirements.txt
```

**Julia**

```julia
# install.jl
using Pkg; Pkg.add(open(f->readlines(f), "./requirements.txt"))
```

```
$ julia install.jl
```
***

## Note

If you have a large number of folders on your desktop, it may not work properly.
