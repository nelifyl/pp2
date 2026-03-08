from functools import reduce

#1 map() — square each number
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print("Squared numbers:", squared)


#2 map() — convert strings to uppercase
words = ["python", "java", "c++"]
upper_words = list(map(str.upper, words))
print("Uppercase words:", upper_words)


#3 filter() — keep only even numbers
numbers = [1, 2, 3, 4, 5, 6]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even_numbers)


#4 filter() — keep words longer than 4 characters
words = ["cat", "elephant", "dog", "giraffe"]
long_words = list(filter(lambda word: len(word) > 4, words))
print("Long words:", long_words)


#5 reduce() — calculate the product of all numbers
numbers = [1, 2, 3, 4]
product = reduce(lambda x, y: x * y, numbers)
print("Product of numbers:", product)