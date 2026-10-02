import re
import sys

WORD_RE = re.compile(r'\w+')

index = {}

with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index.setdefault(word, []).append(location)

for word in sorted(index, key=str.upper):
    print(word, index[word])

import collections # using defaultdict to simplify the code above

index = collections.defaultdict(list)

with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index[word].append(location)

for word in sorted(index, key=str.upper):
    print(word, index[word])

"""
For example, if dd is a defaultdict, and k is a missing key,
dd[k] will call the default_factory to create a default value, but
dd.get(k) still returns None, and k in dd is False.
"""

# __missing__() is called by dict.__getitem__() when a key is not found;
# It can be overridden in a subclass to customize behavior for missing keys.