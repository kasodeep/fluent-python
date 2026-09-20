from time import sleep, strftime
from concurrent import futures

def display(*args):
    print(strftime("[%H:%M:%S]"), end=" ")
    print(*args)

def loiter(n):
    msg = '{}loiter({}): doing nothing for {} seconds...'
    display(msg.format('\t' * n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t' * n, n))
    return n * 10

def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)
    results = executor.map(loiter, range(5))

    display('results:', results)
    display('Waiting for individual results:')

    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))
    display('Script ending.')

"""
The combination of executor.submit and futures.as_completed is more flexible than executor.map
because you can submit different callables and arguments, while executor.map is designed
to run the same callable on the different arguments. In addition, the set of futures you pass
to futures.as_completed may come from more than one executor—perhaps some were created by
a ThreadPoolExecutor instance, while others are from a ProcessPoolExecutor.
"""