from unicodedata import normalize, name

"""
THEORY
------
Problem: the same visible text can have different code point sequences.
  'é' = U+00E9 (composed)  OR  'e' + U+0301 (decomposed)
Unicode calls these "canonical equivalents" and says apps should treat them as
the same, but Python compares code points, so == gives False.
Fix: normalize both sides to one form before comparing.

Two independent switches give four forms:

  Form  | compat. chars decomposed | recomposed | lossy
  ------+--------------------------+------------+------
  NFD   | no                       | no         | no
  NFC   | no                       | yes        | no
  NFKD  | yes                      | no         | yes
  NFKC  | yes                      | yes        | yes

- NFC: shortest equivalent string (composes). Default for storage/interchange.
- NFD: expands into base char + combining marks. Handy for stripping accents.
- K forms (compatibility): also replace "similar" characters with a preferred
  representation (ligatures, superscripts, fractions, fullwidth forms).
  Formatting is supposed to be external markup, not part of Unicode, so
  info is lost ('4²' -> '42'). Use for search/indexing, NOT permanent storage.
- Compatibility character: added to Unicode only for round-trip conversion
  with legacy encodings. Example: micro sign U+00B5 exists for latin1 even
  though Greek mu U+03BC is the "real" letter.
- Normalization works on code points (decode bytes first). It does not do
  case-insensitivity (use casefold() after) and does not merge cross-script
  lookalikes (Cyrillic 'а' vs Latin 'a').
"""

# --- Canonical equivalence: NFC / NFD ---
s1 = 'café'
s2 = 'cafe\N{COMBINING ACUTE ACCENT}'
print(s1 == s2)                                    # False (different code points)
print(len(s1), len(s2))                            # 4 5
print(normalize('NFC', s1) == normalize('NFC', s2))  # True
print(normalize('NFD', s1) == normalize('NFD', s2))  # True

# --- Compatibility equivalence: NFKC / NFKD (lossy) ---
half = '\N{VULGAR FRACTION ONE HALF}'
print(normalize('NFKC', half))                     # 1⁄2 (FRACTION SLASH, not '/')
print([name(c) for c in normalize('NFKC', half)])  # DIGIT ONE, FRACTION SLASH, DIGIT TWO
print('1/2' in normalize('NFKC', half))            # False: ASCII '/' won't match

print(normalize('NFKC', '4²'))                     # 42 (meaning changed!)

# --- Micro sign vs. ohm sign ---
# Micro is a *compatibility* char; ohm is a *canonical* singleton, so NFC
# rewrites ohm but leaves micro alone. NFKC/NFKD change both.
micro = 'µ'                                        # U+00B5
ohm = '\N{OHM SIGN}'                               # U+2126

print(normalize('NFC', micro) == micro)            # True: NFC leaves micro alone
print(normalize('NFKC', micro) == 'μ')             # True: NFKC -> Greek mu U+03BC
print(ord(micro), ord(normalize('NFKC', micro)))   # 181 956

print(normalize('NFC', ohm) == 'Ω')                # True: NFC changes ohm -> Greek capital omega
print(normalize('NFKC', ohm) == 'Ω')               # True