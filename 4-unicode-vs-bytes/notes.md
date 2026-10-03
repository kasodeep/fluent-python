# Python `bytes` and `bytearray` (Fluent Python, Ch. 4)

## Core model
- `str` is a sequence of Unicode code points (text).
- `bytes` is an **immutable** sequence of ints in `range(256)`.
- `bytearray` is the **mutable** version of `bytes`.
- `bytes` carries no encoding information. An encoding converts `str` to `bytes` (`str.encode()`) and back (`bytes.decode()`).
- `'café'` is 4 characters but 5 bytes in UTF-8 (`é` is `c3 a9`).

## Indexing vs. slicing
- `b[0]` returns an **int** (`cafe[0]` is `99`).
- `b[:1]` returns a **bytes** of length 1 (`b'c'`).
- The same holds for `bytearray`.
- Rule: indexing returns the **element type**, slicing returns the **container type**.

| Container | `x[0]` | `x[:1]` |
|---|---|---|
| `[10, 20]` | `10` (int) | `[10]` (list) |
| `(10, 20)` | `10` (int) | `(10,)` (tuple) |
| `b'abc'` | `97` (int) | `b'a'` (bytes) |
| `'abc'` | `'a'` (str) | `'a'` (str) |

## Why `s[0] == s[:1]` holds only for `str`
- Python has no char type. A "character" is just a `str` of length 1.
- Element type and container type are both `str`, so index and slice agree.
- Holds only for non-empty strings: `''[0]` raises `IndexError`, while `''[:1]` returns `''`.
- Side effect: `'abc'[0][0][0]` still works.

## How `bytes` are displayed (repr)
| Byte value | Shown as |
|---|---|
| 32-126 | the ASCII character |
| tab, newline, CR, backslash | `\t`, `\n`, `\r`, `\\` |
| everything else | hex escape (`\xc3`) |

- If both `'` and `"` appear, the repr uses `'` as the delimiter and escapes inner `'`.
- The repr is only a display convenience. The data is ints.
- `bytearray` has no literal syntax and prints as `bytearray(b'...')`.

## Methods
- Most `str` methods work (`replace`, `strip`, `upper`, `endswith`, `translate`, ...), but **arguments must be `bytes`**.
- Not available: `format`, `format_map`, `casefold`, `isdecimal`, `isnumeric`, `isidentifier`, `isprintable`, `encode`. They need Unicode data or formatting machinery.
- `upper()` and similar methods affect only ASCII letters.
- `re` works on bytes if the **pattern is also bytes** (`rb'\d+'`).
- `%` formatting on bytes was restored in 3.5 (PEP 461).
- `bytes.fromhex('31 4B CE A9')` gives `b'1K\xce\xa9'`.

## Ways to construct
1. `str` + `encoding=`: `bytes('café', encoding='utf_8')`
2. An iterable of ints 0-255: `bytes([99, 97, 102])`
3. A buffer-protocol object (`bytes`, `bytearray`, `memoryview`, `array.array`)

## Copy vs. share
- Building from a buffer **copies** the bytes.
- `memoryview` **shares** memory without copying.

## Endianness
- `bytes(array.array('h', [-2, -1, 0, 1, 2]))` gives 10 bytes (5 × 16-bit).
- `-2` appears as `fe ff`, meaning little-endian on that machine.
- Raw byte layout depends on CPU byte order, which matters for files and networks.

## Correction to the book
- The book says `bytes(n)` was deprecated in 3.5 and removed in 3.6. I believe this is wrong, and `bytes(5)` still returns `b'\x00' * 5`.
- Verify by running `bytes(5)` in your interpreter.