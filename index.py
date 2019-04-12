"""Build an index mapping word -> list of occurrences"""

import re

WORD_RE = re.compile(r'\w+')

index = {}
with open('zen.txt', encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start()+1
            location = (line_no, column_no)
            index.setdefault(word, []).append(location)
            # Get the list of occurrences for word, or set it to [] if not found; setdefault returns the value, 
            # so it can be updated without requiring a second search.
            
# print in alphabetical order
for word in sorted(index, key=str.upper):
    print(word, index[word])