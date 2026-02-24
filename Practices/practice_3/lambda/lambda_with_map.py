nums = [1, 2, 3, 4]

# 1
print(list(map(lambda x: x * 2, nums)))

# 2
print(list(map(lambda x: x ** 2, nums)))

# 3
print(list(map(str, nums)))

# 4
print(list(map(lambda x: x + 10, nums)))

# 5
print(list(map(lambda x: x % 2 == 0, nums)))