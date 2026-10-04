import sys
import unicodedata

START, END = ord(' '), sys.maxunicode + 1

def find(*query_words, start=START, end=END):
    """Find Unicode characters whose names contain all of the query words."""

    query_words = {word.upper() for word in query_words}
    for codepoint in range(start, end):
        char = chr(codepoint)
        name = unicodedata.name(char, None)
        if name and query_words.issubset(name.split()):
            print(f'U+{codepoint:04X}\t{char}\t{name}')

def main(words):
    if not words:
        print('Usage: python unicode_database.py <word1> <word2> ...')
        return
    find(*words)

if __name__ == '__main__':
    main(sys.argv[1:])