# "r" - Read - Default value. Opens a file for reading, error if the file does not exist
# "a" - Append - Opens a file for appending, creates the file if it does not exist
# "w" - Write - Opens a file for writing, creates the file if it does not exist
# "x" - Create - Creates the specified file, returns an error if the file exists
# "t" - Text - Default value. Text mode
# "b" - Binary - Binary mode (e.g. images)

#To open a file for reading it is enough to specify the name of the file:
f = open("demofile.txt")

#1 To open the file, use the built-in open() function.
# The open() function returns a file object, which has a read() method for reading the content of the file:
f = open("demofile.txt")
print(f.read())

#2 If the file is located in a different location, you will have to specify the file path, like this:
f = open("D:\\myfiles\welcome.txt")
print(f.read())

#3 Close the file when you are finished with it:
f = open("demofile.txt")
print(f.readline())
f.close()

#4 Return the 5 first characters of the file:
with open("demofile.txt") as f:
  print(f.read(5))

#5You can return one line by using the readline() method:
with open("demofile.txt") as f:
  print(f.readline())

#6 Loop through the file line by line:
with open("demofile.txt") as f:
  for x in f:
    print(x)