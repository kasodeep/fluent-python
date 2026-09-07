'''
Concurrency is about dealing with lots of things at once.
Parallelism is about doing lots of things at once.

Concurrency:
The ability to handle multiple pending tasks, making progress one at a time or in
parallel (if possible) so that each of them eventually succeeds or fails. A single-
core CPU is capable of concurrency if it runs an OS scheduler that interleaves the
execution of the pending tasks. Also known as multitasking.

Parallelism:
The ability to execute multiple computations at the same time. This requires a
multicore CPU, multiple CPUs, a GPU, or multiple computers in a cluster.

Execution unit:
General term for objects that execute code concurrently, each with independent
state and call stack. Python natively supports three kinds of execution units: processes, 
threads, and coroutines.

Lock
An object that execution units can use to synchronize their actions and avoid
corrupting data. While updating a shared data structure, the running code
should hold an associated lock.

Contention
Dispute over a limited asset. Resource contention happens when multiple execu‐
tion units try to access a shared resource—such as a lock or storage. There’s also
CPU contention, when compute-intensive processes or threads must wait for the
OS scheduler to give them a share of the CPU time.
'''

'''
1. Each instance of the Python interpreter is a process. You can start additional
Python processes using the multiprocessing.

2. The Python interpreter uses a single thread to run the users program and the
memory garbage collector.

3. Access to object reference counts and other internal interpreter state is controlled by a lock,
the Global Interpreter Lock (GIL).

4. Every Python standard library function that makes a syscall5 releases the GIL.

5. To run CPU-intensive Python code on multiple cores, you must use multiple Python processes.

Summary:
If you want your application to make better use of the computational resources of multicore 
machines, you are advised to use multiprocessing or concurrent.futures.ProcessPoolExecutor.
However, threading is still an appropriate model if you want to run multiple I/O-bound tasks
simultaneously.
'''

'''
The first important insight of this example is that time.sleep()
blocks the calling thread but releases the GIL, allowing other
Python threads to run.
'''

import itertools
import time
from threading import Thread, Event

def spin(msg: str, done: Event) -> None:
    # Runs in a SEPARATE THREAD. Prints one animation frame every 0.1s.
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)

        # done.wait(0.1) blocks for up to 0.1s, but crucially it RELEASES
        # the GIL while waiting -- this is what lets the main thread run.
        if done.wait(0.1):
            break  # done.set() was called elsewhere -> stop spinning

    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')  # erase the spinner line

def slow() -> int:
    # The "heavy work" placeholder. time.sleep() also releases the GIL,
    # which is WHY the spinner thread gets a chance to run at all here.
    # If you replace this with is_prime(n), the GIL is still forcibly
    # taken away from this thread every 5ms by CPython -- so the spinner
    # STILL keeps spinning, just with slightly more overhead/contention.
    time.sleep(3)
    return 44

def supervisor() -> int:
    done = Event()  # shared flag: tells the spinner thread when to stop
    spinner = Thread(target=spin, args=('thinking!', done))

    print(f'spinner object: {spinner}')
    spinner.start()      # spinner thread starts running concurrently

    result = slow()       # main thread does the "real work"
    done.set()             # signal spinner to stop
    spinner.join()          # wait for spinner thread to actually finish
    return result

def main() -> None:
    result = supervisor()
    print(f'Answer: {result}')

if __name__ == '__main__':
    main()