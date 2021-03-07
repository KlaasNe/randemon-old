from time import time


def print_time(func, *args):
    start = time()
    func(*args)
    print(f"time {str(func)}: " + str(time() - start) + " seconds")