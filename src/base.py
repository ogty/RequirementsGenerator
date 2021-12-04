import inspect
import json
import os
import platform


# Sorry: many SPLIT_WORD and many f-string
# list(), dict() -> [], {} Because it's faster

class LibraryExtractor:
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
        result, embedded_libraries = self.common(source)
        filtered_result = list(filter(lambda m: False if m in embedded_libraries else m, result))
        return filtered_result
    
    def pythonipynb(self, ipynb_data: str) -> list:
        result, embedded_libraries = self.common(ipynb_data, ipynb=True)
        filtered_result = list(filter(lambda m: False if m in embedded_libraries else m, result))
        return filtered_result
    
    def julia(self, source: str) -> list:
        result, embedded_libraries = self.common(source)
        replaced_result = list(map(lambda m: m.replace(":", "").replace(";", ""), result))
        filtered_result = list(filter(lambda m: False if m in embedded_libraries else m, replaced_result))
        return filtered_result

    def juliaipynb(self, ipynb_data: str) -> list:
        result, embedded_libraries = self.common(ipynb_data, ipynb=True)
        replaced_result = list(map(lambda m: m.replace(":", "").replace(";", ""), result))
        filtered_result = list(filter(lambda m: False if m in embedded_libraries else m, replaced_result))
        return filtered_result

    def go(self, source: str) -> list:
        result = []
        embedded_libraries: list = SETTINGS["languages"]["go"][2]
        splited_source = source.split()
        library_prefix_index = splited_source.index("import")

        # If you have multiple libraries
        if splited_source[library_prefix_index+1] == "(":
            library_count = library_prefix_index+2
            while True:
                maybe_library = splited_source[library_count]
                if maybe_library == ")":
                    break

                result.append(maybe_library)
                library_count += 1
        # If you have only one library
        else:
            result.append(splited_source[library_prefix_index+1])

        # Remove unwanted strings and exclude built-in libraries
        filtered_result = list(map(lambda x: x.replace("\"", ""), result))
        filtered_result = list(filter(lambda x: False if x.split("/")[0] in embedded_libraries else x, filtered_result))

        return filtered_result

    # Handle the parts common to python and julia
    def common(self, source: str, ipynb=False) -> tuple:
        called_function_name = str(inspect.stack()[1].function)

        # If it's ipynb, process it like normal source code
        if ipynb:
            ipynb_data: object = json.loads(source)
            source_list = [cell["source"] for cell in ipynb_data["cells"]]
            source = "".join(source_list)

        # Because everything except ipynb is common
        language = "python" if "python" in called_function_name else "julia"
        prefixes: list = SETTINGS["languages"][language][1]
        embedded: list = SETTINGS["languages"][language][2]

        # Process it so that it can be executed by the eval method
        process = [f"x.startswith('{pref}')" for pref in prefixes]
        process_word = " or ".join(process)

        # Retrieve just the library from the line containing it
        splited_source = source.split("\n")
        library_line = [x for x in splited_source if eval(process_word)]
        libraries = list(map(lambda m: m.split()[1], library_line))
        result = list(map(lambda m: m.split(".")[0] if not m.startswith(".") else "", libraries))

        return (result, embedded)

# Get data in a hierarchical directory structure
class Operate:
    # Get all directories in the selected directory
    def get_directories(self, path: str) -> None:
        parent: list = os.listdir(path)
        directories = [f for f in parent if os.path.isdir(os.path.join(path, f))]

        # Get all hierarchical data by calling recursively
        for dir in directories:
            dir_full_path = path + SPLIT_WORD + dir
            self.all_directory.append(dir_full_path)
            self.get_directories(dir_full_path)

    # Retrieves a specific file in the retrieved directory
    def get_files(self, selected_lang: str) -> None:
        if "ipynb" in selected_lang:
            index = selected_lang.find("ipynb")
            selected_lang = f"{selected_lang[:index]}-{selected_lang[index:]}"

        # selected supported language extension only
        for dir in self.all_directory:
            parent: list = os.listdir(dir)
            files = [f for f in parent if os.path.isfile(os.path.join(dir, f))]
            filtered_files_path = list(filter(lambda path: path.endswith(SETTINGS["languages"][selected_lang][0]), files))
            file_full_path = list(map(lambda path: dir + SPLIT_WORD + path, filtered_files_path))
            self.all_file += file_full_path

class RequirementsGenerator(Operate):
    # initialize valiables and run function
    def __init__(self, path="", lang="") -> None:
        self.path = path
        self.lang = lang
        self.all_file = []
        self.all_directory = [path]

    # Main process(generate requirements.txt)
    def generate(self) -> None:
        self.get_directories(self.path)
        self.get_files(self.lang)

        # Library extract
        library_extractor = LibraryExtractor()
        library_list = []

        # Extract libraries from the source code of all files obtained from the selected directory
        for file_path in self.all_file:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            library_list += getattr(library_extractor, self.lang)(source)

        # if library_list is not empty
        if library_list:
            library_list = list(set(library_list))
            library_list.sort()

            with open(f"{self.path}{SPLIT_WORD}requirements.txt", "w", encoding="utf-8") as f:
                labraries = "\n".join(library_list)
                f.write(labraries)

    # Get detailed information about a selected directory
    def detail(self, directories: list) -> dict:
        result = {}

        for dir in directories:
            supported_extension = {
                "py"   : 0, 
                "jl"   : 0, 
                "go"   : 0,
                "ipynb": 0, 
                "other": 0
            }
            
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
            if sum_extension_counted > 0:
                supported_extension = {e: round((v/sum_extension_counted)*100, 2) for e, v in zip(supported_extension, extension_counted)}
            else:
                supported_extension["other"] = 100

            display_dir_name = dir.split(SPLIT_WORD)[-1]
            result[display_dir_name] = supported_extension
            self.all_directory.clear()
        
        return result

# Generate the tree structure needed for directory selection
def generate_tree():
    # Get all directory information directly under the default path written in settings.json
    os_name = platform.system()
    user_name = os.getlogin()
    path = SETTINGS["os"][os_name].replace("<user_name>", user_name)

    # Store the retrieved information in a dict
    tree_data = {"data": []}
    for directory_stracture in os.walk(path):
        tree_information = {}

        dir_path = directory_stracture[0]
        if not ".git" in dir_path:                                      # .git is ignore
            dir_list = dir_path.split(SPLIT_WORD)
            tree_information["id"] = dir_path                           # full directory path
            tree_information["text"] = dir_list[-1]                     # displayed name
            tree_information["parent"] = SPLIT_WORD.join(dir_list[:-1]) # directory parent

            # Since we are starting from Desktop, its parents are not there
            if path == dir_path:
                tree_information["parent"] = "#"

            tree_data["data"].append(tree_information)

    with open(f"{os.getcwd()}{SPLIT_WORD}static{SPLIT_WORD}tree.json", "w", encoding="utf-8") as f:
        json.dump(tree_data, f, ensure_ascii=False, indent=2)

SPLIT_WORD = "\\" if platform.system() == "Windows" else "/"
data = open(f"{os.getcwd()}{SPLIT_WORD}static{SPLIT_WORD}settings.json", "r")
SETTINGS = json.load(data)