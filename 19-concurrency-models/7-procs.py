"""
procs.py: a "homegrown" process pool for checking primes,
using multiprocessing.Process and SimpleQueue with poison pills
to shut workers down.
"""
import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count
from multiprocessing import queues

from common.primes import is_prime, NUMBERS

# NOTE:
# - Poison pill is `0`. Unsafe as a sentinel in general — it only works
#   here because `NUMBERS` never contains 0. A real job queue should use
#   `None`/`Ellipsis` (Ellipsis survives pickling with identity intact).
# - Speedup only shows up with real cores + real per-task cost; on a
#   constrained/limited-core box, process-spawn overhead can make this
#   slower than sequential.py.


class PrimeResult(NamedTuple):
    n: int
    prime: bool
    elapsed: float


JobQueue = queues.SimpleQueue
ResultQueue = queues.SimpleQueue


def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)


def worker(jobs: JobQueue, results: ResultQueue) -> None:
    while n := jobs.get():
        results.put(check(n))
    results.put(PrimeResult(0, False, 0.0))  # poison pill received, signal done


def start_jobs(
    procs: int, jobs: JobQueue, results: ResultQueue
) -> None:
    for n in NUMBERS:
        jobs.put(n)
    for _ in range(procs):
        proc = Process(target=worker, args=(jobs, results))
        proc.start()
        jobs.put(0)  # poison pill, one per worker


def report(procs: int, results: ResultQueue) -> int:
    checked = 0
    procs_done = 0
    while procs_done < procs:
        n, prime, elapsed = results.get()
        if n == 0:
            procs_done += 1
        else:
            checked += 1
            label = 'P' if prime else ' '
            print(f'{n:16}  {label} {elapsed:9.6f}s')
    return checked


def main() -> None:
    if len(sys.argv) < 2:
        procs = cpu_count()
    else:
        procs = int(sys.argv[1])

    print(f'Checking {len(NUMBERS)} numbers with {procs} processes:')
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue()
    results: ResultQueue = SimpleQueue()
    start_jobs(procs, jobs, results)
    checked = report(procs, results)
    elapsed = perf_counter() - t0
    print(f'{checked} checks in {elapsed:.2f}s')


if __name__ == '__main__':
    main()