import itertools
import operator

def vowel(c):
    return c.lower() in 'aeiou'

list(filter(vowel, 'Deep'))
list(itertools.dropwhile(vowel, 'Naman'))
list(itertools.takewhile(vowel, 'Deep'))

sample = [5, 4, 7, 2, 6]
list(itertools.accumulate(sample, max))
list(itertools.accumulate(sample, operator.mul))

list(enumerate('albatroz', 1))
list(map(lambda a, b: (a, b), range(11), [2, 4, 8]))

def tree(cls, level):
    yield cls.__name__, level
    for sub_cls in cls.__subclasses__():
        yield from tree(sub_cls, level + 1)

def display(cls):
    for class_name, level in tree(cls, 0):
        indent = ' ' * 4 * level
        print(f'{indent}{class_name}')

if __name__ == '__main__':
    display(BaseException)