from libs import MapBlock


class MapBlockGenerator:

    @staticmethod
    def gen1(map_block: MapBlock):
        for position in map_block.size:
            chunk = map_block.get_chunk(position)
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
