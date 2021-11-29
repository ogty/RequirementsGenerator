import autopep8
import json
import os


# Module Extractor
class ModuleExtractor:
    def python(self, source: str, lang: str) -> list:
        fixed_source = autopep8.fix_code(source)
        result = self.common(lang, fixed_source)
        return result

    def julia(self, source: str, lang: str) -> list:
        result = self.common(lang, source)
        result = map(lambda d: d.replace(":", "").replace(";", ""), result)
        return result

    def go(self, source: str, lang: str) -> list:
        # This language requires a lot of processing.
        result = self.common(lang, source)
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

        # Remove embedded libraries
        map(lambda x: result.pop(x), embedded)
        return result

class RequirementsGenerator(ModuleExtractor):
    # initialize valiables and run function
    def __init__(self, path: str, lang: str) -> None:
        self.path = path
        self.all_dir: list = [path]
        self.all_file = list()
        self.lang = lang

        # run
        self.get_dirs(path)
        self.get_files()
        self.main()

    # Get all directories in the selected directory.
    def get_dirs(self, path: str) -> None:
        base = os.listdir(path)
        files_dir = [f for f in base if os.path.isdir(os.path.join(path, f))]

        for dir in files_dir:
            self.all_dir.append(f"{path}/{dir}")
            self.get_dirs(f"{path}/{dir}")

    # Retrieves a specific file in the retrieved directory.
    def get_files(self) -> None:
        for dir in self.all_dir:
            base = os.listdir(dir)
            files = [f for f in base if os.path.isfile(os.path.join(dir, f))]                      # get only files
            files = list(filter(lambda f: f.endswith(settings["languages"][self.lang][0]), files)) # extension
            files = list(map(lambda f: f"{dir}/{f}", files))                                       # create absolute path
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
        with open(f"{self.path}/requirements.txt", "w", encoding="utf-8") as f:
            data = "\n".join(module_list)
            f.write(data)

data = open(f"{os.getcwd()}\\src\\settings.json", "r")
settings = json.load(data)
