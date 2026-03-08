#1 Remove the file "demofile.txt":
import os
os.remove("demofile.txt")

#2 Check if file exists, then delete it:
import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")

#3 Copy a file
import shutil
# Copy file from source to destination
shutil.copy("source.txt", "destination.txt")  
# Copies the file content and permissions

#4 Remove an empty directory
import os
os.rmdir("empty_folder")
# Removes an empty directory

#5 Safe delete with existence check
import os
file_path = "example.txt"
if os.path.exists(file_path):
    os.remove(file_path)
    print("File deleted")
else:
    print("File does not exist")