
import re

WORD_RE = re.compile(r'\w+')

index = {}
with open('zen.txt', encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start()+1
            location = (line_no, column_no)
            # this is ugly; coded like this to make a point
            
            occurrences = index.get(word, []) 
            # Get the list of occurrences for `word`, or [] if not found
            
            occurrences.append(location) 
            # Append new location to `occurrences`
            
            index[word] = occurrences 
            # Put changed `occurrences` into `index` dict; this entails a second search through the `index`
            
# print in alphabetical order
for word in sorted(index, key=str.upper):
    print(word, index[word])