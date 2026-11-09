import time


def wait_until(condition, timeout=10, interval=0.5, message=""):
    start_time = time.monotonic()
    while True:
        result = condition()
        if result:
            return result
        if time.monotonic() - start_time >= timeout:
            raise TimeoutError(f"timed out after {timeout}s: {message}; last value: {result!r}")
        time.sleep(interval)
