import os
import shutil
from pathlib import Path


# 1. Move a file to another folder (basic usage)
shutil.move("source.txt", "destination_folder/source.txt")
print("1. File moved to destination_folder")


# 2. Rename a file while moving
shutil.move("old_name.txt", "destination_folder/new_name.txt")
print("2. File moved and renamed")


# 3. Move using pathlib
source = Path("example.txt")
destination = Path("destination_folder") / "example.txt"

if source.exists():
    shutil.move(str(source), str(destination))
    print("3. File moved using pathlib")


# 4. Move all .txt files from one folder to another
source_folder = "source_folder"
destination_folder = "destination_folder"

for filename in os.listdir(source_folder):
    if filename.endswith(".txt"):
        shutil.move(
            os.path.join(source_folder, filename),
            os.path.join(destination_folder, filename)
        )

print("4. All .txt files moved")


# 5. Safe move with existence check
file_path = "important.txt"
target_path = "backup/important.txt"

if os.path.exists(file_path):
    shutil.move(file_path, target_path)
    print("5. Important file moved safely")
else:
    print("5. File does not exist")