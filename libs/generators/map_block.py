from libs import MapBlock
from libs.math import Position2


class MapBlockGenerator:

    @staticmethod
    def gen1(map_block: MapBlock) -> Position2 | None:
        spawn_position = None
        for position in map_block.size:
            if spawn_position is not None:
                break
            chunk = map_block.get_chunk(position)
            if chunk:
                for i in chunk.size:
                    if chunk.get_plate(i).type == "spawn":
                        spawn_position = i * 50
                        break
            # print(chunk, position)
            # if chunk:
            #     print(chunk)
            #     for i in chunk.map:
            #         for j in i:
            #             print(f"{str(j):<17}", end="")
            #         print()
            #         # print([str(g) for g in i])
            #     print()
            # # if chunk:
            # #     MapChunkGenerator.gen1(chunk)
        return spawn_position
