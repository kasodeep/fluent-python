
for codec in ['latin_1', 'utf_8', 'utf_16']:
    print(codec, 'El Niño'.encode(codec), sep='\t')

# Coping with UnicodeEncodeError

city = 'São Paulo'
print(city.encode('utf-8'))
print(city.encode('utf-16'))
print(city.encode('iso-8859-1'))
print(city.encode('cp437'))

print(city.encode('cp437', errors='ignore'))
print(city.encode('cp437', errors='replace'))
print(city.encode('cp437', errors='xmlcharrefreplace'))

# Coping with UnicodeDecodeError
"""
Not every byte holds a valid ASCII character, and not every byte sequence is valid
UTF-8 or UTF-16; therefore, when you assume one of these encodings while convert‐
ing a binary sequence to text, you will get a UnicodeDecodeError if unexpected bytes
are found.
"""

octets = b'Montr\xe9al'
print(octets.decode('cp1252'))
print(octets.decode('koi8_r'))
print(octets.decode('utf-8'))

# add the string "# coding: cp1252" at the top of the file to avoid the UnicodeDecodeError when running this script.

"""
That is how the package “Chardet—The Universal Character Encoding Detector”
works to guess one of more than 30 supported encodings.
"""

# BOM: Byte Order Mark
"""
ff fe	U+FEFF in little-endian, so the stream is UTF-16LE; E-(45 00)
fe ff	U+FEFF in big-endian, so the stream is UTF-16BE; E-(00 45)
"""

'El Niño'.encode('utf-16le')  # b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00

"""
The Unicode standard says to assume big-endian.
In practice, x86 and Windows produce lots of little-endian UTF-16 with no BOM,
so that assumption often fails.
If you know the order, use utf_16le or utf_16be explicitly and skip the guesswork.
"""



