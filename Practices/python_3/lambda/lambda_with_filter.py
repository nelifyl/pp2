nums = [1, 2, 3, 4, 5, 6]

# 1
print(list(filter(lambda x: x % 2 == 0, nums)))

# 2
print(list(filter(lambda x: x > 3, nums)))

# 3
print(list(filter(lambda x: x < 5, nums)))

# 4
print(list(filter(lambda x: x != 2, nums)))

# 5
print(list(filter(lambda x: x % 3 == 0, nums)))