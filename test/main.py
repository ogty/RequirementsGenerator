import subprocess


def get_installed_libraries() -> list:
    stdout_result = subprocess.run(["pip3", "freeze"], capture_output=True)
    pip_freezed = stdout_result.stdout.decode("utf-8").split("\n")
    
    installed_libary_names = []
    for installed_libary_and_version in pip_freezed:
        installed_libary_names.append(installed_libary_and_version.split("==")[0])

    return installed_libary_names

def is_install(module: str) -> bool:
    installed_libraries = get_installed_libraries()
    if module in installed_libraries:
        return True
    else:
        return False

if __name__ == "__main__":
    print(is_install("python-dotenv"))
    print(is_install("dotenv"))
