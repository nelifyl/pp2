# Python has a set of built-in math functions, including an extensive math module, that allows you to perform mathematical tasks on numbers.

#1 The min() and max() functions can be used to find the lowest or highest value in an iterable:
x = min(5, 10, 25)
y = max(5, 10, 25)

print(x)
print(y)

#2 The abs() function returns the absolute (positive) value of the specified number:
x = abs(-7.25)

print(x)

#3 The pow(x, y) function returns the value of x to the power of y (xy).
#Return the value of 4 to the power of 3 (same as 4 * 4 * 4):
x = pow(4, 3)

print(x)

#Python has also a built-in module called math, which extends the list of mathematical functions.

# import math

#4 The math.sqrt() method for example, returns the square root of a number:
import math

x = math.sqrt(64)

print(x)

#5 The math.ceil() method rounds a number upwards to its nearest integer, and the math.floor() method rounds a number downwards to its nearest integer, and returns the result:
import math

x = math.ceil(1.4)
y = math.floor(1.4)

print(x) # returns 2
print(y) # returns 1