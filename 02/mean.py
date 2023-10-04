import time


def mean(n):
    if n <= 0:
        raise Exception("Decorator error, number of measures <= 0")

    last_measures = [None] * n
    i = 0

    def _mean(func):
        def inner(*args, **kwargs):
            nonlocal i

            time_start = time.time()

            ret = func(*args, **kwargs)

            time_end = time.time()

            last_measures[i % n] = time_end - time_start
            i += 1

            sum_time = 0
            count = 0

            for t in last_measures:
                if t is not None:
                    sum_time += t
                    count += 1

            print(f"Среднее время: {sum_time / count} сек.")

            return ret

        return inner

    return _mean


# @mean(4)
# def b():
#     time.sleep(0.6)


# @mean(3)
# def a():
#     time.sleep(0.5)


# a()
# a()
# a()

# print("----------------------------")


# b()
# b()
# b()
# b()
# b()
