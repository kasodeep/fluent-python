"""
Concurrency is essential for efficient network I/O: instead of idly waiting for remote
machines, the application should do something else until a response comes back.

1.  Regardless of the concurrency constructs you use—threads or coroutines—you will
see vastly improved throughput over sequential code in network I/O operations,
if you code it properly.

2. For HTTP clients that can control how many requests they make, there is no 
significant difference in performance between threads and coroutines.

Python’s standard library provides the urllib.request module, but its API is
synchronous only, and is not user friendly.
"""

import time
from pathlib import Path
from typing import Callable

import httpx

POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()

BASE_URL = 'https://www.fluentpython.com/data/flags'
DEST_DIR = Path(__file__).parent / 'downloads'

def save_flag(img: bytes, filename: str) -> None:
    """Save a flag image to the 'downloads' directory."""
    dest = DEST_DIR / filename
    dest.write_bytes(img)
    print(f'Written to {dest}')

def get_flag(cc: str) -> bytes:
    """Return the content of a flag image as bytes."""
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=6.1, follow_redirects=True)

    resp.raise_for_status()
    return resp.content

def download_many(cc_list: list[str]) -> int:
    """Download a list of flag images."""
    for cc in sorted(cc_list):
        image = get_flag(cc)
        save_flag(image, f'{cc}.gif')
        print(cc, end=' ', flush=True)
    return len(cc_list)

def main(downloader: Callable[[list[str]], int]) -> None:
    """Download flags of the 20 most populous countries."""
    DEST_DIR.mkdir(exist_ok=True)
    t0 = time.perf_counter()
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} flags downloaded in {elapsed:.2f}s')

if __name__ == '__main__':
    main(download_many)