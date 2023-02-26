import functools
import time


results_list = list()
app_run_time = list()


def app_timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        func(*args, **kwargs)

        app_run_time.append(time.perf_counter() - start_time)
    return wrapper_timer



def timer(log):
    def deco(func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()
            value = func(*args, **kwargs)

            run_time = time.perf_counter() - start_time
            log.debug(f"{func.__name__!r} - Thread {args[1]} - Runtime: {run_time:.4f} secs")
            results_list.append(float(f'{run_time:.4f}'))

            return value
        return wrapper_timer
    return deco


def async_timer(log):
    def deco(func):
        @functools.wraps(func)
        async def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()
            await func(*args, **kwargs)

            run_time = time.perf_counter() - start_time
            log.debug(f"{func.__name__!r} - Task {args[1]} - Runtime: {run_time:.4f} secs")
            results_list.append(float(f'{run_time:.4f}'))
        return wrapper_timer
    return deco