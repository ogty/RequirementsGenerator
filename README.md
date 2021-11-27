# Requirements.txt Generator

Generate `requirements.txt`.
By default, it targets the folder directly under Desktop.
However, you can also set a directory other than Desktop as the current directory by changing the path of the OS that suits you in `settings.json`.

The language name has an array, where the first index contains the extension. The second index contains the description method to use when importing libraries.

```json
{
    "languages": {
        "python": [
            "py",
            ["import", "from"]
        ], 
        "julia": [
            "jl",
            ["using"]
        ]
    }, 
    "os": {
        "Windows": "C:\\Users\\<user_name>\\Desktop",
        "Darwin": "/Users/<user_name>/Desktop"
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
        prefix = settings["languages"][lang][1]
        fixed_source = autopep8.fix_code(source)
        result = self.common(fixed_source, prefix)
        return result

    def julia(self, source: str, lang: str) -> list:
        prefix = settings["languages"][lang][1]
        result = self.common(source, prefix)
        result = map(lambda d: d.replace(":", "").replace(";", ""), result)
        return result

    def common(self, source: str, prefix: list) -> list:
        result = list()
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

        return result
```