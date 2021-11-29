<h1 align="center">Requirements.txt Generator</h1>

<div align="center">

 [![Download Now](https://img.shields.io/badge/-Download%20Now!-%2322A6F2)](https://github.com/ogty/RequirementsGenerator/releases/download/v1.0.1/ReqirementsGenerator.zip)
 ![release](https://img.shields.io/github/v/release/ogty/RequirementsGenerator?style=social)
 ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ogty/RequirementsGenerator?style=social)
 
</div>

## Demo

![demo](./static/demo.gif)

***

## Features

 - [x] Basic Features
 - [x] Can be built on Windows
 - [ ] Can be built on MacOS
 - [ ] Creation of original icons
 - [ ] Percentage display
 - [ ] Library selection
 - [ ] Execution by command
 - [ ] Display not only folders but also requirements.txt
 - [ ] Search function

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

***

## To add a language

Generate `requirements.txt`.
By default, it targets the folder directly under Desktop.
However, you can also set a directory other than Desktop as the current directory by changing the path of the OS that suits you in `settings.json`.

The language name has an array, where the first index contains the extension. The second index contains the description method to use when importing libraries.

```json
{
    "languages": {
        "python": [
            "py",
            ["import", "from"],
            ["os", "sys", "time"]
        ], 
        "julia": [
            "jl",
            ["using"],
            ["Base"]
        ]
    }, 
    "os": {
        "Windows": "C:\\Users\\<user_name>\\Desktop",
        "Darwin": "//Users//<user_name>//Desktop"
    }
}
```

Depending on the language, you may want to perform a specific process. The following are classes for Python and Julia library extraction, both of which perform a "common function".

But before calling it, each one performs its own processing; in Python, the linter cleans up the source code. In Julia, after calling the common function, we perform string operations on the result.

So it is easy to add a new language and implement your own processing.

The common function is probably supposed to be somewhat similar in all languages, so if it is different, you may want to change it.

```python
class ModuleExtractor:
    def python(self, source: str, lang: str) -> list:
        fixed_source = autopep8.fix_code(source)
        result = self.common(lang, fixed_source)
        return result

    def julia(self, source: str, lang: str) -> list:
        result = self.common(lang, source)
        result = map(lambda d: d.replace(":", "").replace(";", ""), result)
        return result

    def common(self, lang: str, source: str) -> list:
        result = list()
        prefix = settings["languages"][lang][1]
        embedded = settings["languages"][lang][2]

        if len(prefix) >= 2:
            process_list = map(lambda x: f"line.startswith('{x}')", prefix)
            process = " or ".join(process_list)
        elif len(prefix) == 1:
            process = "line.startswith('{prefix[0]}')"

        source_list = source.split("\n")
        for line in source_list:
            if eval(process):
                module = line.split(" ")[1]
                if not module.startswith("."):
                    module = module.split(".")[0]
                    result.append(module)

        map(lambda x: result.pop(x), embedded)
        return result
```
