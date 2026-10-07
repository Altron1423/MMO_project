from json import loads, dumps
from libs.dtos.entity import AttributeLayerEntityDTO
from libs.mappers.entity import AttributeLayerEntityMapper


class Attributer:
    _type_: str = "Attributer"

    _basic: AttributeLayerEntityDTO
    _elevated: AttributeLayerEntityDTO
    _artefacts: AttributeLayerEntityDTO
    _effects: AttributeLayerEntityDTO
    _ratio: AttributeLayerEntityDTO
    result: AttributeLayerEntityDTO

    def __init__(self):
        """
            constitution - телосложение
            agility - ловкость
            defense - защита
            strength - сила
            intellect - интеллект
            spirit - дух
            health_reg - здоровье
            max_mana - макс_мана
        """
        self._basic = AttributeLayerEntityDTO()
        self._elevated = AttributeLayerEntityDTO()

        self._artefacts = AttributeLayerEntityDTO()
        self._effects = AttributeLayerEntityDTO()

        self._ratio = AttributeLayerEntityDTO()

        self.result = AttributeLayerEntityDTO()

    def save(self):
        ...

    def load_from_str(self, data: str):
        if data[0] == '<' and data[-1] == '>':
            data = data[1:-1]
            tp, data = data.split('_')
            if tp != self._type_:
                raise TypeError(f"This string not {self._type_}")
            # print(data)
            self.load(loads(data))
        else:
            raise TypeError("Attributer only accepts strings")


    def load(self, data: dict[str, list[int | float]]):
        if "basic" in data:
            self._basic = AttributeLayerEntityMapper.list_to_dto(data["basic"])
        if "elevated" in data:
            self._elevated = AttributeLayerEntityMapper.list_to_dto(data["elevated"])
        if "artefacts" in data:
            self._artefacts = AttributeLayerEntityMapper.list_to_dto(data["artefacts"])
        if "effects" in data:
            self._effects = AttributeLayerEntityMapper.list_to_dto(data["effects"])
        if "ratio" in data:
            self._ratio = AttributeLayerEntityMapper.list_to_dto(data["ratio"])

    def update(self):
        self.result = (self._basic + self._elevated + self._artefacts + self._effects) * self._ratio

    @property
    def constitution(self) -> int:
        return self.result.constitution

    # @constitution.setter
    # def constitution(self, value):
    #     print(value)

    @property
    def agility(self) -> int:
        return self.result.agility

    @property
    def defense(self) -> int:
        return self.result.defense

    @property
    def strength(self) -> int:
        return self.result.strength

    @property
    def intellect(self) -> int:
        return self.result.intellect

    @property
    def spirit(self) -> int:
        return self.result.spirit

    @property
    def health_reg(self) -> int:
        return self.result.health_reg

    @property
    def max_mana(self) -> int:
        return self.result.max_mana

    def __dict__(self):
        return {
            "basic": AttributeLayerEntityMapper.dto_to_list(self._basic),
            "elevated": AttributeLayerEntityMapper.dto_to_list(self._elevated),
            "artefacts": AttributeLayerEntityMapper.dto_to_list(self._artefacts),
            "effects": AttributeLayerEntityMapper.dto_to_list(self._effects),
            "ratio": AttributeLayerEntityMapper.dto_to_list(self._ratio),
        }

    def __str__(self):
        return f"<{self._type_}_{dumps(self.__dict__(), separators=(',', ':'))}>"
