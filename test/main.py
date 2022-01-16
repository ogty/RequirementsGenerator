import subprocess


def get_installed_libraries() -> list:
    stdout_result = subprocess.run(["pip3", "freeze"], capture_output=True)
    pip_freezed = stdout_result.stdout.decode("utf-8").split("\n")
    installed_libary_names = [library_data.split("==")[0] for library_data in pip_freezed]

    return installed_libary_names

def is_install(module: str) -> bool:
    installed_libraries = get_installed_libraries()
    if module in installed_libraries:
        return True
    else:
        return False
