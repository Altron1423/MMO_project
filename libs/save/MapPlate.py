from libs.math import Vector3


class MapPlate:

    def __init__(self, chunk):
        self.position: Vector3 = Vector3()
        self.type = None
        self.chunk = chunk
        self.entities = []
