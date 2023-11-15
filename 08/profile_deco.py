import time
import cProfile
import pstats


def profile_deco(func):
    profiler = cProfile.Profile()

    def print_stats():
        sortby = "cumulative"
        prof_stats = pstats.Stats(profiler).sort_stats(sortby)
        prof_stats.print_stats()

    def __inner(*args, **kwargs):
        profiler.enable()
        res = func(*args, **kwargs)
        profiler.disable()

        return res

    __inner.print_stat = print_stats

    return __inner


@profile_deco
def sleepy(a):
    time.sleep(a)


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


add(1, 2)
add(4, 5)
sub(4, 5)

# print(add.__dict__)

# выводится результат профилирования суммарно по
# всем вызовам функции add (всего два вызова)
add.print_stat()

# выводится результат профилирования суммарно по
# всем вызовам функции sub (всего один вызов)
sub.print_stat()


sleepy(2)
sleepy(1)
sleepy(3)

sleepy.print_stat()
