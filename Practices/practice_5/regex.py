#1

import re

pattern = r'ab*'

text = "abbb a ac abb"

matches = re.findall(pattern, text)
print(matches)

#2

import re

pattern = r'ab{2,3}'

text = "ab abb abbb abbbb"

matches = re.findall(pattern, text)
print(matches)


#3

import re

pattern = r'[a-z]+_[a-z]+'

text = "hello_world test_value Hello_World"

matches = re.findall(pattern, text)
print(matches)


#4

import re

pattern = r'[A-Z][a-z]+'

text = "Hello world My Name is Python"

matches = re.findall(pattern, text)
print(matches)


#5

import re

pattern = r'a.*b'

text = "acb axxxb a123b test"

matches = re.findall(pattern, text)
print(matches)


#6

import re

text = "Hello, world. Python is cool"

result = re.sub(r'[ ,.]', ':', text)
print(result)


#7

import re

def snake_to_camel(text):
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), text)

text = "hello_world_test"
print(snake_to_camel(text))


#8

import re

text = "HelloWorldTest"

result = re.findall(r'[A-Z][a-z]*', text)
print(result)


#9

import re

text = "HelloWorldTest"

result = re.sub(r'(?<!^)([A-Z])', r' \1', text)
print(result)


#10

import re

def camel_to_snake(text):
    return re.sub(r'([A-Z])', r'_\1', text).lower()

text = "helloWorldTest"
print(camel_to_snake(text))