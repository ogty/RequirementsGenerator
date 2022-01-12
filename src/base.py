import inspect
import json
import os
import subprocess

import settings


class ModuleExtractor:
    """
    Supported Languages
    =====================
     - Python
     - Python(ipynb)
     - Julia
     - Julia(ipynb)
     - Go

    Note: Use common functions to handle everything except Go.
    """

    def python(self, source: str) -> list:
        result, embedded_modules = self.common(source)
        filtered_result = list(filter(lambda m: False if m in embedded_modules else m, result))
        return filtered_result
    
    def pythonipynb(self, ipynb_data: str) -> list:
        result, embedded_modules = self.common(ipynb_data, ipynb=True)
        filtered_result = list(filter(lambda m: False if m in embedded_modules else m, result))
        return filtered_result
    
    def julia(self, source: str) -> list:
        result, embedded_modules = self.common(source)
        replaced_result = list(map(lambda m: m.replace(":", "").replace(";", ""), result))
        filtered_result = list(filter(lambda m: False if m in embedded_modules else m, replaced_result))
        return filtered_result

    def juliaipynb(self, ipynb_data: str) -> list:
        result, embedded_modules = self.common(ipynb_data, ipynb=True)
        replaced_result = list(map(lambda m: m.replace(":", "").replace(";", ""), result))
        filtered_result = list(filter(lambda m: False if m in embedded_modules else m, replaced_result))
        return filtered_result

    def go(self, source: str) -> list:
        result = []
        embedded_modules: list = settings.CONFIG["languages"]["go"][2]
        splited_source = source.split()
        try:
            index_with_module_prefix = splited_source.index("import")
        except ValueError:
            return []

        # If you have multiple modules
        if splited_source[index_with_module_prefix + 1] == "(":
            module_count = index_with_module_prefix + 2
            while True:
                maybe_module = splited_source[module_count]
                if maybe_module == ")":
                    break

                result.append(maybe_module)
                module_count += 1
        # If you have only one module
        else:
            result.append(splited_source[index_with_module_prefix + 1])

        # Remove unwanted strings and exclude built-in modules
        filtered_result = list(map(lambda x: x.replace("\"", ""), result))
        filtered_result = list(filter(lambda x: False if x.split("/")[0] in embedded_modules else x, filtered_result))

        return filtered_result

    # Handle the parts common to python and julia
    def common(self, source: str, ipynb: bool=False) -> tuple:
        called_function_name = str(inspect.stack()[1].function)

        # If it's ipynb, process it like normal source code
        if ipynb:
            source_list = []
            ipynb_data: object = json.loads(source)
            for cell in ipynb_data["cells"]:
                source_list += cell["source"]
            source = "".join(source_list)

        # Because everything except ipynb is common
        language = "python" if "python" in called_function_name else "julia"
        prefixes: list = settings.CONFIG["languages"][language][1]
        embedded: list = settings.CONFIG["languages"][language][2]

        # Process it so that it can be executed by the eval method
        process = [f"x.startswith('{prefix}')" for prefix in prefixes]
        process_word = " or ".join(process)

        # Retrieve just the module from the line containing it
        splited_source = source.split("\n")
        line_with_module = [x for x in splited_source if eval(process_word)]
        modules = list(map(lambda m: m.split()[1], line_with_module))
        result = list(map(lambda m: m.split(".")[0] if not m.startswith(".") else "", modules))

        return (result, embedded)

    
# Get data in a hierarchical directory structure
class Operate:
    # Get all directories in the selected directory
    def get_directories(self, path: str) -> None:
        parent: list = os.listdir(path)
        directories = [f for f in parent if os.path.isdir(os.path.join(path, f))]

        # Get all hierarchical data by calling recursively
        for dir in directories:
            dir_full_path = os.path.join(path, dir)
            self.all_directory.append(dir_full_path)
            self.get_directories(dir_full_path)

    # Retrieves a specific file in the retrieved directory
    def get_files(self, selected_lang: str) -> None:
        if "ipynb" in selected_lang:
            ipynb_index = selected_lang.find("ipynb")
            selected_lang = f"{selected_lang[:ipynb_index]}-{selected_lang[ipynb_index:]}"

        # Selected supported language extension only
        for dir in self.all_directory:
            parent: list = os.listdir(dir)
            files = [f for f in parent if os.path.isfile(os.path.join(dir, f))]
            filtered_files_path = list(filter(lambda path: path.endswith(settings.CONFIG["languages"][selected_lang][0]), files))
            file_full_path = list(map(lambda path: os.path.join(dir, path), filtered_files_path))
            self.all_file += file_full_path

            
class RequirementsGenerator(Operate):
    # Initialize valiables and run function
    def __init__(self, path: str="", lang: str="", version: bool=False) -> None:
        self.path = path
        self.lang = lang
        self.version = version

        if version and lang == "python":
            self.pip_freezed = []
            stdout_result = subprocess.run(["pip3", "freeze"], capture_output=True)
            pip_freezed = stdout_result.stdout.decode("utf-8").split("\n")
            for installed_libary in pip_freezed:
                if "==" in installed_libary:
                    self.pip_freezed.append(installed_libary)

        self.all_file = []
        self.all_directory = [path]

    def confirm(self) -> list:
        # Get all file paths directly under the selected directory
        self.get_directories(self.path)
        self.get_files(self.lang)

        module_extractor = ModuleExtractor()
        module_list = []

        # Extract modules from the source code of all files obtained from the selected directory
        for file_path in self.all_file:
            with open(file_path, "r", encoding="utf-8") as file:
                file_contents = file.read()

            module_list += getattr(module_extractor, self.lang)(file_contents)
        
        if module_list:
            module_list = list(set(module_list))
            module_list.sort()

        if hasattr(self, "pip_freezed"):
            tmp_module_list = []
            matched_module_list = []
            for module in module_list:
                module = module.replace("_", "-")
                for installed_library in self.pip_freezed:
                    library_name = installed_library.split("==")[0]
                    if module == library_name.lower():
                        matched_module_list.append(module)
                        tmp_module_list.append(installed_library)
                    else:
                        tmp_module_list.append(module)
            
            tmp_module_list = list(set(tmp_module_list))
            module_list = tmp_module_list
            module_list.sort()

            for matched_module in matched_module_list:
                try:
                    module_list.remove(matched_module)
                except:
                    pass

        return module_list

    # Main process(generate requirements.txt)
    def generate(self, module_list: list) -> None:
        module_list = list(map(lambda x: x.replace("\n", ""), module_list))
        with open(os.path.join(self.path, "requirements.txt"), "w", encoding="utf-8") as f:
            modules = "\n".join(module_list)
            f.write(modules)

    # Get detailed information about a selected directory
    def detail(self, directories: list) -> dict:
        result = {}

        for dir in directories:
            supported_extension = {"py": 0, "jl": 0, "go": 0, "ipynb": 0, "other": 0}
            
            # Because an empty string will cause an error
            if self.all_directory.count(""):
                self.all_directory.remove("")

            # Get the hierarchical directory
            self.all_directory.append(dir)
            self.get_directories(dir)

            # Count supported language extensions
            for middle_dir in self.all_directory:
                parent: list = os.listdir(middle_dir)
                files = [f for f in parent if os.path.isfile(os.path.join(middle_dir, f))]

                for extension in supported_extension:
                    supported_extension[extension] += len(list(filter(lambda f: f.endswith(extension), files)))

            # Process it so that it is easy to handle in the next process
            extension_counted = [v for v in supported_extension.values()]
            sum_extension_counted = sum(extension_counted)

            # Process the data so that it can be displayed as a percentage
            if 0 < sum_extension_counted:
                supported_extension = {e: round((v / sum_extension_counted) * 100, 2) for e, v in zip(supported_extension, extension_counted)}
            else:
                supported_extension["other"] = 100

            display_dir_name = dir.split("/")[-1]
            result[display_dir_name] = supported_extension
            self.all_directory.clear()
        
        return result

    
# Generate the tree structure needed for directory selection
def generate_tree() -> None:
    # Store the retrieved information in a dict
    tree_data = {"data": []}

    for directory_stracture in os.walk(settings.DESKTOP_PATH):
        tree_information = {}

        dir_path = directory_stracture[0]
        if not list(filter(lambda x: True if x in dir_path else False, settings.IGNORE_DIRECTORIES)):
            dir_list = dir_path.split(settings.SPLIT_WORD)
            tree_information["id"] = dir_path                                    # full directory path
            tree_information["text"] = dir_list[-1]                              # displayed name
            tree_information["parent"] = settings.SPLIT_WORD.join(dir_list[:-1]) # directory parent

            # Since we are starting from Desktop, its parents are not there
            if settings.DESKTOP_PATH == dir_path:
                tree_information["parent"] = "#"

            tree_data["data"].append(tree_information)

    with open(settings.TREE_PATH, "w", encoding="utf-8") as f:
        json.dump(tree_data, f, ensure_ascii=False, indent=2)
