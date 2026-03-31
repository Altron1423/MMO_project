from libs import AttributeEntityDTO


class Attributer:
    _basic: AttributeEntityDTO
    _elevated: AttributeEntityDTO
    _artefacts: AttributeEntityDTO
    _effects: AttributeEntityDTO
    _ratio: AttributeEntityDTO
    result: AttributeEntityDTO

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
        self._basic = AttributeEntityDTO()
        self._elevated = AttributeEntityDTO()

        self._artefacts = AttributeEntityDTO()
        self._effects = AttributeEntityDTO()

        self._ratio = AttributeEntityDTO()

        self.result = AttributeEntityDTO()

    def save(self):
        ...

    def load(self, data):
        ...

    def update(self):
        self.result = (self._basic + self._elevated + self._artefacts + self._effects) * self._ratio

    @property
    def constitution(self) -> int:
        return self.result.constitution

    @constitution.setter
    def constitution(self, value):
        print(value)

    @property
    def agility(self) -> int:
        return self.result.agility

    @agility.setter
    def agility(self, value):
        print(value)

    @property
    def defense(self) -> int:
        return self.result.defense

    @defense.setter
    def defense(self, value):
        print(value)

    @property
    def strength(self) -> int:
        return self.result.strength

    @strength.setter
    def strength(self, value):
        print(value)

    @property
    def intellect(self) -> int:
        return self.result.intellect

    @intellect.setter
    def intellect(self, value):
        print(value)

    @property
    def spirit(self) -> int:
        return self.result.spirit

    @spirit.setter
    def spirit(self, value):
        print(value)

    @property
    def health_reg(self) -> int:
        return self.result.health_reg

    @health_reg.setter
    def health_reg(self, value):
        print(value)

    @property
    def max_mana(self) -> int:
        return self.result.max_mana

    @max_mana.setter
    def max_mana(self, value):
        print(value)
