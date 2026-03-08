#1 Open the file "demofile.txt" and append content to the file:
with open("demofile.txt", "a") as f:
  f.write("Now the file has more content!")

#open and read the file after the appending:
with open("demofile.txt") as f:
  print(f.read())

#2 Open the file "demofile.txt" and overwrite the content:
with open("demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")

#open and read the file after the overwriting:
with open("demofile.txt") as f:
  print(f.read())

#3 Writing text to a file (overwrite mode)
with open("example1.txt", "w", encoding="utf-8") as file:
    file.write("Hello, world!\n")  # Write a line to the file
    file.write("This is the first file write.")  # Write another line

#4 Appending text to a file
with open("example1.txt", "a", encoding="utf-8") as file:
    file.write("\nThis line was appended.")  # Add text to the end of the file

#5 Writing multiple lines using writelines()
lines = [
    "First line\n",
    "Second line\n",
    "Third line\n"
]

with open("example2.txt", "w", encoding="utf-8") as file:
    file.writelines(lines)  # Write a list of strings to the file