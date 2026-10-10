b=6

def f1(a):
    print(a)
    print(b)
    b=9

f1(5) # UnboundLocalError: local variable 'b' referenced before assignment

"""
But the fact is, when Python compiles the body of the function, it decides that b is a
local variable because it is assigned within the function.
"""

def f3(a):
    global b
    print(a)
    print(b)
    b=9

f3(5) # 5 6
print(b) # 9
