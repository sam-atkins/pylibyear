import tomllib

with open("pyproject.toml", "rb") as file:
    pyproject = tomllib.load(file)

version = pyproject["project"]["version"]

with open("libyear/__about__.py", "w") as file:
    file.write(f'__version__ = "{version}"\n')

print(f"Version bumped to {version} in libyear/__about__.py.")
