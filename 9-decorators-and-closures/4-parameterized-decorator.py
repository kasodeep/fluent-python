registry = set()  # a set of registered functions

def register(active=True):
    """Register a function if active is True."""
    def decorate(func):
        print(f"running register(active={active}) -> decorate({func})")
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate

@register(active=False)
def f1():
    print(f"running f1()")

@register()  # active=True by default
def f2():
    print(f"running f2()")