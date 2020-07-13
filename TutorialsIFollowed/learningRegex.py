import re

textToMatch = '''abcdefghijklmnopqrstuvwxyz
                 ABCDEFGHIJKLMNOPQRSTUVWXYZ
                 012-3806188 012-6089168
                 5 minutes 5 hours 10 hours 10 days
                 20-5-2020
                 This is a ... This is a magnanimous man
                 abc is like 123
                 Mr. Gram-Schmidt'''
pattern = re.compile(r'\d\d\d-\d\d\d\d\d\d\d')
match = pattern.finditer(textToMatch)
for match in match:
    print(match)
