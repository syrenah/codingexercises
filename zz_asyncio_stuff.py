import asyncio
import inspect
import asyncio
import time
from functools import wraps
import asyncio
import time
from functools import wraps

def retry(attempts=3, delay=0.5, exceptions=(Exception,), backoff=1.0):
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                last_error = None
                current_delay = delay

                for attempt in range(1, attempts + 1):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as exc:
                        last_error = exc
                        print(f"{func.__name__} failed on attempt {attempt}/{attempts}: {exc}")
                        if attempt == attempts:
                            break
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff

                raise last_error
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                last_error = None
                current_delay = delay

                for attempt in range(1, attempts + 1):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as exc:
                        last_error = exc
                        print(f"{func.__name__} failed on attempt {attempt}/{attempts}: {exc}")
                        if attempt == attempts:
                            break
                        time.sleep(current_delay)
                        current_delay *= backoff

                raise last_error
            return sync_wrapper

    return decorator



def log_time(func):
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"{func.__name__} took {elapsed:.4f}s")
            return result
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"{func.__name__} took {elapsed:.4f}s")
            return result
        return sync_wrapper


def repeat(times):
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            async def async_wrapper(*args, **kwargs):
                for _ in range(times):
                    await func(*args, **kwargs)
            return async_wrapper
        else:
            def sync_wrapper(*args, **kwargs):
                for _ in range(times):
                    func(*args, **kwargs)
            return sync_wrapper
    return decorator
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator
@log_time
@retry(attempts=3, delay=0.2, exceptions=(ValueError,))
def do_work():
    print("doing work...")
    raise ValueError("temporary failure")

@log_time
@retry(attempts=4, delay=0.5, exceptions=(RuntimeError,))
async def fetch_data():
    print("fetching...")
    raise RuntimeError("network glitch")
def repeat_async(times):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for _ in range(times):
                await func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(7)
def non_async_demo():
    print("non async")

@repeat_async(7)
async def printing_stuff():
    await asyncio.sleep(2)
    print("Hello, World!")

async def main():
    await printing_stuff()
    non_async_demo()

if __name__ == "__main__":
    asyncio.run(main())