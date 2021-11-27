import autopep8
from flask import Flask
from flask import render_template, request
import os
import platform

app = Flask(__name__)


language = {
    "python": "py",
    "julia": "jl",
}

# Module Extractor
class ModuleExtractor:
    def python(self, source) -> list:
        fixed_source = autopep8.fix_code(source)
        result = list()
        source_list = fixed_source.split("\n")
        for line in source_list:
            if line.startswith("import") or line.startswith("from"):
                module = line.split(" ")[1]
                if not module.startswith("."):
                    module = module.split(".")[0]
                    result.append(module)

        return result

    def julia(self, source) -> list:
        result = list()
        source_list = source.split("\n")
        for line in source_list:
            if line.startswith("using"):
                module = line.split(" ")[1]
                if not module.startswith("."):
                    module = module.split(".")[0]
                    module = module.replace(":", "").replace(";", "")
                    result.append(module)   

        return result             

class RequirementsGenerator:
    # initialize valiables and run function
    def __init__(self, dir_name: str, lang: str) -> None:
        self.all_dir: list = [dir_name]
        self.all_file = list()
        self.base_dir = dir_name
        self.lang = lang

        self.get_dirs(dir_name)
        self.get_files()
        self.main()

    # Of course I know that there is "os.walk". But...
    # Get all directories in the selected directory.
    def get_dirs(self, path) -> list:
        middle = list()
        base = os.listdir(path)
        files_dir = [f for f in base if os.path.isdir(os.path.join(path, f))]
        for dir in files_dir:
            self.all_dir.append(f"{path}/{dir}")
            middle += self.get_dirs(f"{path}/{dir}")

        return middle

    # Retrieves a specific file in the retrieved directory.
    def get_files(self) -> None:
        for dir in self.all_dir:
            base = os.listdir(dir)
            files = [f for f in base if os.path.isfile(os.path.join(dir, f))]
            files = list(filter(lambda f: f.endswith(language[self.lang]), files))
            files = list(map(lambda f: f"{dir}/{f}", files))
            self.all_file += files

    # Main process(generate)
    def main(self) -> None:
        # Module extract
        module_extractor = ModuleExtractor()
        module_list = list()
        for file_path in self.all_file:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            module_list += getattr(module_extractor, self.lang)(source)

        # Generate
        module_list = list(set(module_list))
        module_list.sort()
        with open(f"{self.base_dir}/requirements.txt", "w", encoding="utf-8") as f:
            data = "\n".join(module_list)
            f.write(data)

# Get all tree
def all_tree() -> list:
    user_name = os.getlogin()
    os_name = platform.system()

    if os_name == "Windows":
        path = f"C:\\Users\\{user_name}\\"
        result = os.walk(path)
    elif os_name == "Darwin":
        path = f"/Users/{user_name}/"
        result = os.walk(path)

    return result

@app.route("/", methods=["GET", "POST"])
def main():
    data = {
        "tree": list(),
        "error": "Error"
    }
    if request.method == "POST":
        base_dir = request.form["dirname"]
        language = request.form["language"]
        # RequirementsGenerator(base_dir, language)
        return render_template("main.html", data=data)
    else:
        result = all_tree()
        data["tree"] = result
        return render_template("main.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)


"""
・使われているファイルをディレクトリごとに割合表示とかしたい

"""