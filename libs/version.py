

class Version:
    major: int
    minor: int
    patch: int

    def __init__(self, data: str):
        self.major, self.minor, self.patch = data.split('.')

    def __str__(self):
        return f'{self.major}.{self.minor}.{self.patch}'

    # def __contains__(self, item: Version):

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return str(self) == other
        elif isinstance(other, Version):
            return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)
        return False

    def __ne__(self, other) -> bool:
        if isinstance(other, str):
            return str(self) != other
        elif isinstance(other, Version):
            return (self.major, self.minor, self.patch) != (other.major, other.minor, other.patch)
        return False
