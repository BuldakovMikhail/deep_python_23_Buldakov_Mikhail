class Integer:
    def __set_name__(self, owner, name):
        self.name = f"int_desc_{name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None
        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if obj is None:
            return None

        if not isinstance(val, int):
            raise ValueError("Int required")

        return setattr(obj, self.name, val)


class String:
    def __init__(self, length=100):
        self.length = length

    def __set_name__(self, owner, name):
        self.name = f"str_desc_{name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None
        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if obj is None:
            return None

        if not isinstance(val, str):
            raise ValueError("String required")

        if len(val) > self.length:
            raise ValueError(f"String length must be <= {self.length}")

        return setattr(obj, self.name, val)


class PositiveInteger:
    def __set_name__(self, owner, name):
        self.name = f"pos_int_desc_{name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None
        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if obj is None:
            return None

        if not isinstance(val, int):
            raise ValueError("Int required")

        if val <= 0:
            raise ValueError("Value must be grater than 0")

        return setattr(obj, self.name, val)


class Track:
    """
    Класс Track является сущностью в музыкальном альбоме.
    order - устанавливает относительный порядок треков (мб отрицательным)
    auditions_num - количество прослушиваний (> 0)
    name - название трека (длинной не больше 100 символов)
    """

    order = Integer()
    name = String()
    auditions_num = PositiveInteger()

    def __init__(self, name, auditions_num, order):
        self.name = name
        self.auditions_num = auditions_num
        self.order = order

    def get_name(self):
        return self.name

    def get_auditions_num(self):
        return self.auditions_num

    def get_order(self):
        return self.order

    def __str__(self):
        print(self.__dict__)
        return f"Name: {self.name}, \
                Aud_Num: {self.auditions_num}, Order: {self.order}"
