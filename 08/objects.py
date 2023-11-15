import weakref
import cProfile

from time import process_time
from memory_profiler import profile


class TestObj:
    def __init__(self, var) -> None:
        self.var = var

    def add(self, val):
        self.var += val


class ChestMain:
    def __init__(self, threasures, latitude):
        self.threas = threasures
        self.lat = latitude
        self.long = self.lat


class ChestSlots:
    __slots__ = ("threas", "lat", "long")

    def __init__(self, threasures, latitude):
        self.threas = threasures
        self.lat = latitude
        self.long = self.lat


class ChestWeakref:
    def __init__(self, threasures, latitude):
        self.threas = threasures
        self.lat = latitude
        self.long = weakref.ref(self.lat)


def measure_chest_main_time(obj_count=50000, measures=10):
    start_create_time = process_time()
    for _ in range(measures):
        arr = [ChestMain(2 * i, TestObj(i)) for i in range(obj_count)]
    end_create_time = process_time()

    res_create_time = (end_create_time - start_create_time) / measures

    start_changing_time = process_time()
    for _ in range(measures):
        for cls in arr:
            cls.threas += 1
            cls.lat.add(1)
            cls.long.add(1)
    end_changing_time = process_time()

    res_changing_time = (end_changing_time - start_changing_time) / measures

    return res_create_time, res_changing_time


def measure_chest_slots_time(obj_count=50000, measures=10):
    start_create_time = process_time()
    for _ in range(measures):
        arr = [ChestSlots(2 * i, TestObj(i)) for i in range(obj_count)]
    end_create_time = process_time()

    res_create_time = (end_create_time - start_create_time) / measures

    start_changing_time = process_time()
    for _ in range(measures):
        for cls in arr:
            cls.threas += 1
            cls.lat.add(1)
            cls.long.add(1)
    end_changing_time = process_time()

    res_changing_time = (end_changing_time - start_changing_time) / measures

    return res_create_time, res_changing_time


def measure_chest_weakref_time(obj_count=50000, measures=10):
    start_create_time = process_time()
    for _ in range(measures):
        arr = [ChestWeakref(2 * i, TestObj(i)) for i in range(obj_count)]
    end_create_time = process_time()

    res_create_time = (end_create_time - start_create_time) / measures

    start_changing_time = process_time()
    for _ in range(measures):
        for cls in arr:
            cls.threas += 1
            cls.lat.add(1)
            cls.long().add(1)
    end_changing_time = process_time()

    res_changing_time = (end_changing_time - start_changing_time) / measures

    return res_create_time, res_changing_time


@profile
def measure_chest_main_memory(obj_count=50000):
    arr = [ChestMain(2 * i, TestObj(i)) for i in range(obj_count)]

    for cls in arr:
        cls.threas += 1
        cls.lat.add(1)
        cls.long.add(1)


@profile
def measure_chest_slots_memory(obj_count=50000):
    arr = [ChestSlots(2 * i, TestObj(i)) for i in range(obj_count)]
    for cls in arr:
        cls.threas += 1
        cls.lat.add(1)
        cls.long.add(1)


@profile
def measure_chest_weakref_memory(obj_count=50000):
    arr = [ChestWeakref(2 * i, TestObj(i)) for i in range(obj_count)]
    for cls in arr:
        cls.threas += 1
        cls.lat.add(1)
        cls.long().add(1)


def measure_chest_main_calls(obj_count=50000):
    arr = [ChestMain(2 * i, TestObj(i)) for i in range(obj_count)]

    for cls in arr:
        cls.threas += 1
        cls.lat.add(1)
        cls.long.add(1)


def measure_chest_slots_calls(obj_count=50000):
    arr = [ChestSlots(2 * i, TestObj(i)) for i in range(obj_count)]
    for cls in arr:
        cls.threas += 1
        cls.lat.add(1)
        cls.long.add(1)


def measure_chest_weakref_calls(obj_count=50000):
    arr = [ChestWeakref(2 * i, TestObj(i)) for i in range(obj_count)]
    for cls in arr:
        cls.threas += 1
        cls.lat.add(1)
        cls.long().add(1)


if __name__ == "__main__":
    N = 500_000
    MC = 100

    chest_main = measure_chest_main_time(N, MC)
    print(
        f"Время создания {N=} классов c обычными атрибутами:\
        {chest_main[0]} мс."
    )
    print(
        f"Время изменения {N=} классов c обычными атрибутами:\
        {chest_main[1]} мс."
    )

    chest_slots = measure_chest_slots_time(N, MC)
    print(f"Время создания {N=} классов со слотами: {chest_slots[0]} мс.")
    print(f"Время изменения {N=} классов со слотами: {chest_slots[1]} мс.")

    chest_weakref = measure_chest_weakref_time(N, MC)
    print(f"Время создания {N=} классов c weakref: {chest_weakref[0]} мс.")
    print(f"Время изменения {N=} классов c weakref: {chest_weakref[1]} мс.")

    measure_chest_main_memory()
    measure_chest_slots_memory()
    measure_chest_weakref_memory()

    with cProfile.Profile() as pr:
        measure_chest_main_calls(N)
        measure_chest_slots_calls(N)
        measure_chest_weakref_calls(N)

        pr.print_stats()
