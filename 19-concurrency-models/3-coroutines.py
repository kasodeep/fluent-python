'''
In contrast, coroutines are driven by an application-level event loop that manages a
queue of pending coroutines, drives them one by one, monitors events triggered by
I/O operations initiated by coroutines, and passes control back to the corresponding
coroutine when each event happens.

asyncio.run(coro()):
Called from a regular function to drive a coroutine object that usually is the entry
point for all the asynchronous code in the program, like the supervisor in this
example. This call blocks until the body of coro returns. The return value of the
run() call is whatever the body of coro returns.

asyncio.create_task(coro()):
Called from a coroutine to schedule another coroutine to execute eventually.
This call does not suspend the current coroutine. It returns a Task instance, an
object that wraps the coroutine object and provides methods to control and
query its state.

await coro():
Called from a coroutine to transfer control to the coroutine object returned by
coro(). This suspends the current coroutine until the body of coro returns. The
value of the await expression is whatever the body of coro returns.
'''

import asyncio
import itertools

async def spin(msg: str) -> None:
    # This is a COROUTINE, not a thread. It only runs when the event
    # loop explicitly gives it a turn -- there's no OS-level pre-emption.
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')

        try:
            # await hands control back to the event loop for 0.1s.
            # This is the ONLY way this coroutine yields control.
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            # Raised when supervisor() calls spinner.cancel()
            break

    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

async def slow() -> int:
    # Placeholder for heavy work. await asyncio.sleep(3) yields control,
    # so the event loop is free to run spin() while this "waits."
    #
    # THE TRAP: if you replace this body with a plain synchronous
    # is_prime(n) call, there is NO await inside it. So once this
    # coroutine starts running, it monopolizes the single thread until
    # it returns. spin() never gets scheduled -- not even once. The
    # program just looks frozen for ~3s.
    await asyncio.sleep(3)
    return 42

def main() -> None:
    # asyncio.run() is the entry point: creates the event loop, runs
    # supervisor() to completion, and closes the loop. Blocks until done.
    result = asyncio.run(supervisor())
    print(f'Answer: {result}')

async def supervisor() -> int:
    # create_task() SCHEDULES spin() to run but does NOT block/suspend
    # this coroutine -- supervisor() moves on to the next line immediately.
    spinner = asyncio.create_task(spin('thinking!'))
    print(f'spinner object: {spinner}')

    # await suspends supervisor() here and hands control to the event
    # loop, which is what actually lets spinner's task run at all.
    result = await slow()

    spinner.cancel()  # stop the spinner once slow() is done
    return result

if __name__ == '__main__':
    main()