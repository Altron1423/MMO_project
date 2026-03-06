import json

from src.modules.save.MapChunk import MapChunks


class Dimension:
    SIZE_X: int
    SIZE_Y: int
    SIZE_Z: int
    CountChunkX: int
    CountChunkZ: int
    map: list[list[MapChunks]]



    ...
