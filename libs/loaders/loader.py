from pathlib import Path


class Loader:
    elements: dict[str, object]

    def __init__(self):
        self.elements = {}

    def load(self, path: Path) -> None:
        ...

    def load_from_dir(self, path: Path) -> None:
        for iPath in path.iterdir():
            self.load(iPath)

    def add(self, element: object, name: str) -> None:
        self.elements[name] = element

    def get(self, name: str) -> object | None:
        element = self.elements.get(name)
        return element

    def get_changeable(self, name: str) -> object | None:
        ...

    def get_new(self, name: str) -> object | None:
        element = self.elements.get(name)
        return element.__copy__() if element else None

