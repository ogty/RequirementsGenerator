import subprocess


stdout_result = subprocess.run(["julia", "./src/package_status.jl"], capture_output=True)
installed_packages = stdout_result.stdout.decode("utf-8").split("\n")

installed_packages = list(map(lambda x: x.lstrip("  "), installed_packages))
installed_packages.remove("")

result = ["@".join(package_info.split(" ")[1:]) for package_info in installed_packages[1:]]
print(result)
