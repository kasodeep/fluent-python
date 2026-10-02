"""
Context manager objects exist to control a with statement, just like iterators exist to
control a for statement.

The context manager interface consists of the __enter__ and __exit__ methods. At
the top of the with, Python calls the __enter__ method of the context manager
object. When the with block completes or terminates for any reason, Python calls
__exit__ on the context manager object.
"""

import sys

with open("myfile.txt") as f:
    for line in f:
        print(line, end="")

print(f.closed, f.encoding)  # True
print(type(f))  # <class '_io.TextIOWrapper'>

f = open('file.txt')
hasattr(f, '__enter__')   # True
hasattr(f, '__exit__')    # True

class LookingGlass:
    def __enter__(self):
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JABBERWOCKY'

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print("Please DO NOT divide by zero!")
            return True  # Suppress the exception
        print("Leaving the LookingGlass")

with LookingGlass() as what:
    print(what)  # YKCOWREBBAJ
    print('Alice, Kitty and Snowdrop')  # pordwonS dna yttiK ,ecilA

print("Back to normal")  # Back to normal