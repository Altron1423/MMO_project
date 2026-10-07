from dataclasses import dataclass

from libs import MapChunkSaveDTO, MapChunk, MapChunkConfigDTO


@dataclass(frozen=True, slots=True)
class MapChunkSaveMapper:

    @staticmethod
    def dto_to_dict(dto: MapChunkSaveDTO) -> dict:
        return {
            "full_name": dto.full_name,
            "name": dto.name,
            "id": dto.id,
            "changes_plates": dto.changes_plates,
        }

    @staticmethod
    def dict_to_dto(data: dict) -> MapChunkSaveDTO:
        return MapChunkSaveDTO(
            full_name=data["full_name"],
            name=data["name"],
            id=data["id"],
            changes_plates=data["changes_plates"],
        )

    @staticmethod
    def chunk_to_dto(map_chunk: MapChunk) -> MapChunkSaveDTO:
        changes_plates = {}
        for position in map_chunk.size:
            plate = map_chunk.get_plate(position)
            if plate.changeable:
                changes_plates[str(plate)] = str(position)
        return MapChunkSaveDTO(
            full_name=str(map_chunk),
            name=map_chunk.name,
            id=map_chunk.id,
            changes_plates = changes_plates
        )

    @staticmethod
    def update_from_dto(chunk: MapChunk, dto: MapChunkSaveDTO):
        chunk.full_name = dto.full_name
        chunk.name = dto.name
        chunk.id = dto.id


@dataclass(frozen=True, slots=True)
class MapChunkConfigMapper:

    @staticmethod
    def dict_to_dto(data: dict) -> MapChunkConfigDTO:
        return MapChunkConfigDTO(
            name=data["name"],
            size=data["size"],
            plates=data["plates"],
            map_plates=data["map_plates"],
            height_map=data["height_map"],
        )
