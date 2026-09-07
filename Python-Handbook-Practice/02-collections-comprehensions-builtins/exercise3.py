# Count words case-insensitively and return the three most common words.
# [('python', 8), ('is', 2), ('learn', 2)]

import re
from collections import defaultdict

text = """
Python is powerful and python is easy to learn.
PYTHON makes coding fun. Python, python, PYTHON!
Learn python programming with python examples.
"""

word_freq = defaultdict(int)

for word in re.findall(r'\w+', text.lower()):
    word_freq[word] += 1

print(word_freq)