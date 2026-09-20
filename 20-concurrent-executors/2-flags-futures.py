import time
from pathlib import Path
from typing import List
from concurrent import futures

from flagsseq import get_flag, save_flag, main

def download_one(cc: str):
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

def download_many(cc_list: List[str]) -> int:

    """
    the executor.__exit__ method will call executor.shutdown(wait=True),
    which will block until all threads are done.
    """
    with futures.ThreadPoolExecutor() as executor:
        res = executor.map(download_one, sorted(cc_list)) # max_workers = min(32, os.cpu_count() + 4)
    return len(list(res))

if __name__ == '__main__':
    main(download_many)

"""
An instance of either Future class represents a deferred computation that may or may not have completed.
"""

def download_many(cc_list: list[str]) -> int:
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do: list[futures.Future] = []

        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do.append(future)
            print(f'Scheduled for {cc}: {future}')
        
        for count, future in enumerate(futures.as_completed(to_do), 1):
            res: str = future.result()
            print(f'{future} result: {res!r}')
    return count