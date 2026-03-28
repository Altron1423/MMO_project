from dataclasses import dataclass

from libs import MapPlateConfigDTO, MapPlate, MapPlateSaveDTO


@dataclass(frozen=True, slots=True)
class MapPlateSaveMapper:

    @staticmethod
    def dto_to_dict(dto: MapPlateSaveDTO) -> dict:
        return {
            "full_name": dto.full_name,
            "name": dto.name,
            "id": dto.id,
            "type": dto.type,
            "custom_data": dto.custom_data,
        }

    @staticmethod
    def dict_to_dto(data: dict) -> MapPlateSaveDTO:
        return MapPlateSaveDTO(
            full_name=data["full_name"],
            name=data["name"],
            id=data["id"],
            type=data["type"],
            custom_data=data["custom_data"],
        )

    @staticmethod
    def plate_to_dto(map_chunk: MapPlate) -> MapPlateSaveDTO:
        return MapPlateSaveDTO(
            full_name=str(map_chunk),
            name=map_chunk.name,
            id=map_chunk.id,
            type=map_chunk.type,
            custom_data=map_chunk.get_custom_data()
        )

    @staticmethod
    def update_from_dto(plate:MapPlate, dto: MapPlateSaveDTO):
        plate.full_name = dto.full_name
        plate.name = dto.name
        plate.id = dto.id
        plate.type = dto.type
        plate.custom_data = dto.custom_data


@dataclass(frozen=True, slots=True)
class MapPlateConfigMapper:

    # @staticmethod
    # def dto_to_dict(dto: MapPlateConfigDTO) -> dict:
    #     return {
    #         "name": dto.name,
    #         "type": dto.type,
    #         "color": dto.color,
    #         "texture": dto.texture,
    #         "height": dto.height
    #     }

    @staticmethod
    def dict_to_dto(data: dict) -> MapPlateConfigDTO:
        return MapPlateConfigDTO(
            name=data["name"],
            type=data["type"],
            color=data["color"],
            texture=data["texture"],
            changeable=data["changeable"],
        )
