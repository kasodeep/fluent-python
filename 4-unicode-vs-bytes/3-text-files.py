open('file.txt', 'w', encoding='utf-8').write('El Niño')
print(open('file.txt', encoding='utf-8').read())
# bug, not providing decoding will use the default encoding, which is platform dependent.
# On Windows, it is cp1252, on Linux and macOS, it is utf-8.

"""
Code that has to run on multiple machines or on multiple occa‐
sions should never depend on encoding defaults. Always pass an
explicit encoding= argument when opening text files, because the
default may change from one machine to the next, or from one day
to the next.
"""

# Ordinary code should never use 'rb' or 'wb' modes for text files.
# These modes are for binary files, and using them for text files can lead to unexpected behavior,
# especially with character encoding. Always use 'r' or 'w' modes for reading and writing text files,
# and specify the encoding explicitly to avoid issues with different platforms and locales.