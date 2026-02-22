import sys
import tomllib

if len(sys.argv) > 1:
    new_version = sys.argv[1]
    with open("pyproject.toml", "rb") as file:
        content = file.read()

    pyproject = tomllib.loads(content.decode())
    old_version = pyproject["project"]["version"]

    text = content.decode().replace(
        f'version = "{old_version}"', f'version = "{new_version}"', 1
    )
    with open("pyproject.toml", "w") as file:
        file.write(text)

    version = new_version
    print(f"Version set to {version} in pyproject.toml.")
else:
    with open("pyproject.toml", "rb") as file:
        pyproject = tomllib.load(file)
    version = pyproject["project"]["version"]

with open("libyear/__about__.py", "w") as file:
    file.write(f'__version__ = "{version}"\n')

print(f"Version bumped to {version} in libyear/__about__.py.")
