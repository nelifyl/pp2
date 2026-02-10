# 1 

def sum_all(*numbers):
    print(sum(numbers))

# 2 

def show_info(**data):
    print(data)

# 3

def greet_all(*names):
    for n in names:
        print("Hello", n)

# 4

def print_kwargs(**kwargs):
    for k, v in kwargs.items():
        print(k, v)

# 5

def mix(a, *args, **kwargs):
    print(a, args, kwargs)