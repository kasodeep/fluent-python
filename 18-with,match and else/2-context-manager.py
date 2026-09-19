"""
@contextmanager: yield splits the generator into two halves.
- Code BEFORE yield  -> runs on __enter__ (the "setup")
- Code AFTER  yield  -> runs on __exit__  (the "teardown")
- The yielded VALUE   -> becomes the `as` target

Effectively: @contextmanager wraps your generator function in a class
that implements __enter__/__exit__ for you.

__enter__:
    1. calls the generator function -> gen
    2. next(gen)            -> runs setup, pauses at yield
    3. returns yielded value -> bound to `as` target

__exit__:
    - if an exception occurred in the with-block:
        gen.throw(exc) -> re-raised INSIDE the generator, at the yield line
    - else:
        next(gen)       -> resumes after yield (teardown runs)
"""

import contextlib
import sys


# --- BROKEN version: no exception handling around yield -------------------
@contextlib.contextmanager
def looking_glass_broken():
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    yield 'JABBERWOCKY'
    sys.stdout.write = original_write   # <-- never runs if block raises!

"""
FLAW: if the with-block raises, Python re-raises it at the `yield` line
inside the generator. There's no try/except there, so the function just
dies -- `sys.stdout.write` is NEVER restored. sys.stdout is left broken
for the rest of the program.
"""


# --- FIXED version: wrap yield in try/except/finally -----------------------
@contextlib.contextmanager
def looking_glass():
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write   # ALWAYS restored, no matter what
    if msg:
        print(msg)

"""
- finally guarantees restoration even on exception, early return, etc.
- except ZeroDivisionError here means: this exception is considered
  "handled" -> IT WILL BE SUPPRESSED, not propagated to the caller.

Inversion of default __exit__ behavior:
- Normal class-based __exit__: return truthy  -> suppress exception
                                return falsy/None -> propagate exception
- @contextmanager's auto-generated __exit__ flips this:
  if YOUR generator catches the exception (and doesn't re-raise it),
  that's treated as "handled" -> suppressed.
  If you don't catch it, it propagates normally.
  So exception-handling logic lives in try/except around yield,
  not in a return value.
"""


# --- Bonus: contextmanager objects can double as decorators -----------------
@looking_glass()
def verse():
    print('Alice, Kitty and Snowdrop')

"""
This works because @contextmanager builds on contextlib.ContextDecorator:
any context manager it produces can ALSO be used as a function decorator.
Using it this way runs the whole function body as if wrapped in
`with looking_glass(): ...` on every call to verse() --
setup before the call, teardown after -- without needing a `with` block
at every call site.
"""