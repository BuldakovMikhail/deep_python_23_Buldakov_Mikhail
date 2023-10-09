class CustomList(list):
    def __add__(self, other):
        shortest = other
        longest = self

        if len(longest) < len(shortest):
            shortest, longest = longest, shortest

        temp = CustomList(longest)

        for i, val in enumerate(shortest):
            temp[i] += val

        return temp

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        temp = CustomList(self)

        if len(temp) < len(other):
            for _ in range(len(other) - len(temp)):
                temp.append(0)

        for i, val in enumerate(other):
            temp[i] -= val

        return temp

    def __rsub__(self, other):
        temp = CustomList(other)

        if len(temp) < len(self):
            for _ in range(len(self) - len(temp)):
                temp.append(0)

        for i, val in enumerate(self):
            temp[i] -= val

        return temp

    def __lt__(self, other):
        # self < other
        return sum(self) < sum(other)

    def __gt__(self, other):
        # self > other
        return sum(self) > sum(other)

    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return not self < other

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f"List: {super().__str__()}, sum: {sum(self)}"
