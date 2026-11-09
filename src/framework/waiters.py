import time
from time import sleep, monotonic


def wait_until(condition, timeout=10, interval=0.5, message=""):
    start_time = time.monotonic()
    while True:
        result = condition()
        if not result:
            if time.monotonic() - start_time >= timeout:
                raise TimeoutError(f'{message}, {result}')
            time.sleep(interval)
        else:
            return result