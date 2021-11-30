import autopep8
import json
import os
import platform


# Module Extractor
class ModuleExtractor:
    def python(self, source: str, lang: str) -> list:
        embedded: list = settings["languages"][lang][2]
        fixed_source = autopep8.fix_code(source)
        splited_source = fixed_source.split()

        modules = [splited_source[i+1] for i, x in enumerate(splited_source) if x == "from" or x == "import"]
        result = list(filter(lambda m: m.split(".")[0] if not m.startswith(".") else "", modules))
        result = list(map(lambda x: "" if x in embedded else x, result))

        return result
    
    def julia(self, source: str, lang: str) -> list:
        embedded: list = settings["languages"][lang][2]
        splited_source = source.split()

        modules = [splited_source[i+1] for i, x in enumerate(splited_source) if x == "using" or x == "import"]
        result = list(filter(lambda m: m.split(".")[0] if not m.startswith(".") else "", modules))
        result = list(map(lambda m: m.replace(":", "").replace(";", ""), result))
        result = list(map(lambda x: "" if x in embedded else x, result))

        return result

    def go(self, source: str, lang: str) -> list:
        result = list()
        embedded = settings["languages"][lang][2]

        splited_source = source.split()
        start = splited_source.index("import")

        if splited_source[start + 1] == "(":
            count = start + 2
            while True:
                module = splited_source[count]
                if module == ")":
                    break
                result.append(module)
                count += 1
        else:
            result.append(splited_source[start + 1])

        result = list(map(lambda x: x.replace("\"", ""), result))
        result = list(map(lambda x: "" if x.split("/")[0] in embedded else x, result))

        return result

class RequirementsGenerator:
    # initialize valiables and run function
    def __init__(self, path: str, lang: str) -> None:
        self.path = path
        self.lang = lang
        self.all_file = list()
        self.all_dir: list = [path]
        os_name = platform.system()
        self.split_word = settings["os"][os_name][1]

        self.get_dirs(self.path)
        self.get_files()
        self.main()

    # Get all directories in the selected directory.
    def get_dirs(self, path: str) -> None:
        base = os.listdir(path)
        files_dir = [f for f in base if os.path.isdir(os.path.join(path, f))]

        for dir in files_dir:
            self.all_dir.append(f"{path}{self.split_word}{dir}")
            self.get_dirs(f"{path}{self.split_word}{dir}")

    # Retrieves a specific file in the retrieved directory.
    def get_files(self) -> None:
        for dir in self.all_dir:
            base = os.listdir(dir)
            files = [f for f in base if os.path.isfile(os.path.join(dir, f))]
            files = list(filter(lambda f: f.endswith(settings["languages"][self.lang][0]), files))
            files = list(map(lambda f: f"{dir}{self.split_word}{f}", files))

            self.all_file += files

    # Main process(generate)
    def main(self) -> None:
        # Module extract
        module_extractor = ModuleExtractor()
        module_list = list()

        for file_path in self.all_file:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            module_list += getattr(module_extractor, self.lang)(source, self.lang)

        # Generate
        module_list = list(set(module_list))
        module_list.sort()

        # If an error occurs, generate a file with the string from
        with open(f"{self.path}/requirements.txt", "w", encoding="utf-8") as f:
            try:
                data = "\n".join(module_list)
                f.write(data)
            except TypeError:
                f.write("")


def generate_tree():
    # Get all directory information directly under the default path written in settings.json
    os_name = platform.system()
    user_name = os.getlogin()
    path = settings["os"][os_name][0].replace("<user_name>", user_name)
    
    # Store the retrieved information in a dict
    main_data = {"data": list()}
    for data in os.walk(path):
        base_dict = {
            "id": "",
            "parent": "",
            "text": ""
            }
        
        if os_name == "Windows":
            dir_constract = data[0]
            dir_list = dir_constract.split("\\")
            parent = "\\".join(dir_list[:-1])

        elif os_name == "Darwin":
            dir_constract = data[0].replace("/", "//")
            dir_list = dir_constract.split("//")
            parent = "//".join(dir_list[:-1])
            
        child = dir_list[-1]

        base_dict["id"] = dir_constract
        base_dict["text"] = child
        base_dict["parent"] = parent

        if path == data[0]:
            base_dict["parent"] = "#"

        main_data["data"].append(base_dict)

    with open(f"{os.getcwd()}\\static\\tree.json", "w", encoding="utf-8") as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)

def get_detail(dirs: list):
    pass

data = open(f"{os.getcwd()}\\src\\settings.json", "r")
settings = json.load(data)