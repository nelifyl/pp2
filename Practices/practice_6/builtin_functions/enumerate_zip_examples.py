# 1. enumerate() — basic usage
fruits = ["apple", "banana", "cherry"]

for index, fruit in enumerate(fruits):
    print("1.", index, fruit)


# 2. enumerate() — starting index from 1
for index, fruit in enumerate(fruits, start=1):
    print("2.", index, fruit)


# 3. zip() — combine two lists
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

for name, score in zip(names, scores):
    print("3.", name, score)


# 4. zip() — convert zipped result to list
zipped_list = list(zip(names, scores))
print("4. Zipped list:", zipped_list)


# 5. zip() + enumerate() — indexed pairing
for index, (name, score) in enumerate(zip(names, scores), start=1):
    print("5.", index, name, score)