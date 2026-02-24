pairs = [(1, 3), (2, 1), (4, 2)]

# 1
print(sorted(pairs, key=lambda x: x[0]))

# 2
print(sorted(pairs, key=lambda x: x[1]))

# 3 строки по длине
words = ["hi", "hello", "a"]
print(sorted(words, key=lambda x: len(x)))

# 4 обратная сортировка
print(sorted(nums := [3, 1, 2], key=lambda x: x, reverse=True))

# 5
students = [{"age": 20}, {"age": 18}, {"age": 22}]
print(sorted(students, key=lambda s: s["age"]))