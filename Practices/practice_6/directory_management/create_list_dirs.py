import os
from pathlib import Path


# 1. Create a single directory
os.mkdir("new_folder")
print("1. Directory 'new_folder' created")


# 2. Create nested directories
os.makedirs("parent_folder/child_folder", exist_ok=True)
print("2. Nested directories created")


# 3. Create directory using pathlib
path = Path("pathlib_folder")
path.mkdir(exist_ok=True)
print("3. Directory created using pathlib")


# 4. List directories in current folder
print("4. Directories in current folder:")
for item in os.listdir("."):
    if os.path.isdir(item):
        print(" -", item)


# 5. List directories using pathlib
print("5. Directories using pathlib:")
for item in Path(".").iterdir():
    if item.is_dir():
        print(" -", item.name)