import os
import json
import shutil

from datetime import datetime
from pathlib import Path

from libs.dtos import (
    DimensionSaveDTO, MapBlockSaveDTO, MapChunkSaveDTO, MapPlateSaveDTO,
    CreateSaveWF_DTO, DataSaveDTO
)
from libs.loaders import (
    dimension_loader,
    map_block_loader,
    map_chunk_loader,
    map_plate_loader,
)
from libs.mappers import (
    SaveMapper,
    DimensionSaveMapper,
    MapBlockSaveMapper,
    MapChunkSaveMapper,
    MapPlateSaveMapper
)
from libs.math import Position2
from libs.save import (
    SaveFull, SaveLight,
    MapPlate, MapChunk,
    MapBlock, Dimension
)


class SavesWF:
    path_map: Path

    def __init__(self, path: Path):
        self.path = path
        self.path_map = path.joinpath("maps")
        self.path_dim = self.path_map.joinpath("dimensions")
        self.path_blocks = self.path_map.joinpath("blocks")
        self.path_chunks = self.path_map.joinpath("chunks")
        self.path_plates = self.path_map.joinpath("plates")

    @staticmethod
    def get_save_info(path_save_directory: Path) -> DataSaveDTO:
        with open(path_save_directory.joinpath("main.json"), "r", encoding="utf-8") as f:
            data = SaveMapper.dict_to_dto(json.load(f))
        return data

    @staticmethod
    def create_save(create_save: CreateSaveWF_DTO) -> None:
        path = create_save.path_to_save.joinpath(create_save.name)
        os.mkdir(path)
        SavesWF.__create_file__(
            path.joinpath("main.json"),
            {
                "name": create_save.name,
                "version": ".".join(map(str, create_save.version)),
                "description": create_save.description,
                "last_open": str(create_save.last_open),
                "created": str(create_save.created),
            }
        )
        SavesWF.__create_save_files__(path)

    @staticmethod
    def delete(path_save_directory: Path):
        shutil.rmtree(path_save_directory)

    @staticmethod
    def load_save_light(save: SaveLight):
        SaveMapper.update_from_dto(
            save,
            SavesWF.get_save_info(save.path_save)
        )

    def load_save_full(self, save: SaveFull):
        plates = {}
        chunks = {}
        blocks = {}
        dimensions = []
        for iPath in self.path_plates.iterdir():
            plate = self.__load_plates__(iPath)
            plates[str(plate)] = plate

        for iPath in self.path_chunks.iterdir():
            chunk = self.__load_chunk__(iPath, plates)
            chunks[str(chunk)] = chunk

        for iPath in self.path_blocks.iterdir():
            block = self.__load_block__(iPath, chunks)
            blocks[str(block)] = block

        for iPath in self.path_dim.iterdir():
            dim = self.__load_dimension__(iPath, blocks)
            dimensions.append(dim)

        save.dimensions = dimensions

    @staticmethod
    def __load_plates__(path: Path) -> MapPlate:
        with open(path, "r", encoding="utf-8") as file:
            dto = MapPlateSaveMapper.dict_to_dto(json.load(file))
        plate = map_plate_loader.get_changeable(dto.name)
        MapPlateSaveMapper.update_from_dto(plate, dto)
        return plate

    @staticmethod
    def __load_chunk__(path: Path, plates: dict[str, MapPlate]) -> MapChunk:
        with open(path, "r", encoding="utf-8") as file:
            dto = MapChunkSaveMapper.dict_to_dto(json.load(file))
        chunk = map_chunk_loader.get_new(dto.name)
        MapChunkSaveMapper.update_from_dto(chunk, dto)
        for chunk_name in dto.changes_plates:
            chunk.set_plate_on(
                plates[chunk_name],
                Position2(dto.changes_plates[chunk_name])
            )
        return chunk

    @staticmethod
    def __load_block__(path: Path, chunks: dict[str, MapChunk]) -> MapBlock:
        with open(path, "r", encoding="utf-8") as file:
            dto = MapBlockSaveMapper.dict_to_dto(json.load(file))
        block = map_block_loader.get_new(dto.name)
        MapBlockSaveMapper.update_from_dto(block, dto)
        for position in block.size:
            chunk_name = dto.chunks[position.z][position.x]
            if chunk_name is not None:
                block.set_chunk_on(
                    chunks[chunk_name],
                    position
                )
        return block

    @staticmethod
    def __load_dimension__(path: Path, blocks: dict[str, MapBlock]) -> Dimension:
        with open(path, "r", encoding="utf-8") as file:
            dto = DimensionSaveMapper.dict_to_dto(json.load(file))
        dim: Dimension = dimension_loader.get_new(dto.name)
        DimensionSaveMapper.update_from_dto(dim, dto)
        for block_name in dto.blocks:
            block = blocks[block_name]
            dim.add_map_block(
                block,
            )
        return dim


    def saving(self, save_full: SaveFull):

        with open(self.path.joinpath("main.json"), "w", encoding="utf-8") as file:
            json.dump(
                {
                    "name": "test_world3",
                    "version": ".".join(map(str, save_full.version)),
                    "description": save_full.description,
                    "last_open": str(datetime.now()),
                    "created": save_full.created
                },
                file
            )

        for i_dimension in save_full.dimensions:
            self.__saving_dimension__(
                DimensionSaveMapper.dim_to_dto(i_dimension)
            )
            for i_map_block in i_dimension.blocks:
                self.__saving_block__(
                    MapBlockSaveMapper.block_to_dto(i_map_block)
                )
                for position in i_map_block.size:
                    chunk = i_map_block.get_chunk(position)
                    if chunk:
                        self.__saving_chunk__(
                            MapChunkSaveMapper.chunk_to_dto(
                                chunk
                            )
                        )
                        for position_plate in chunk.size:
                            plate = chunk.get_plate(position_plate)
                            if plate.changeable and plate.id != 0:
                                self.__saving_plate__(
                                    MapPlateSaveMapper.plate_to_dto(
                                        plate
                                    )
                                )

    def __saving_plate__(self, map_plate: MapPlateSaveDTO):
        path = self.path_plates.joinpath(f"{map_plate.name}_{map_plate.id}.json")
        with open(path, "+w", encoding="utf-8") as file:
            json.dump(
                MapPlateSaveMapper.dto_to_dict(map_plate),
                file
            )

    def __saving_chunk__(self, map_chunk: MapChunkSaveDTO):
        path = self.path_chunks.joinpath(f"{map_chunk.name}_{map_chunk.id}.json")
        with open(path, "+w", encoding="utf-8") as file:
            json.dump(
                MapChunkSaveMapper.dto_to_dict(map_chunk),
                file
            )

    def __saving_block__(self, map_block: MapBlockSaveDTO):
        path = self.path_blocks.joinpath(f"{map_block.name}_{map_block.id}.json")
        with open(path, "+w", encoding="utf-8") as file:
            json.dump(
                MapBlockSaveMapper.dto_to_dict(map_block),
                file
            )

    def __saving_dimension__(self, dimension: DimensionSaveDTO):
        path = self.path_dim.joinpath(f"{dimension.name}.json")
        with open(path, "+w", encoding="utf-8") as file:
            json.dump(
                DimensionSaveMapper.dto_to_dict(dimension),
                file
            )

    @staticmethod
    def __create_save_files__(path: Path) -> None:
        SavesWF.__create_file__(
            path.joinpath("players.json"),
            {
                "type": "player_saves",
                "players": []
            }
        )
        path_map = path.joinpath("maps")
        os.mkdir(path_map.joinpath("dimensions"))
        os.mkdir(path_map.joinpath("blocks"))
        os.mkdir(path_map.joinpath("chunks"))
        os.mkdir(path_map.joinpath("plates"))

    @staticmethod
    def __create_file__(path: Path, data: dict):
        with open(path, "a", encoding="utf-8") as file:
            json.dump(data, file)
