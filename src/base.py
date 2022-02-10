import inspect
import json
import os
import subprocess
from typing import List, Dict, Tuple, Set

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
    """

    def python(self, source: str) -> Set[str]:
        result, embedded_modules = self.common(source)
        filtered_result = set(filter(lambda m: False if m in embedded_modules else m, result))
        return filtered_result
    
    def pythonipynb(self, ipynb_data: str) -> Set[str]:
        result, embedded_modules = self.common(ipynb_data, ipynb=True)
        filtered_result = set(filter(lambda m: False if m in embedded_modules else m, result))
        return filtered_result
    
    def julia(self, source: str) -> Set[str]:
        result, embedded_modules = self.common(source)
        replaced_result = list(map(lambda m: m.replace(":", "").replace(";", ""), result))
        filtered_result = set(filter(lambda m: False if m in embedded_modules else m, replaced_result))
        return filtered_result

    def juliaipynb(self, ipynb_data: str) -> Set[str]:
        result, embedded_modules = self.common(ipynb_data, ipynb=True)
        replaced_result = list(map(lambda m: m.replace(":", "").replace(";", ""), result))
        filtered_result = set(filter(lambda m: False if m in embedded_modules else m, replaced_result))
        return filtered_result

    def go(self, source: str) -> Set[str]:
        result = []
        embedded_modules: list = settings.CONFIG["languages"]["go"][2]
        splited_source = source.split()
        try:
            index_with_module_prefix = splited_source.index("import")
        except ValueError:
            return set()

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
        filtered_result = set(filter(lambda x: False if x.split("/")[0] in embedded_modules else x, filtered_result))

        return filtered_result

    # Handle the parts common to python and julia
    def common(self, source: str, ipynb: bool = False) -> Tuple[Set[str], List[str]]:
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
        result = set(map(lambda m: m.split(".")[0] if not m.startswith(".") else "", modules))

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
    def __init__(self, path: str = None, lang: str = None, version: bool = False) -> None:
        self.path = "" if path is None else path
        self.lang = "" if lang is None else lang 
        self.all_file = []
        self.all_directory = [path]

        # If a version is specified, get the information of the installed module
        if version:
            if "python" in self.lang:
                stdout_result_splited = self.command_runner(["pip3", "freeze"])

                self.installed_modules = [x for x in stdout_result_splited if "==" in x]
                self.version_split_word = "=="
                self.module_match_process_word = "module.replace('_', '-') == module_name.lower()"

            elif "julia" in self.lang:
                stdout_result_splited = self.command_runner(["julia", "-e", "using Pkg; Pkg.status()"])
                installed_packages = list(map(lambda x: x.lstrip("  "), stdout_result_splited))
                installed_packages.remove("")

                self.installed_modules = ["@".join(package_info.split(" ")[1:]) for package_info in installed_packages[1:]]
                self.version_split_word = "@"
                self.module_match_process_word = "module == module_name"
                
    def command_runner(self, command: List[str]) -> List[str]:
        stdout_result = subprocess.run(command, capture_output=True)
        stdout_result_splited = stdout_result.stdout.decode("utf-8").split("\n")
        return stdout_result_splited
    
    def confirm(self) -> List[str]:
        # Get all file paths directly under the selected directory
        self.get_directories(self.path)
        self.get_files(self.lang)

        module_extractor = ModuleExtractor()
        modules_for_return = set()

        # Extract modules from the source code of all files obtained from the selected directory
        for file_path in self.all_file:
            with open(file_path, "r", encoding="utf-8") as file:
                file_contents = file.read()

            modules_for_return = modules_for_return.union(getattr(module_extractor, self.lang)(file_contents))

        if hasattr(self, "installed_modules"):
            tmp_modules = set()
            matched_modules = set()

            for module in modules_for_return:
                for installed_module in self.installed_modules:
                    module_name = installed_module.split(self.version_split_word)[0] # Note: Used in eval

                    if eval(self.module_match_process_word):
                        matched_modules.add(module)
                        tmp_modules.add(installed_module)
                    else:
                        tmp_modules.add(module)

            module_list = list(tmp_modules)
            for matched_module in matched_modules:
                try:
                    module_list.remove(matched_module)
                except ValueError as ex:
                    print(f"Error: {ex}")
        else:
            module_list = list(modules_for_return)

        module_list.sort()
        return module_list

    # Main process(generate requirements.txt)
    def generate(self, module_list: List[str]) -> None:
        module_list = list(map(lambda x: x.replace("\n", ""), module_list))
        with open(os.path.join(self.path, "requirements.txt"), "w", encoding="utf-8") as f:
            modules = "\n".join(module_list)
            f.write(modules)

    # Get detailed information about a selected directory
    def detail(self, directories: List[str]) -> Dict[str, Dict[str, int]]:
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
                try:
                    files = [f for f in parent if os.path.isfile(os.path.join(middle_dir, f))]
                    for extension in supported_extension:
                        supported_extension[extension] += len(list(filter(lambda f: f.endswith(extension), files)))
                except TypeError as ex:
                    print(f"Error: {ex}")

            # Process it so that it is easy to handle in the next process
            extension_counted = [v for v in supported_extension.values()]
            sum_extension_counted = sum(extension_counted)

            # Process the data so that it can be displayed as a percentage
            if 0 < sum_extension_counted:
                supported_extension = {k: round((v / sum_extension_counted) * 100, 2) for k, v in zip(supported_extension, extension_counted)}
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
            dir_list = dir_path.split(settings.PATH_SPLIT_WORD)
            tree_information["id"] = dir_path                                         # Full directory path
            tree_information["text"] = dir_list[-1]                                   # Displayed name
            tree_information["parent"] = settings.PATH_SPLIT_WORD.join(dir_list[:-1]) # Directory parent

            # Since you are starting from Desktop, its parents are not there
            if settings.DESKTOP_PATH == dir_path:
                tree_information["parent"] = "#"

            tree_data["data"].append(tree_information)

    with open(settings.TREE_PATH, "w", encoding="utf-8") as f:
        json.dump(tree_data, f, ensure_ascii=False, indent=2)
