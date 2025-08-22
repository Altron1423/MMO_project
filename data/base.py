import time
import json
import os


def generate_path(path:str):
    path = path.split('\\')
    if path[-1].find("."):
        path = path[:-1]
    # print(path)
    for iPath in range(1, len(path)+1):
        # print("\\".join(path[:iPath]))
        if os.path.exists("\\".join(path[:iPath])):
            pass
        else:
            break
    else:
        print("complit")
        return
    for i in range(iPath, len(path)+1):
        os.mkdir("\\".join(path[:i]))


class Vector2:
    LenFindeTF = True

    def __init__(self, *args):
        self.x = self.y = None
        tf = True
        if len(args) == 0:
            args = (0, 0)
        elif type(args[0]) == tuple:
            args = args[0]
        elif isinstance(args[0], Vector2):
            other = args[0]
            self.__dict__["x"] = other.x
            self.__dict__["y"] = other.y
            self._ln = other._ln
            tf = False
        elif len(args) == 1:
            args = (args[0], 0)
        if tf:
            x, y = args[0], args[1]
            self.__dict__["x"] = x
            self.__dict__["y"] = y
            if self.LenFindeTF:
                self._ln = (x ** 2 + y ** 2) ** 0.5
            else:
                self._ln = None

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        if self.LenFindeTF:
            self._ln = (self.x ** 2 + self.y ** 2) ** 0.5
        return self

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        if self.LenFindeTF:
            self._ln = (self.x ** 2 + self.y ** 2) ** 0.5
        return self

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __imul_(self, other):
        self.x *= other
        self.y *= other
        if self.LenFindeTF:
            self._ln = (self.x ** 2 + self.y ** 2) ** 0.5
        return self

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __itruediv__(self, other):
        self.x /= other
        self.y /= other
        if self.LenFindeTF:
            self._ln = (self.x ** 2 + self.y ** 2) ** 0.5
        return self

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        if (key == "x" or key == "y") and self.LenFindeTF:
            self.__dict__["_ln"] = (self.x ** 2 + self.y ** 2) ** 0.5

    def distance_to(self, other):
        x = other.x - self.x
        y = other.y - self.y
        return (x ** 2 + y ** 2) ** 0.5

    def distance_squared_to(self, other):
        x = other.x - self.x
        y = other.y - self.y
        return x ** 2 + y ** 2

    def len(self):
        self._ln = (self.x ** 2 + self.y ** 2) ** 0.5
        return self._ln


class Vector3:
    LenFindeTF = True

    def __init__(self, *args):
        self.x = self.y = self.z = None
        tf = True
        if len(args) == 0:
            args = (0, 0, 0)
        elif type(args[0]) == tuple:
            args = args[0]
        elif isinstance(args[0], Vector2):
            other = args[0]
            self.__dict__["x"] = other.x
            self.__dict__["y"] = other.y
            self.__dict__["z"] = 0
            self._ln = other._ln
            tf = False
        elif isinstance(args[0], Vector3):
            other = args[0]
            self.__dict__["x"] = other.x
            self.__dict__["y"] = other.y
            self.__dict__["z"] = other.z
            self._ln = other._ln
            tf = False
        elif len(args) == 1:
            args = (args[0], 0, 0)
        elif len(args) == 2:
            args = (args[0], args[1], 0)
        if tf:
            x, y, z = args[0], args[1], args[2]
            self.__dict__["x"] = x
            self.__dict__["y"] = y
            self.__dict__["z"] = z
            if self.LenFindeTF:
                self._ln = (x ** 2 + y ** 2 + z ** 2) ** 0.5
            else:
                self._ln = None

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        if self.LenFindeTF:
            self._ln = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        return self

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        if self.LenFindeTF:
            self._ln = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        return self

    def __mul__(self, other):
        return Vector3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self * other

    def __imul_(self, other):
        self.x *= other
        self.y *= other
        self.z *= other
        if self.LenFindeTF:
            self._ln = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        return self

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other, self.z / other)

    def __itruediv__(self, other):
        self.x /= other
        self.y /= other
        self.z /= other
        if self.LenFindeTF:
            self._ln = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        return self

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        if self.LenFindeTF and (key == "x" or key == "y" or key == "z"):
            self.__dict__["_ln"] = (self.x ** 2 + self.y ** 2) ** 0.5

    def distance_to(self, other):
        x = other.x - self.x
        y = other.y - self.y
        z = other.z - self.z
        return (x ** 2 + y ** 2 + z ** 2) ** 0.5

    def distance_squared_to(self, other):
        x = other.x - self.x
        y = other.y - self.y
        z = other.z - self.z
        return (x ** 2 + y ** 2 + z ** 2)

    def len(self):
        self._ln = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        return self._ln


class Timers:
    class ITimer:
        def __init__(self, timer):
            self.name = timer["name"]
            self.timeAct = time.time() + timer["timeAct"]
            self.func = timer["func"]
            self.data = timer["data"]

    def __init__(self, regul=1):
        """
        regul - the interval between timer checks
        :param regul:
        """
        self.timers = []
        self.regul = regul
        self.nextUpdate = time.time() + regul

    def add(self, timers:dict):
        """
        Add new timer with input param
        timers = {"name": str, "timeAct": int, "func": function, "data": list}
        :param timers:
        :return:
        """
        self.timers.append(self.ITimer(timers))

    def update(self):
        if self.nextUpdate <= time.time():
            self.nextUpdate += self.regul
            for iT in self.timers:
                if iT.timeAct <= time.time():
                    iT.func(iT.data)
                    self.timers.remove(iT)


class GameElement:
    def __init__(self, path:str, exceptions:list):
        self.path = path
        # self.name = ""
        self.exceptions = exceptions

    def save(self):
        save_data = {}
        for i in self.exceptions:
            save_data[i] = self.__dict__[i]
            self.__dict__[i] = None
        try:
            with open(self.path, "w") as f:
                pass
        except:
            generate_path(self.path)
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.__dict__))

        for i in self.exceptions:
            self.__dict__[i] = save_data[i]

    def load(self):
        try:
            with open(f"{self.path}.json", "x") as f:
                pass
        except:
            generate_path(self.path)
        with open(f"{self.path}.json", "r", encoding="utf-8") as f:
            return json.load(f)





# Vector3.LenFindeTF = False
#
# Vector2.LenFindeTF = False

if __name__ == "__main__":
    pass
    generate_path(r"C:\Users\Altron\PycharmProjects\MMO_project\saves\test_world\main.json")



