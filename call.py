from src.base import RequirementsGenerator


def main():
    # Load settings.json
    data = open("./src/settings.json", "r")
    settings = json.load(data)

    # Get OS name and User name
    os_name = platform.system()
    user_name = os.getlogin()

    # Set path
    base_path = settings["os"][os_name].replace("<user_name>", user_name)

    # Run
    example_dir = "Desktop/myapp"
    example_lang = "python"
    path = base_path + example_dir

    if os.path.exists(path):
        RequirementsGenerator(path, example_lang)
    else:
        print("Error: The selected directory does not exist.")

if __name__ == "__main__":
    main()