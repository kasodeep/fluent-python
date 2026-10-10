"""
Actually, a closure is a function—let’s call it f—with an extended scope that encompasses
variables referenced in the body of f that are not global variables or local variables of f.
"""

class Averager():
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total / len(self.series)

def make_averager():
    """
    Note that series is a local variable of make_averager because the assignment series
    = [] happens in the body of that function. But when avg(10) is called,
    make_averager has already returned, and its local scope is long gone.
    """
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return averager

"""
But with immutable types like numbers, strings, tuples, etc., all you can do is read,
never update. If you try to rebind them, as in count = count + 1, then you are
implicitly creating a local variable count. It is no longer a free variable, and therefore
it is not saved in the closure.
"""
def make_averager_local():
    count = 0
    total = 0

    def averager(new_value):
        count += 1
        total += new_value
        return total / count

    return averager

"""
It lets you declare a variable as a free variable even when it is assigned within the function.
If a new value is assigned to a nonlocal variable, the binding stored in the closure is changed.
"""
def make_averager_nonlocal():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count

    return averager