"""
A decorator is a callable that takes another function as an argument (the decorated function).
A decorator may perform some processing with the decorated function, and returns
it or replaces it with another function or callable object.
"""

"""
A key feature of decorators is that they run right after the decorated function is
defined. That is usually at import time.
"""

registry = []

def register(func):
    print(f"running register({func})")
    registry.append(func)
    return func

@register
def f1():
    print("running f1()")

@register
def f2():
    print("running f2()")

def main():
    print("running main()")
    print("registry ->", registry)
    f1()
    f2()

if __name__ == "__main__":
    main()

"""
Function decorators are executed as soon as the module is imported,
but the decorated functions only run when they are explicitly invoked.
"""
